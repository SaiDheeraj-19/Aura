# 🎙️ AURA

A professional-grade Streamlit application for extracting audio from videos and providing high-accuracy transcripts in **Telugu, Tamil, English, Malayalam, Hindi, and Kannada**. Optimized for speed and quality using cloud-based AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Features

- **🎬 Dual Input Support**
  - Upload local video files (MP4, AVI, MOV, MKV, etc.)
  - Process YouTube videos via URL

- **🎯 High-Accuracy Transcription**
  - Powered by **AssemblyAI Universal-2**
  - High-speed cloud processing
  - Multi-language support with native script output

- **✨ AI Post-Processing**
  - Grammar and punctuation correction via **Google Gemini 1.5 Flash**
  - Automatic executive summarization
  - Multi-language regional translations

- **🌐 Multi-Language Support**
  - Telugu (తెలుగు)
  - Tamil (தமிழ்)
  - English
  - Malayalam (മലയാളം)
  - Hindi (హిन्दी)
  - Kannada (ಕನ್ನಡ)

- **📥 Export Options**
  - Download high-fidelity transcripts (.md)
  - Fully synchronized segments view

## 🏗️ Project Structure

```
AURA/
│
├── app.py                      # Main Streamlit application
├── engine.py                   # Core AURA Synthesis Engine
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
│
├── utils/
│   ├── __init__.py
│   ├── audio_extractor.py     # Flux Transit audio extraction
│   └── transcription_engine.py # AssemblyAI + Gemini pipeline
│
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system

### Installation

1. **Clone or navigate to the project directory:**

   ```bash
   cd AURA
   ```

2. **Run the setup script:**

   ```bash
   bash run.sh
   ```

3. **Set up environment variables:**
   Edit `.env` and add your API keys:

   ```env
   ASSEMBLYAI_API_KEY=your_aai_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Access the app:**
   Open your browser and navigate to `http://localhost:8501`

## 🔑 API Keys Setup

### AssemblyAI API Key
1. Sign up at [AssemblyAI](https://www.assemblyai.com/)
2. Get your API key from the dashboard

### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Create a new API key

## 🛠️ Tech Stack

| Component            | Technology                          |
| -------------------- | ----------------------------------- |
| **Frontend**         | Streamlit                           |
| **Audio Extraction** | yt-dlp, FFmpeg (Flux Transit)       |
| **Transcription**    | AssemblyAI Universal-2              |
| **Post-Processing**  | Google Gemini 1.5 Flash             |

## ⚡ Performance Optimization

- **Cloud-First:** Eliminates local model loading bottlenecks.
- **Flux Transit:** Optimized YouTube audio streaming extraction.
- **Gemini Super-Pass:** High-speed cleaning and translation in a single pass.

---

**Built with ❤️ for Indian Language Accessibility**
