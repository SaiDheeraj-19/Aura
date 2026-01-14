import streamlit as st

def apply_obsidian_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;700&family=JetBrains+Mono:wght@300;500&display=swap');
        
        /* Premium Icon Support */
        @import url('https://cdn.jsdelivr.net/npm/lucide-static@0.321.0/font/lucide.min.css');

        /* Base Obsidian Black Theme with Overlay for Clarity */
        .stApp {
            background-color: #050505;
            color: #ffffff;
            font-family: 'Inter', sans-serif;
        }
        
        /* Darkening Overlay for readability */
        .stApp::after {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.6);
            pointer-events: none;
            z-index: 0;
        }

        /* Grainy Overlay */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://grainy-gradients.vercel.app/noise.svg');
            opacity: 0.05;
            pointer-events: none;
            z-index: 9999;
        }

        /* Ensure content is above overlay */
        .stMain, .stHeader, [data-testid="stSidebar"] {
            position: relative;
            z-index: 1;
        }
        
        /* Premium Icon Styling */
        .premium-icon {
            display: inline-block;
            vertical-align: middle;
            margin-right: 12px;
            font-size: 1.2rem;
            opacity: 0.8;
        }
        
        /* AURA Title Styling */
        .aura-title {
            font-family: 'Inter', sans-serif;
            font-weight: 300;
            font-size: 6rem;
            letter-spacing: 12px;
            text-align: center;
            background: linear-gradient(to bottom, #ffffff, #333333);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            text-shadow: 0 0 30px rgba(255, 255, 255, 0.1);
        }
        
        .aura-subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.6rem;
            text-align: center;
            color: #888;
            letter-spacing: 8px;
            text-transform: uppercase;
            margin-bottom: 4rem;
            opacity: 0.8;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        /* Shimmering Status Orb Animation - Refined */
        .orb-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 60vh;
        }
        
        .aura-loader {
            position: relative;
            width: 200px;
            height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 4rem;
        }
        
        .aura-loader::before, .aura-loader::after {
            content: "";
            position: absolute;
            border-radius: 50%;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .aura-loader::before {
            width: 100%;
            height: 100%;
            animation: rotate-aura 10s linear infinite;
            border-top-color: rgba(255, 255, 255, 0.8);
        }
        
        .aura-loader::after {
            width: 80%;
            height: 80%;
            animation: rotate-aura 5s linear reverse infinite;
            border-bottom-color: rgba(255, 255, 255, 0.4);
        }
        
        .status-orb {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: #fff;
            filter: blur(8px);
            animation: pulse-glow 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            z-index: 2;
        }
        
        @keyframes rotate-aura {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        @keyframes pulse-glow {
            0%, 100% { transform: scale(1); opacity: 0.3; box-shadow: 0 0 40px rgba(255,255,255,0.2); }
            50% { transform: scale(1.5); opacity: 1; box-shadow: 0 0 100px rgba(255,255,255,0.5); }
        }
        
        .loading-text {
            color: #ffffff;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            letter-spacing: 8px;
            text-transform: uppercase;
            text-align: center;
            animation: text-fade 2s ease-in-out infinite;
        }
        
        @keyframes text-fade {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }
        
        /* Custom Buttons - Hollow/Minimalist */
        .stButton>button {
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 0px;
            padding: 1rem 3rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            letter-spacing: 2px;
            transition: all 0.5s cubic-bezier(0.19, 1, 0.22, 1);
            width: 100%;
            text-transform: uppercase;
            backdrop-filter: blur(10px);
        }
        
        .stButton>button:hover {
            background: #ffffff;
            color: #000000;
            border-color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        }
        
        /* Input fields */
        .stTextInput>div>div>input {
            background-color: rgba(255, 255, 255, 0.03);
            color: white;
            border-radius: 0px;
            border: none;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem 1rem;
            font-size: 1rem;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 2px;
            transition: all 0.3s ease;
            text-transform: uppercase;
        }
        
        .stTextInput>div>div>input::placeholder {
            color: rgba(255, 255, 255, 0.3) !important;
            letter-spacing: 4px;
        }
        
        .stTextInput>div>div>input:focus {
            border-bottom-color: #ffffff;
            background-color: rgba(255, 255, 255, 0.05);
            box-shadow: none;
        }
        
        /* Tab styling - Hidden or highly minimal */
        .stTabs [data-baseweb="tab-list"] {
            gap: 40px;
            background-color: transparent;
            justify-content: center;
            margin-bottom: 2rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            color: #666;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #aaa;
        }
        
        .stTabs [aria-selected="true"] {
            color: #fff !important;
            border-bottom: 2px solid #fff !important;
        }
        
        /* Success/Error/Expander styling */
        .stAlert {
            background-color: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #eee;
            border-radius: 0px;
            backdrop-filter: blur(10px);
        }

        .streamlit-expanderHeader {
            background-color: transparent !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 0px !important;
        }

        /* Metrics Styling */
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem !important;
            letter-spacing: -1px;
        }
        [data-testid="stMetricLabel"] {
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #888 !important;
        }

        /* Hide Streamlit elements */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        [data-testid="stDecoration"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

def show_status_orb(text="RECONSTRUCTING INTELLIGENCE"):
    st.markdown(f"""
        <div class="orb-container">
            <div class="aura-loader">
                <div class="status-orb"></div>
            </div>
            <div class="loading-text">
                {text}
            </div>
        </div>
    """, unsafe_allow_html=True)
