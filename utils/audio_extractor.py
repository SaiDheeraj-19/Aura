"""
Audio extraction utilities for AURA
Handles YouTube downloads and local file audio extraction with 16kHz mono conversion
"""

import os
import time
import tempfile
import yt_dlp
import subprocess

def safe_print(*args, **kwargs):
    try:
        print(*args, **kwargs)
    except (BrokenPipeError, IOError):
        pass


class AudioExtractor:
    """Extract and preprocess audio from YouTube URLs or local video files"""
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
    
    def get_direct_audio_url(self, url: str) -> str:
        """
        Get direct audio stream URL from YouTube without downloading/processing.
        TRUTH: This resolves the hidden URL so AssemblyAI can download it from YouTube's CDN directly.
        """
        try:
            # FORTRESS MODE: Mimic Browser for max bypass
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'force_ipv4': True,
                'extract_flat': True,
                'socket_timeout': 15,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
            }
            
            # If the URL already looks like a direct stream URL
            if "googlevideo.com" in url or "manifest" in url:
                return url

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if not info or 'url' not in info:
                    raise Exception("yt-dlp could not find a stream URL")
                return info['url']
        except Exception as e:
            raise Exception(f"Failed to resolve YouTube URL: {str(e)}")

    def extract_from_youtube(self, url: str, raw: bool = False) -> str:
        """
        Extract audio from YouTube URL and convert to 16kHz mono WAV.
        OPTIMIZED: Faster format selection, robust streaming flags, and smart timeouts.
        """
        output_path = os.path.join(self.temp_dir, "youtube_audio.wav")
        
        # Custom Logger to capture yt-dlp output
        class MyLogger:
            def debug(self, msg):
                if not msg.startswith('[debug] '):
                    safe_print(f"    [yt-dlp] {msg}")

            def warning(self, msg):
                safe_print(f"    [yt-dlp WARNING] {msg}")

            def error(self, msg):
                safe_print(f"    [yt-dlp ERROR] {msg}")

        try:
            safe_print(f"🎵 [EXTRACT] Processing URL: {url}")
            
            # 1. METADATA PRE-CHECK
            # We first check if the video is too long or is a live stream to avoid hanging forever.
            safe_print("🔍 [EXTRACT] Validating stream...", flush=True)
            pre_opts = {
                'quiet': True, 
                'extract_flat': True, 
                'socket_timeout': 5,
                'force_ipv4': True
            }
            with yt_dlp.YoutubeDL(pre_opts) as ydl:
                try:
                    info = ydl.extract_info(url, download=False)
                    duration = info.get('duration', 0)
                    is_live = info.get('is_live', False)
                    
                    if is_live:
                        safe_print("⚠️ [EXTRACT] Live stream detected. Limiting download to recent segment impossible in this mode - Checking direct stream support.")
                        # Implementing live stream download often hangs. We will try, but with strict controls.
                    
                    if duration and duration > 7200: # 2 hours
                        raise Exception("Video is too long (> 2 hours). Please use a shorter video.")
                        
                except Exception as e:
                    safe_print(f"⚠️ [EXTRACT] Metadata check warning: {e}. Proceeding with caution.")

            # 2. ROBUST DOWNLOAD
            temp_raw_path = os.path.join(self.temp_dir, "raw_download")
            downloaded_file = None
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    # Optional: Print progress every few seconds if needed
                    pass
                if d['status'] == 'finished':
                    safe_print("    [yt-dlp] Download complete.")

            ydl_opts = {
                'format': 'ba[abr<=128]/ba/worst',
                'outtmpl': temp_raw_path + ".%(ext)s",
                'logger': MyLogger(),
                'progress_hooks': [progress_hook],
                'noplaylist': True,
                'socket_timeout': 60, # Super-Hero Timeout
                'overwrites': True,
                'force_ipv4': True,
                'retries': 10,
                'fragment_retries': 10,
                'nocheckcertificate': True,
                'geo_bypass': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                },
            }

            safe_print("⏳ [EXTRACT] Starting Download (Optimized)...", flush=True)

            start_dl = time.time()
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                downloaded_file = ydl.prepare_filename(info)

            dl_time = time.time() - start_dl
            safe_print(f"✅ Downloaded raw file in {dl_time:.1f}s: {downloaded_file}")

            if not os.path.exists(downloaded_file):
                raise Exception("Download reported success but file is missing.")

            # 3. CONVERSION
            safe_print("⚡ Converting to standard 16kHz Mono WAV...")
            cmd = [
                'ffmpeg', '-y', '-nostdin', '-threads', '1',
                '-i', downloaded_file,
                '-vn', '-sn', '-dn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                output_path
            ]
            
            # Capture stderr for diagnostics
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=300)
            
            if process.returncode != 0:
                raise Exception(f"FFmpeg conversion failed: {stderr}")

            if os.path.exists(output_path):
                safe_print(f"✅ Conversion Complete: {output_path}")
                try:
                    os.remove(downloaded_file)
                except Exception:
                    pass
                return output_path
            else:
                raise Exception("Conversion produced no file")
                
        except subprocess.TimeoutExpired:
            raise Exception("Process timed out (FFmpeg conversion took too long).")
        except Exception as e:
            safe_print(f"❌ Extraction Failed: {str(e)}")
            raise e
            
    
    def extract_from_file(self, video_file_path: str) -> str:
        """
        Extract audio from uploaded video file and convert to 16kHz mono WAV
        """
        # Ensure input exists
        if not os.path.exists(video_file_path):
            raise Exception(f"Input file not found: {video_file_path}")

        output_path = os.path.join(self.temp_dir, f"extracted_{int(time.time())}.wav")
        
        try:
            safe_print(f"🎵 [EXTRACT] Extracting audio from: {video_file_path}")
            
            # Check for FFmpeg first
            try:
                subprocess.run(['ffmpeg', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except FileNotFoundError:
                raise Exception("FFmpeg not found in system path. Please install FFmpeg.")

            cmd = [
                'ffmpeg', '-y', '-nostdin', '-threads', '1', '-i', video_file_path,
                '-vn', '-sn', '-dn', '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1',
                output_path
            ]
            
            # Use subprocess directly for better control and error capture
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = process.communicate(timeout=300)
            
            if process.returncode != 0:
                safe_print(f"❌ FFmpeg Error (Code {process.returncode}): {stderr}")
                raise Exception(f"FFmpeg failed: {stderr}")
            
            if not os.path.exists(output_path):
                raise Exception("FFmpeg completed but output file is missing.")

            safe_print(f"✅ Audio extracted: {output_path}")
            return output_path
        except subprocess.TimeoutExpired:
            safe_print("❌ Extraction Timed Out (300s)")
            raise Exception("AUDIO EXTRACTION TIMED OUT")
        except Exception as e:
            # If it was a Signal 9, stderr might be empty, so we provide context
            if "died with <Signals.SIGKILL: 9>" in str(e):
                raise Exception("FFmpeg was killed by the system (SIGKILL 9). This usually happens due to extreme memory pressure or a corrupted video file. Try a smaller file or a different format.")
            raise Exception(f"Failed to extract audio from file: {str(e)}")
    
    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


def get_youtube_metadata(url: str, api_key: str = None) -> dict:
    """
    Fetch YouTube video metadata AND direct stream URL in one go.
    SPEED-OPTIMIZED: Uses tiny audio formats for AssemblyAI and direct info extraction.
    """
    import time
    start = time.time()
    metadata = {
        'title': 'Unknown',
        'thumbnail': None,
        'stream_url': None,
        'duration': 0
    }
    
    try:
        # Ultra-Aggressive yt-dlp flags for extreme speed
        ydl_opts = {
            'format': 'ba[abr<=64][ext=m4a]/ba[abr<=64]/wa/worst', 
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'force_ipv4': True,
            'extract_flat': True, # Flat extraction is near-instant
            'socket_timeout': 10,
            'youtube_include_dash_manifest': False,
            'youtube_include_hls_manifest': False,
            'playlist_items': '1',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            safe_print(f"📡 Resolving YouTube data for: {url}")
            info = ydl.extract_info(url, download=False)
            metadata['title'] = info.get('title', 'Unknown')
            metadata['thumbnail'] = info.get('thumbnail', None)
            metadata['stream_url'] = info.get('url', None)
            metadata['duration'] = info.get('duration', 0)
            safe_print(f"✅ Metadata & Stream resolved in {time.time() - start:.2f}s")
    
    except Exception as e:
        safe_print(f"❌ Failed to fetch metadata: {str(e)}")
    
    return metadata
