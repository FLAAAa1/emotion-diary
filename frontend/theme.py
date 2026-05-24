'''Apply theme (light/dark), font size, and language via CSS and session state.'''
import streamlit as st

def load_and_apply():
    settings = st.session_state.get('_settings') or {}
    if not settings:
        try:
            from frontend.api import get_settings
            settings = get_settings()
            st.session_state['_settings'] = settings
        except Exception:
            settings = {}

    theme = settings.get('theme', 'light')
    font_size = settings.get('font_size', 14)
    lang = settings.get('language', 'zh')
    st.session_state['_lang'] = lang
    st.session_state['_theme'] = theme
    st.session_state['_font_size'] = font_size

    if theme == 'dark':
        bg = '#0e1117'; text = '#fafafa'; sidebar_bg = '#111'; input_bg = '#262730'
    else:
        bg = '#ffffff'; text = '#31333f'; sidebar_bg = '#f0f2f6'; input_bg = '#ffffff'

    css = ''
    css += '<style>'
    css += f'.stApp {{ background-color: {bg}; }}'
    css += f'.stApp,.stApp p,.stApp span,.stApp label,.stApp div,.stApp li {{ color: {text} !important; }}'
    css += f'.stApp .stTextInput>div>div>input,.stApp .stSelectbox>div>div>div,.stApp .stNumberInput>div>div>input {{ background-color: {input_bg} !important; color: {text} !important; }}'
    css += f'.stApp [data-testid=\"stSidebar\"] {{ background-color: {sidebar_bg} !important; }}'
    css += f'.stApp [data-testid=\"stSidebar\"] * {{ color: {text} !important; }}'
    css += f'.stApp [data-testid=\"stHeader\"] {{ background-color: {bg} !important; }}'
    css += f'.stApp .st-bb,.stApp .st-cb,.stApp .st-db,.stApp .st-eb {{ color: {text} !important; }}'
    css += f'html,body {{ font-size: {font_size}px !important; }}'
    css += '</style>'
    st.markdown(css, unsafe_allow_html=True)
