import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from frontend.api import get_settings, update_settings, change_password, delete_account, clear_chat_history
from utils.i18n import t

st.set_page_config(page_title='设置', page_icon='=')

if 'token' not in st.session_state:
    st.warning('请先登录')
    st.switch_page('pages/login.py')
    st.stop()
from frontend.theme import load_and_apply
load_and_apply()

settings_data = get_settings()
lang = settings_data.get('language', 'zh') if settings_data else 'zh'
_ = lambda key: t(key, lang)

st.title(_('settings'))

tab_general, tab_ai, tab_diary, tab_security, tab_data, tab_about = st.tabs([
    _('general'), _('ai_companion'), _('diary'), _('security'), _('data_management'), _('about')
])

# ---- General ----
with tab_general:
    new_lang = st.selectbox(_('language'), ['zh', 'en'],
        index=0 if lang == 'zh' else 1,
        format_func=lambda x: {'zh': '中文', 'en': 'English'}[x])
    new_theme = st.radio(_('theme'), ['light', 'dark'],
        index=0 if settings_data.get('theme') == 'light' else 1,
        format_func=lambda x: _('light') if x == 'light' else _('dark'))
    new_font = st.slider(_('font_size'), 10, 24, settings_data.get('font_size', 14))
    if st.button(_('save_success'), key='save_general'):
        update_settings(language=new_lang, theme=new_theme, font_size=new_font)
        st.success(_('save_success'))
        st.rerun()

# ---- AI Companion ----
with tab_ai:
    ai_styles = {'empathetic': _('empathetic'), 'rational': _('rational'),
                 'humorous': _('humorous'), 'concise': _('concise')}
    cur_style = settings_data.get('ai_style', 'empathetic')
    style_keys = list(ai_styles.keys())
    new_style = st.selectbox(_('ai_style'), style_keys,
        index=style_keys.index(cur_style) if cur_style in style_keys else 0,
        format_func=lambda x: ai_styles[x])
    new_nickname = st.text_input(_('ai_nickname'), value=settings_data.get('ai_nickname', ''))
    new_retention = st.number_input(_('history_retention'), 1, 365, settings_data.get('history_retention_days', 30))
    sensitivities = {'low': _('low'), 'medium': _('medium'), 'high': _('high')}
    cur_sens = settings_data.get('crisis_sensitivity', 'medium')
    sens_keys = list(sensitivities.keys())
    new_sens = st.selectbox(_('crisis_sensitivity'), sens_keys,
        index=sens_keys.index(cur_sens) if cur_sens in sens_keys else 1,
        format_func=lambda x: sensitivities[x])
    if st.button(_('save_success'), key='save_ai'):
        update_settings(ai_style=new_style, ai_nickname=new_nickname,
                        history_retention_days=new_retention, crisis_sensitivity=new_sens)
        st.success(_('save_success'))
        st.rerun()

# ---- Diary ----
with tab_diary:
    scale_opts = {'1-5': '1-5', '1-10': '1-10'}
    cur_scale = settings_data.get('emotion_scale', '1-10')
    scale_keys = list(scale_opts.keys())
    new_scale = st.radio(_('emotion_scale'), scale_keys,
        index=scale_keys.index(cur_scale) if cur_scale in scale_keys else 1, horizontal=True)
    reminder_on = st.checkbox(_('daily_reminder'), value=bool(settings_data.get('daily_reminder_enabled', 0)))
    reminder_time = st.time_input(_('reminder_time'), value=None)
    if st.button(_('save_success'), key='save_diary'):
        rt_str = reminder_time.strftime('%H:%M') if reminder_time else None
        update_settings(emotion_scale=new_scale, daily_reminder_enabled=int(reminder_on),
                        daily_reminder_time=rt_str)
        st.success(_('save_success'))
        st.rerun()

# ---- Security ----
with tab_security:
    st.subheader(_('change_password'))
    with st.form('pwd_form'):
        old = st.text_input(_('old_password'), type='password')
        new = st.text_input(_('new_password'), type='password')
        conf = st.text_input(_('confirm_password'), type='password')
        if st.form_submit_button(_('change_password')):
            if new != conf:
                st.error(_('password_mismatch'))
            elif not old or not new:
                st.warning('请填写完整')
            else:
                result = change_password(old, new)
                if result:
                    st.success(_('password_updated'))
                else:
                    st.error(_('password_error'))

# ---- Data ----
with tab_data:
    if st.button(_('export_data')):
        st.info(_('export_placeholder'))
    if st.button(_('clear_history'), type='primary'):
        if clear_chat_history():
            st.success(_('history_cleared'))
    st.divider()
    if st.button(_('delete_account'), type='secondary'):
        with st.form('delete_confirm_form'):
            st.warning(_('delete_confirm'))
            confirmed = st.checkbox('我确定要删除账户')
            if st.form_submit_button('确认删除', type='primary') and confirmed:
                if delete_account():
                    st.session_state.clear()
                    st.success(_('account_deleted'))
                    st.switch_page('pages/login.py')

# ---- About ----
with tab_about:
    st.subheader(_('app_name'))
    st.caption(_('app_desc'))
    st.metric(_('version'), '0.3.0')
    st.divider()
    st.subheader(_('hotline_title'))
    st.markdown('''
    - 全国心理援助热线: **400-161-9995**
    - 北京心理危机干预中心: **010-82951332**
    - Lifeline (国际): **988**
    ''')

if st.sidebar.button(_('back'), use_container_width=True):
    st.switch_page('streamlit_app.py')

