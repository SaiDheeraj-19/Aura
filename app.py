import streamlit as st
import os
import time
import json
import re
from dotenv import load_dotenv
from styles import apply_obsidian_theme, show_status_orb
from engine import AURAEngine
import streamlit.components.v1 as components

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AURA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Engine
if 'engine' not in st.session_state:
    st.session_state.engine = AURAEngine()

# Initialize State Machine
if 'state' not in st.session_state:
    st.session_state.state = "LAUNCHER"
if 'master_data' not in st.session_state:
    st.session_state.master_data = None

# Apply Theme
apply_obsidian_theme()

# Set Background Image
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/render/image/public/project-uploads/b7dadfea-2c17-4751-89cb-042194a1f545/Gemini_Generated_Image_ec9qsjec9qsjec9q-1767806111889.jpeg?width=8000&height=8000&resize=contain");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def set_state(state):
    st.session_state.state = state
    st.rerun()


# --- UI State: LAUNCHER ---
if st.session_state.state == "LAUNCHER":
    st.markdown("<h1 class='aura-title'>AURA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='aura-subtitle'>MULTILINGUAL TRANSCRIBER</p>", unsafe_allow_html=True)
    
    # Using emojis for "premium" feel as Streamlit tabs don't support raw HTML labels
    tab1, tab2 = st.tabs(["📺 YOUTUBE", "📁 LOCAL"])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🚀 AI-DRIVEN CLOUD TRANSCRIPTION (ASSEMBLYAI)")
        model_choice = "ASSEMBLY AI (CLOUD)"
    with col2:
        language_choice = st.selectbox("SOURCE LANGUAGE", ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"], index=0)
    with col3:
        target_language_choice = st.selectbox("TARGET LANGUAGE", ["Tamil", "Telugu", "Hindi", "Kannada", "Malayalam", "English"], index=0)
    
    source_type = None
    source_value = None
    
    with tab1:
        video_url = st.text_input("Enter Video URL", placeholder="PASTE YOUTUBE / WEB URL", key="url_input", label_visibility="collapsed")
        if video_url:
            source_type = "url"
            source_value = video_url
            
    with tab2:
        uploaded_file = st.file_uploader("UPLOAD MEDIA", type=["mp4", "mkv", "mov", "avi"], key="file_input", label_visibility="collapsed")
        if uploaded_file:
            source_type = "local"
            source_value = uploaded_file
            
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.button("L A U N C H"):
        if source_value:
            st.session_state.source_type = source_type
            st.session_state.source_value = source_value
            st.session_state.model_choice = model_choice
            st.session_state.language_choice = language_choice
            st.session_state.target_language = target_language_choice
            set_state("PROCESSING")
        else:
            st.warning("PLEASE PROVIDE A MEDIA SOURCE")
            
# --- UI State: PROCESSING ---
elif st.session_state.state == "PROCESSING":
    status_container = st.empty()
    
    try:
        # Step 1: Extraction
        with status_container:
            show_status_orb("EXTRACTING AUDIO...")
            
        if st.session_state.source_type == "url":
            extraction_result = st.session_state.engine.extract_audio_from_url(st.session_state.source_value)
        else:
            extraction_result = st.session_state.engine.extract_audio_from_local(st.session_state.source_value)
            
        if not extraction_result or 'path' not in extraction_result:
            raise Exception("FAILED TO EXTRACT AUDIO")
            
        # Step 2: Integrated Transcription & Translation
        with status_container:
            show_status_orb("TRANSCRIBING AUDIO (CLOUD)...")
            
        # Use SMART TRANSCRIBE (with automatic fallback for URL errors)
        transcription_data = st.session_state.engine.smart_transcribe(
            extraction_result, 
            language=st.session_state.language_choice
        )
        
        with status_container:
            show_status_orb("SYNTHESIZING MULTILINGUAL SOUL (GEMINI)...")
            
        master_data = st.session_state.engine.unified_multilingual_pipeline_from_result(
            transcription_data,
            source_language=st.session_state.language_choice,
            target_language=st.session_state.target_language
        )
        
        st.session_state.master_data = master_data
        
        # Cleanup temp audio (if it's a local file)
        audio_path = extraction_result.get('path')
        if not extraction_result.get('is_url') and audio_path and os.path.exists(audio_path):
            try:
                os.remove(audio_path)
            except:
                pass
            
        with status_container:
            show_status_orb("COMPLETED")
        time.sleep(1.5)
        set_state("READY")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        error_msg = str(e)
        
        if "TIMED OUT" in error_msg.upper():
            st.error(f"⌛ EXTRACTION TIMED OUT: {error_msg}. THE SOURCE MIGHT BE TOO LARGE OR THE NETWORK IS UNSTABLE.")
        else:
            st.error(f"🚨 PIPELINE INTERRUPTED: {error_msg}")
            
        if st.button("RETURN TO LAUNCHER"):
            set_state("LAUNCHER")

# --- UI State: READY ---
elif st.session_state.state == "READY":
    st.markdown("<h1 class='aura-title'>AURA</h1>", unsafe_allow_html=True)
    st.markdown("<p class='aura-subtitle'>INTELLIGENCE SYNTHESIS COMPLETE</p>", unsafe_allow_html=True)
    
    data = st.session_state.master_data
    
    # Dashboard Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("SOURCE LANGUAGE", data['master_metadata']['source_language'].upper())
    with m2:
        st.metric("TARGET LANGUAGE", st.session_state.get('target_language', 'TAMIL').upper(), "TRANSLATED")
    with m3:
        st.metric("PROCESSING TIME", f"{data['master_metadata']['duration_sec']}s")
    with m4:
        st.metric("PIPELINE STATUS", data['master_metadata']['status'].upper())

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Premium Tabs
    res_tab1, res_tab2, res_tab3, res_tab4 = st.tabs([
        "💎 SUMMARY", 
        "🌐 CONSENSUS", 
        "📜 SCRIPT",
        "🧠 METRICS"
    ])
    
    with res_tab1:
        st.markdown("<h3 style='letter-spacing: 2px; color: #888;'>EXECUTIVE BRIEFING</h3>", unsafe_allow_html=True)
        # Handle bullet points from new Gemini summary
        summary_text = data.get('summary', 'Synthesis complete.')
        if "\n" in summary_text:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.03); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05); margin: 1rem 0;">
                <div style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; line-height: 1.8; color: #fff;">
                    {summary_text.replace('\n', '<br>')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 2rem; border-left: 4px solid #fff; margin: 1rem 0;">
                <p style="font-family: 'Outfit', sans-serif; font-size: 1.1rem; line-height: 1.6; color: #eee;">
                    {summary_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
    with res_tab2:
        st.markdown("<h3 style='letter-spacing: 2px; color: #888;'>MULTILINGUAL SOUL</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); padding: 2rem; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
            <p style="font-size: 1.2rem; line-height: 1.8; color: #ccc;">{data['synthesis']['consensus_transcript']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with res_tab3:
        # --- SYNCHRONIZED PLAYER & TRANSCRIPT ---
        segments = data['cloud_module'].get('segments', [])
        
        # Determine Video Source for Player
        video_src = st.session_state.get('source_value')
        source_type = st.session_state.get('source_type', 'url')

        # Prepare Segments for Frontend
        processed_segments = []
        for i, s in enumerate(segments):
            processed_segments.append({
                'id': f"seg-{i + 1}",
                'start': s['start'],
                'end': s['end'],
                'text': s['text'],
                'original': s.get('original', ''),
                'is_translated': s.get('is_translated', False)
            })

        st.markdown('<div class="theater-mode">', unsafe_allow_html=True)
        col_left, col_right = st.columns([1, 1], gap="large")
        
        with col_left:
            st.markdown('<div class="live-status"><div class="status-dot"></div> AURA REAL-TIME SYNC</div>', unsafe_allow_html=True)
            st.markdown('<div class="video-wrapper">', unsafe_allow_html=True)
            
            # --- CEO FIX: Official YouTube Player API Integration ---
            video_id = ""
            if source_type == "url":
                yt_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", video_src)
                if yt_id_match:
                    video_id = yt_id_match.group(1)
            
            if video_id:
                # 1. Direct Iframe Injection (Visible immediately) + API Target
                st.markdown(f"""
                <script src="https://www.youtube.com/iframe_api"></script>
                <iframe id="aura-player-target" 
                        width="100%" 
                        height="450" 
                        src="https://www.youtube.com/embed/{video_id}?enablejsapi=1&rel=0&playsinline=1" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen 
                        style="border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                </iframe>
                """, unsafe_allow_html=True)
            else:
                st.video(video_src)
                
            st.markdown('</div>', unsafe_allow_html=True)
                
        with col_right:
            # --- CONSOLIDATED PREMIUM TRANSCRIPT COMPONENT ---
            transcript_items_html = ""
            for i, seg in enumerate(processed_segments):
                seg_id = f"seg-{i + 1}"
                original_text = seg.get('original', '')
                translated_text = seg.get('text', '')
                
                # If they are different, we show both. 
                has_original = original_text and original_text.strip().lower() != translated_text.strip().lower()

                transcript_items_html += f"""
                <div class="segment" id="{seg_id}" onclick="seekPlayer({seg['start']/1000})">
                    <div class="timestamp">⏱️ {seg['start'] / 1000:.2f}s</div>
                    {f'<div class="original-text">{original_text}</div>' if has_original else ""}
                    <div class="translated-text">{translated_text}</div>
                </div>
                """

            component_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600&display=swap" rel="stylesheet">
                <style>
                    body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; font-family: 'Outfit', sans-serif; }}
                    
                    /* Scrollbar */
                    ::-webkit-scrollbar {{ width: 8px; }}
                    ::-webkit-scrollbar-track {{ background: rgba(0,0,0,0.3); }}
                    ::-webkit-scrollbar-thumb {{ background: #333; border-radius: 4px; }}
                    ::-webkit-scrollbar-thumb:hover {{ background: #555; }}

                    .transcript-container {{
                        height: 600px;
                        overflow-y: auto;
                        padding: 20px 30px;
                        background: #090909;
                        border-radius: 12px;
                        border: 1px solid #222;
                    }}
                    
                    .segment {{
                        padding: 20px;
                        margin-bottom: 15px;
                        border-radius: 8px;
                        border-left: 3px solid transparent;
                        opacity: 0.5;
                        transition: all 0.2s ease-out;
                        cursor: pointer;
                    }}
                    .segment:hover {{ opacity: 0.8; background: #111; }}
                    
                    .segment.active {{
                        opacity: 1;
                        background: #151515;
                        border-left: 3px solid #00E676; /* Bright Green */
                        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                    }}
                    
                    .timestamp {{ font-family: monospace; font-size: 11px; color: #555; margin-bottom: 5px; }}
                    .original-text {{ font-size: 14px; color: #888; margin-bottom: 5px; line-height: 1.4; }}
                    .translated-text {{ font-size: 20px; color: #ccc; font-weight: 500; line-height: 1.4; }}
                    .active .translated-text {{ color: #fff; }}
                    
                    .debug-badge {{
                        position: fixed; top: 10px; right: 20px;
                        background: rgba(0,0,0,0.8); color: #0f0;
                        font-family: monospace; font-size: 10px; padding: 4px 8px;
                        border-radius: 4px; pointer-events: none; z-index: 999;
                    }}
                </style>
            </head>
            <body>
                <div class="debug-badge" id="debug">waiting...</div>
                <div class="transcript-container" id="scroller">
                    <div style="padding: 20px 0; border-bottom: 1px solid #333; margin-bottom: 20px;">
                        <h2 style="color: #fff; margin:0;">{st.session_state.get('target_language', 'TAMIL').upper()} SCRIPT</h2>
                    </div>
                    {transcript_items_html}
                    <div style="height: 300px;"></div> <!-- Pad for bottom scrolling -->
                </div>

                <script>
                    const segments = {json.dumps(processed_segments)};
                    const debug = document.getElementById('debug');
                    const scroller = document.getElementById('scroller');
                    let lastActiveId = null;
                    let isUserScrolling = false;
                    let scrollTimeout = null;

                    // Manual Scroll Detection
                    scroller.addEventListener('scroll', () => {{
                        isUserScrolling = true;
                        if(scrollTimeout) clearTimeout(scrollTimeout);
                        scrollTimeout = setTimeout(() => isUserScrolling = false, 3000);
                    }});

                    window.seekPlayer = function(sec) {{
                        isUserScrolling = false;
                        // Send seek command to parent window logic involves YouTube API
                        window.top.postMessage({{ type: 'seek', time: sec }}, '*');
                    }};

                    window.addEventListener('message', (e) => {{
                        if (e.data && e.data.type === 'aura_sync') {{
                            const t = e.data.time / 1000;
                            debug.textContent = `SYNC: ${{t.toFixed(1)}}s`;
                            highlight(t);
                        }}
                    }});

                    function highlight(timeSec) {{
                        // Find active segment
                        let activeId = null;
                        for(let segment of segments) {{
                            // Slightly loose matching for audio drift
                            if (timeSec >= (segment.start/1000 - 0.2) && timeSec < (segment.end/1000 + 0.5)) {{
                                activeId = segment.id;
                                break;
                            }}
                        }}

                        if (activeId && activeId !== lastActiveId) {{
                            lastActiveId = activeId;
                            
                            // DOM Update
                            document.querySelectorAll('.segment.active').forEach(el => el.classList.remove('active'));
                            const el = document.getElementById(activeId);
                            
                            if (el) {{
                                el.classList.add('active');
                                if (!isUserScrolling) {{
                                    el.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                                }}
                            }}
                        }}
                    }}
                </script>
            </body>
            </html>
            """
            components.html(component_html, height=650)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- CEO FIX: GLOBAL MASTER CONTROLLER ---
        # This script runs in the MAIN WINDOW and controls the YouTube API & Transcript Component
        if video_id:
            st.markdown(f"""
            <script>
                // 1. YouTube API Boilerplate
                var player;
                var auraSyncInterval = null;

                // Wait for API to load
                if (typeof YT === 'undefined' || typeof YT.Player === 'undefined') {{
                    var tag = document.createElement('script');
                    tag.src = "https://www.youtube.com/iframe_api";
                    var firstScriptTag = document.getElementsByTagName('script')[0];
                    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                }}

                function onYouTubeIframeAPIReady() {{
                    console.log("AURA: YT API Ready, attaching to iframe...");
                    player = new YT.Player('aura-player-target', {{
                        events: {{
                            'onReady': onPlayerReady
                        }}
                    }});
                }}
                
                // Fallback: If API already ready
                if (window.YT && window.YT.Player) {{
                    onYouTubeIframeAPIReady();
                }}

                function onPlayerReady(event) {{
                    console.log("AURA: Player Connected!");
                    startSync();
                }}
                
                function startSync() {{
                    if (auraSyncInterval) clearInterval(auraSyncInterval);
                    auraSyncInterval = setInterval(() => {{
                        if (player && player.getCurrentTime) {{
                            const t = player.getCurrentTime();
                            broadcast(t * 1000);
                        }}
                    }}, 100); // 10Hz Broadcast
                }}

                function broadcast(timeMs) {{
                    // Send to all stream-component iframes (Transcript)
                    const iframes = document.querySelectorAll('iframe');
                    iframes.forEach(iframe => {{
                        try {{
                            iframe.contentWindow.postMessage({{
                                type: 'aura_sync',
                                time: timeMs
                            }}, '*');
                        }} catch(e) {{}}
                    }});
                }}

                // Listen for Seek Requests from Transcript
                window.addEventListener('message', (e) => {{
                    if (e.data && e.data.type === 'seek') {{
                        if (player && player.seekTo) {{
                            player.seekTo(e.data.time, true);
                            player.playVideo();
                        }}
                    }}
                }});
            </script>
            """, unsafe_allow_html=True)


    with res_tab4:
        st.json(data)

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("NEW SESSION"):
            st.session_state.master_data = None
            set_state("LAUNCHER")
    with col_b:
        transcript_text = data['synthesis']['consensus_transcript']
        st.download_button(
            label="DOWNLOAD TRANSCRIPT (MD)",
            data=f"# AURA TRANSCRIPT\n\n## Summary\n{data.get('summary', '')}\n\n## Transcript\n{transcript_text}",
            file_name=f"aura_transcript_{int(time.time())}.md",
            mime="text/markdown"
        )
        
# --- END OF APP ---
