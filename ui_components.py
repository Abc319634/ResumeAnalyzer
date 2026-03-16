import streamlit as st

def apply_custom_css():
    # Detect theme preference from session state
    if 'theme' not in st.session_state:
        st.session_state.theme = "Light"
        
    # High-contrast color palette to avoid white-on-white
    if st.session_state.theme == "Light":
        theme_bg = "#f0f2f6"
        card_bg = "#ffffff"
        text_color = "#121212"
        sub_text = "#4a4a4a"
        border_color = "#d1d5db"
    else:
        theme_bg = "#0e1117"
        card_bg = "#1e212b"
        text_color = "#fafafa"
        sub_text = "#bcbcbc"
        border_color = "#3d4b5c"

    accent_color = "#4f46e5"

    st.markdown(f"""
        <style>
        /* Force text colors site-wide to prevent white-on-white */
        .stApp, .stApp p, .stApp div, .stApp span, .stApp label {{
            color: {text_color} !important;
        }}
        
        .stApp {{
            background-color: {theme_bg} !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {card_bg} !important;
        }}
        
        [data-testid="stSidebar"] * {{
            color: {text_color} !important;
        }}

        .card {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            color: {text_color} !important;
        }}
        
        .card h3, .card div {{
            color: {text_color} !important;
        }}

        /* Buttons need white text regardless of theme for contrast */
        .stButton>button {{
            background-color: {accent_color} !important;
            color: white !important;
            border: none;
            border-radius: 8px;
            font-weight: bold;
        }}

        /* Fix visibility for info/success/warning boxes */
        div[data-testid="stNotification"] {{
            background-color: {card_bg} !important;
            border: 1px solid {border_color} !important;
        }}
        
        div[data-testid="stNotification"] p {{
            color: {text_color} !important;
        }}

        /* Fix visibility for input labels */
        .stTextInput label, .stTextArea label, .stSelectbox label, .stFileUploader label {{
            color: {text_color} !important;
            font-weight: 600 !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def card(title, content):
    st.markdown(f"""
        <div class="card">
            <h3 style="margin-top:0; color:#4f46e5 !important;">{title}</h3>
            <div style="line-height: 1.6;">{content}</div>
        </div>
    """, unsafe_allow_html=True)

def score_display(score):
    color = "#059669" if score > 70 else "#d97706" if score > 40 else "#dc2626"
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; margin: 10px 0;">
            <div style="font-size: 4rem; font-weight: 800; color: {color} !important;">{score}%</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #4b5563 !important;">COMPATIBILITY SCORE</div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(score / 100)

def section_header(title, icon=None):
    st.markdown(f"""
        <div style="border-bottom: 2px solid #edeff3; margin-bottom: 20px; padding-bottom: 5px;">
            <h2 style="margin: 0;">{icon if icon else ''} {title}</h2>
        </div>
    """, unsafe_allow_html=True)
