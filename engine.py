import os
from dotenv import load_dotenv
from utils.transcription_engine import AssemblyAITranscriber
from utils.audio_extractor import AudioExtractor

load_dotenv()

class AURAEngine:
    def _log(self, msg):
        try:
            print(msg)
        except (BrokenPipeError, IOError):
            pass

    def __init__(self):
        self._log("🧠 [AURAEngine] Initializing...")
        self.aai_key = os.getenv("ASSEMBLYAI_API_KEY")
        self.gemini_key = os.getenv("GEMINI_API_KEY")
        self.extractor = AudioExtractor()

        # Initialize transcribers lazily or with checks
        self.aai_engine = None
        if self.aai_key:
            self._log("   ☁️ Initializing AssemblyAI...")
            self.aai_engine = AssemblyAITranscriber(self.aai_key, self.gemini_key)

        self._log("✅ [AURAEngine] Ready.")

    def extract_audio_from_url(self, url):
        """
        Smart Extraction: Returns a dict with 'path' and 'is_url'.
        Tries to resolve direct stream URL first for speed.
        """
        if "youtube.com" in url or "youtu.be" in url:
            try:
                self._log(f"📡 [SPEED-ROUTE] Attempting Direct Stream resolution for: {url}")
                direct_url = self.extractor.get_direct_audio_url(url)
                return {"path": direct_url, "is_url": True, "original_url": url}
            except Exception as e:
                self._log(f"⚠️ Direct URL resolution failed: {e}. Falling back to high-quality download.")
        
        local_path = self.extractor.extract_from_youtube(url)
        return {"path": local_path, "is_url": False, "original_url": url}

    def extract_audio_from_local(self, video_file):
        """Extracts audio from a local video file with secure temp handling."""
        import uuid
        session_id = str(uuid.uuid4())[:8]
        temp_path = os.path.join(self.extractor.temp_dir, f"input_{session_id}.media")
        
        try:
            with open(temp_path, "wb") as f:
                f.write(video_file.getbuffer())
            local_path = self.extractor.extract_from_file(temp_path)
            # We can delete the uploaded video immediate after extraction to save space
            if os.path.exists(temp_path): os.remove(temp_path)
            return {"path": local_path, "is_url": False}
        except Exception as e:
            if os.path.exists(temp_path): os.remove(temp_path)
            raise e

    def smart_transcribe(self, extraction_result, language="English"):
        """
        Transcribes with an automatic fallback if Direct URL fails.
        Top-Tier Developer Logic: Proactively handles cloud download errors.
        """
        path = extraction_result['path']
        is_url = extraction_result.get('is_url', False)
        
        try:
            self._log(f"☁️ [TRANSCRIPTION] Starting (Source: {'Cloud Stream' if is_url else 'Local Buffer'})")
            return self.aai_engine.transcribe_audio(path, language)
        except Exception as e:
            # If AssemblyAI fails to reach the direct URL (e.g. 403 or 404 from YT)
            if is_url and any(err in str(e).lower() for err in ["download", "403", "forbidden", "reach", "accessible"]):
                self._log("🚨 [FALLBACK] Cloud direct-access blocked. Switching to local tunnel extraction...")
                local_data = self.extractor.extract_from_youtube(extraction_result['original_url'])
                self._log("✅ [FALLBACK] Local tunnel successful. Retrying transcription...")
                return self.aai_engine.transcribe_audio(local_data, language)
            else:
                raise e

    def unified_multilingual_pipeline_from_result(self, transcription_result, source_language="English", target_language="Tamil", start_time=None):
        """
        Synthesis phase: Post-processes raw AAI transcription through Gemini.
        Returns the MASTER JSON for the UI.
        """
        import time
        from datetime import datetime
        if start_time is None: start_time = time.time()
        
        self._log(f"🌌 [SYNTHESIS] Merging Multilingual Intelligence (Target: {target_language})...")

        # Refactor: Call the Gemini logic from aAI engine
        cloud_result = self.aai_engine.perform_gemini_synthesis(transcription_result, source_language, target_language)
        
        # Master JSON Construction
        master_json = {
            "master_metadata": {
                "timestamp": datetime.now().isoformat(),
                "duration_sec": round(time.time() - start_time, 2),
                "source_language": source_language,
                "target_language": target_language,
                "status": "completed",
                "engine": "AURA-V2-CLOUD"
            },
            "summary": cloud_result.get('summary', 'Synthesis complete.'),
            "cloud_module": cloud_result,
            "synthesis": {
                "consensus_transcript": cloud_result.get('cleaned_transcript', ''),
                "multilingual_expansion": cloud_result.get('translations', {})
            }
        }
        
        self._log(f"✅ [SYNTHESIS] Pipeline Complete in {time.time() - start_time:.1f}s")
        return master_json

