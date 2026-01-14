"""
Transcription utilities for AURA
Uses AssemblyAI Cloud API for high-speed transcription.
"""

import warnings
import re
import json
import time
from typing import Optional
import google.generativeai as genai

warnings.filterwarnings('ignore')

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except (BrokenPipeError, IOError):
        pass


class AssemblyAITranscriber:
    """
    Cloud-based transcription using AssemblyAI API
    Ultra-Fast, supports 100+ languages
    """
    # Mapping Heritage Names to AssemblyAI ISO Codes
    AAI_LANG_MAP = {
        'Telugu': 'te',
        'Tamil': 'ta',
        'Hindi': 'hi',
        'Kannada': 'kn',
        'Malayalam': 'ml',
        'English': 'en'
    }

    def __init__(self, api_key: str, gemini_api_key: Optional[str] = None):
        import assemblyai as aai
        self.api_key = api_key
        aai.settings.api_key = api_key
        self.gemini_api_key = gemini_api_key
        
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key)
            # CEO Choice: 2.0-Flash-Exp (Experimental tier often has separate quota)
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    # CEO Choice: Robust Fallback List
    FALLBACK_MODELS = [
        'gemini-2.0-flash-exp',
        'gemini-2.0-flash',
        'gemini-2.0-flash-lite-preview-02-05',
        'gemini-flash-latest', # Added stable fallback
        'gemini-1.5-flash', # Explicit 1.5 fallback
    ]

    def _generate_with_retry(self, prompt: str, retries_per_model: int = 2):
        """Generates content with model rotation to handle 429 Quota errors."""
        for model_name in self.FALLBACK_MODELS:
            try:
                # safe_print(f"      Trying model: {model_name}...", flush=True)
                model = genai.GenerativeModel(model_name)
                
                # Retry loop for the specific model
                for i in range(retries_per_model):
                    try:
                        response = model.generate_content(prompt)
                        if response and response.text:
                            return response
                    except Exception as e:
                        err_str = str(e).lower()
                        # If it's a quota error or 503, wait and retry same model briefly
                        if ("429" in err_str or "quota" in err_str or "503" in err_str) and i < retries_per_model - 1:
                            time.sleep(2 * (i + 1))
                            continue
                        elif "404" in err_str:
                            # Model not found, break to next model immediately
                            break
                        else:
                            # If it's 429 on last attempt, let outer loop handle it
                            if "429" in err_str or "quota" in err_str:
                                pass 
                            else:
                                raise e
                
                # If we get here, this model failed or exhausted retries
                safe_print(f"      ⚠️ Quota/Error on {model_name}. Switching...", flush=True)
                time.sleep(1)
                
            except Exception as e:
                safe_print(f"      ⚠️ Setup failed for {model_name}: {e}", flush=True)
                continue
                
        return None

    def transcribe_audio(self, audio_path: str, language: str = None) -> dict:
        """Transcribe audio using AssemblyAI Cloud API and return timed segments"""
        import assemblyai as aai
        
        # Map language to code
        aai_lang_code = self.AAI_LANG_MAP.get(language, 'en')
        safe_print(f"☁️ Sending to AssemblyAI Cloud (Code: {aai_lang_code})...", flush=True)
        
        if language == "English" or not language:
            config = aai.TranscriptionConfig(
                speech_model="best",
                language_detection=True
            )
        else:
            config = aai.TranscriptionConfig(
                speech_model="best",
                language_code=aai_lang_code
            )
        
        transcriber = aai.Transcriber(config=config)
        transcript = transcriber.transcribe(audio_path)
        
        if transcript.status == "error":
            raise Exception(f"AssemblyAI Transcription failed: {transcript.error}")
            
        segments = []
        try:
            sentences = transcript.get_sentences()
            for s in sentences:
                segments.append({
                    'start': s.start,
                    'end': s.end,
                    'text': s.text
                })
        except Exception as e:
            safe_print(f"    ⚠️ Sentence segmentation failed: {e}")

        words = []
        if transcript.words:
            for i, w in enumerate(transcript.words):
                words.append({
                    'id': f"word-{i}",
                    'text': w.text,
                    'start': w.start,
                    'end': w.end,
                    'confidence': w.confidence
                })
        
        if not segments and transcript.text:
            safe_print("    ⚠️ get_sentences() returned empty. Reconstructing chunks from words...", flush=True)
            if words:
                for i in range(0, len(words), 15):
                    chunk = words[i:i + 15]
                    segments.append({
                        'id': f"seg-{i//15}",
                        'start': chunk[0]['start'],
                        'end': chunk[-1]['end'],
                        'text': " ".join([w['text'] for w in chunk])
                    })
            else:
                segments.append({
                    'id': "seg-0",
                    'start': 0,
                    'end': 0,
                    'text': transcript.text
                })
            
        return {
            'text': transcript.text,
            'segments': segments,
            'words': words
        }

    def _parse_pipe_delimited_translations(self, text: str) -> dict:
        """
        Robust Parser: Handles Pipe-Delimited Output (ID | Text)
        """
        results = {}
        if not text: return results
        
        # Split by newlines
        lines = text.strip().split('\n')
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # Remove potential code block markers
            if line.startswith("```") or line.endswith("```"): continue
            
            # pipe split
            parts = line.split('|', 1)
            if len(parts) >= 2:
                try:
                    seg_id = int(parts[0].strip())
                    trans_text = parts[1].strip()
                    results[seg_id] = trans_text
                except:
                    continue
        return results

    def perform_gemini_synthesis(self, transcription_result: dict, source_language: str, target_language: str = "Tamil") -> dict:
        """
        Post-processes raw transcription through Gemini using BATCH PROCESSING.
        """
        all_synced_segments = []
        summary = "Cloud Analysis complete."
        
        segments = transcription_result.get('segments', [])
        total_segments = len(segments)
        batch_size = 15 # Reduced to prevent timeout 
        
        SCRIPT_MAP = {
            'Telugu': 'Telugu (తెలుగు)',
            'Tamil': 'Tamil (தமிழ்)',
            'Hindi': 'Hindi (हिंदी)',
            'Kannada': 'Kannada (ಕನ್ನಡ)',
            'Malayalam': 'Malayalam (മലയാളം)',
            'English': 'English (Latin script)'
        }
        target_script = SCRIPT_MAP.get(target_language, target_language)

        safe_print(f"💎 [SYNTHESIS] Processing {total_segments} segments for {target_language}...", flush=True)

        try:
            full_text = transcription_result.get('text', '')
            text_for_summary = full_text[len(full_text)//4 : len(full_text)//4 + 15000] if len(full_text) > 20000 else full_text[:15000]
            
            summary_prompt = f"Act as a Senior Executive. Summarize this transcript in 3 clean, high-impact bullet points (English):\n\n{text_for_summary}"
            summary_res = self._generate_with_retry(summary_prompt)
            if summary_res and summary_res.text: 
                summary = summary_res.text.strip()
        except Exception as e:
            safe_print(f"      ⚠️ Summary failed: {e}", flush=True)

        for i in range(0, total_segments, batch_size):
            batch = segments[i : i + batch_size]
            # Just send the text with ID
            indexed_batch_text = "\n".join([f"{j} | {s['text']}" for j, s in enumerate(batch)])
            
            safe_print(f"   ⏳ [BATCH] {int(i/batch_size) + 1} / {int((total_segments-1)/batch_size) + 1}", flush=True)
            
            prompt = f"""You are the AURA Multilingual Engine.
TASK: Translate the segments below from {source_language} to {target_script}.

STRICT REQUIREMENTS:
1. TRANSLATE the content. Do NOT just copy the English text.
2. OUTPUT FORMAT: Pipe-delimited list (ID | TRANSLATED_TEXT).
3. NO JSON, NO MARKDOWN, NO EXPLANATIONS.
4. Keep the same ID for each segment.

Input format: ID | Source Text
------------------------------
{indexed_batch_text}
------------------------------

Output (ID | Translated Text):
"""
            try:
                response = self._generate_with_retry(prompt)
                res_text = response.text if response and response.text else ""
                
                # Use the new pipe parser
                lang_map = self._parse_pipe_delimited_translations(res_text)

                for j, s in enumerate(batch):
                    translated_text = lang_map.get(j, s['text'])
                    # Normalize for comparison
                    is_trans = translated_text.strip().lower() != s['text'].strip().lower()
                    
                    all_synced_segments.append({
                        'id': s.get('id', f"seg-{i + j}"),
                        'start': s['start'],
                        'end': s['end'],
                        'text': translated_text,
                        'original': s['text'],
                        'is_translated': is_trans
                    })

            except Exception as e:
                safe_print(f"      ⚠️ Gemini Batch Failure: {e}", flush=True)
                for j, s in enumerate(batch):
                    all_synced_segments.append({
                        **s,
                        'id': s.get('id', f"seg-{i+j}"),
                        'original': s['text'],
                        'is_translated': False
                    })

        translated_segments_text = [seg['text'] for seg in all_synced_segments]
        cleaned_body = " ".join(translated_segments_text)
        
        return {
            'raw_transcript': transcription_result.get('text', ''),
            'cleaned_transcript': cleaned_body,
            'segments': all_synced_segments,
            'translations': {target_language.lower(): cleaned_body},
            'summary': summary,
            'engine': 'AssemblyAI Universal-2'
        }

    def full_pipeline(self, audio_path: str, language: str, target_language: str = "Tamil", use_gemini: bool = True) -> dict:
        """The Main Pipeline Entry Point"""
        safe_print(f"🔥 [PIPELINE] Starting | Src: {language} | Tgt: {target_language}", flush=True)
        transcription_result = self.transcribe_audio(audio_path, language)

        if use_gemini and self.gemini_api_key:
            return self.perform_gemini_synthesis(transcription_result, language, target_language)
        else:
            return {
                'raw_transcript': transcription_result['text'],
                'segments': transcription_result['segments'],
                'words': transcription_result.get('words', []),
                'summary': "Transcription completed without AI post-processing.",
                'engine': 'AssemblyAI Universal-2'
            }
