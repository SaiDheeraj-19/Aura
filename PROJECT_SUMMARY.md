# AURA — Project Summary

## 🎯 Project Overview

**AURA** is a professional Streamlit-based web application designed to extract audio from videos and generate high-accuracy transcripts in multiple Indian languages (Telugu, Tamil, English, Malayalam, Hindi, and Kannada). It utilizes high-speed cloud transcription via AssemblyAI and intelligent post-processing with Google Gemini.

## 🏗️ Architecture

### Component Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
│  (app.py - Premium AURA Interface)                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  Audio Extraction Layer                     │
│  - Flux Transit: yt-dlp / FFmpeg Optimized                  │
│  - 16kHz Mono Standardization                               │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Transcription Engine (Cloud)                   │
│  - Engine: AssemblyAI Universal-2                           │
│  - High Speed, Multi-Language Support                       │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           Synthesis & Refinement Layer                      │
│  - Google Gemini 1.5 Flash (Super-Pass)                     │
│  - Multilingual Translation & Executive Summary             │
└─────────────────────────────────────────────────────────────┘
```

## 📦 File Structure Explained

### Core Files

1. **app.py** (Main Application)
   - Streamlit UI implementation
   - User input handling (YouTube URL / file upload)
   - Integrated cloud pipeline orchestration
   - Result display with download functionality
   - Custom CSS styling for premium look

2. **engine.py**
   - `AURAEngine` class centralizing all logic
   - Coordinates extraction, transcription, and synthesis

3. **utils/audio_extractor.py**
   - `AudioExtractor` class for audio extraction
   - YouTube download via yt-dlp
   - Local file audio extraction via FFmpeg
   - Optimized for speed (Flux Transit)

4. **utils/transcription_engine.py**
   - `AssemblyAITranscriber` class
   - Integration with AssemblyAI SDK
   - Post-processing with Google Gemini 1.5 Flash

5. **requirements.txt**
   - All Python dependencies
   - Core: Streamlit, assemblyai, google-generativeai
   - Audio: yt-dlp, ffmpeg-python

## 🔄 Workflow Implementation

### User Flow:

1. User opens app → Selects source language
2. Chooses input: [YouTube URL] OR [Upload File]
3. Clicks "LAUNCH"
4. Backend Processing:
   ├── Extract audio (yt-dlp/ffmpeg)
   ├── Transcribe with AssemblyAI Cloud
   └── Post-process with Gemini (Clean, Summarize, Translate)
6. Display Results:
   ├── Executive Summary
   ├── Multilingual Consensus
   ├── Synchronized Script (Segments)
   └── Raw Data JSON

## 🚀 Performance Optimizations

1. **Cloud Transcription**
   - Offloads heavy processing to AssemblyAI servers
   - Eliminates local model loading bottlenecks

2. **Flux Transit Audio Extraction**
   - High-speed YouTube downloading and extraction
   - Optimized FFmpeg parameters for minimal latency

3. **Gemini Super-Pass**
   - Single API call for cleaning, summary, and translation
   - High-speed 1.5 Flash model for near-instant results

## 🔑 API Integration

### AssemblyAI (Transcription)
- **Model**: Universal-2
- **Purpose**: Fast, accurate transcription with word-level timing

### Google Gemini (Post-Processing)
- **Model**: gemini-1.5-flash
- **Purpose**: Clean transcripts, generate summaries, and provide regional translations

---

**Project Status**: ✅ Optimized (Local Bottlenecks Removed)
