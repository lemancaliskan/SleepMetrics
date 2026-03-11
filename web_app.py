import streamlit as st
import plotly.graph_objects as go
from engine import SleepEngine
from PIL import Image
import os

PRIMARY = "#1C274C"
SECONDARY = "#8d93a5"
SUCCESS = "#4CAF50"
WARNING = "#FFC107"
DANGER = "#EF5350"
TEXT_MAIN = "#FFFFFF"
TEXT_MUTED = "#AAAAAA"

ASSETS_PATH = "assets"

def get_logo(is_dark_mode):
    logo_name = "logo_dark.png" if is_dark_mode else "logo.png"
    logo_path = os.path.join(ASSETS_PATH, logo_name)
    if os.path.exists(logo_path):
        return Image.open(logo_path)
    return "🌙"

st.set_page_config(
    page_title="SleepMetrics Web",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_resource
def load_engine():
    return SleepEngine()

engine = load_engine()

langs = {
    "TR": {
        "app_title": "",
        "btn_run": "UYKU ANALİZİNİ BAŞLAT",
        "status_wait": "Analiz bekleniyor...",
        "status_done": "",
        "title_risk": "Uyku Kalitesi Analizi",
        "title_rec": "✨ Size Özel Sağlık Önerileri",
        "title_diagnosis": "TEŞHİS",
        "fields": {
            "age": "Yaş", "sex": "Cinsiyet", "sex_opts": ["Erkek", "Kadın"],
            "height": "Boy (cm)", "weight": "Kilo (kg)",
            "duration": "Uyku Süresi (Saat)", "activity": "Fiziksel Aktivite (dk)",
            "sys_bp": "Sistolik Kan Basıncı", "dia_bp": "Diastolik Kan Basıncı",
            "hr": "Kalp Atış Hızı", "stress": "Stres Seviyesi (1-10)",
            "steps": "Günlük Adım Sayısı"
        },
        "recs": {
            "apnea": "Uyku Apnesi", "apnea_desc": "KBB uzmanına görünün.",
            "insomnia": "İnsomnia", "insomnia_desc": "Yatmadan 2 saat önce mavi ışığı kesin.",
            "stress": "Yüksek Stres", "stress_desc": "Yatmadan önce nefes egzersizi yapın.",
            "duration": "Düşük Süre", "duration_desc": "Vücut onarımı için +7 saat hedefleyin.",
            "activity": "Hareketsizlik", "activity_desc": "Günlük 20-30 dk yürüyüş derin uykuyu %30 artırır.",
            "perfect": "Harika!", "perfect_desc": "Uyku verileriniz oldukça sağlıklı görünüyor.",
            "hr_high": "Yüksek Nabız", "hr_high_desc": "Kafeini azaltın ve bol su tüketin.",
            "bp_high": "Yüksek Tansiyon", "bp_high_desc": "Tuzu kısıtlayın, takibi artırın.",
            "steps_low": "Düşük Adım Sayısı", "steps_low_desc": "Günlük 7500 adım, uykuya dalma süresini %15 kısaltır.",
            "steps_mid": "Hareket Hedefi", "steps_mid_desc": "Uykuda tam onarım için hedefi 10.000 adıma çıkarın."
        },
        "disclaimer": "⚠️ SleepMetrics Core - Uyku Sağlığı ve Risk Değerlendirme Aracı: "
                      "<br>Bu hesaplama aracı sadece bilgilendirme amaçlıdır ve profesyonel tıbbi tavsiye, teşhis veya tedavinin yerini tutmaz. "
                      "<br>Sağlık durumunuz hakkında endişeleriniz varsa, mutlaka bir sağlık profesyoneline başvurun."
    },
    "EN": {
        "app_title": "",
        "btn_run": "RUN SLEEP ANALYSIS",
        "status_wait": "Awaiting analysis...",
        "status_done": "",
        "title_risk": "Sleep Quality Analysis",
        "title_rec": "✨ Personalized Health Recommendation",
        "title_diagnosis": "DIAGNOSIS",
        "fields": {
            "age": "Age", "sex": "Gender", "sex_opts": ["Male", "Female"],
            "height": "Height (cm)", "weight": "Weight (kg)",
            "duration": "Sleep Duration (Hours)", "activity": "Physical Activity (mins)",
            "sys_bp": "Systolic Blood Pressure", "dia_bp": "Diastolic Blood Pressure",
            "hr": "Heart Rate", "stress": "Stress Level (1-10)",
            "steps": "Daily Steps"
        },
        "recs": {
            "apnea": "Sleep Apnea", "apnea_desc": "Consult an ENT specialist.",
            "insomnia": "Insomnia", "insomnia_desc": "Avoid blue light exposure 2 hours before sleep.",
            "stress": "High Stress", "stress_desc": "Practice breathing exercises before sleep.",
            "duration": "Low Duration", "duration_desc": "Aim for +7 hours for body repair.",
            "activity": "Inactivity", "activity_desc": "20-30 mins daily walk increases deep sleep by 30%.",
            "perfect": "Great!", "perfect_desc": "Your sleep data looks quite healthy.",
            "hr_high": "High Heart Rate", "hr_high_desc": "Reduce caffeine intake and drink plenty of water.",
            "bp_high": "High Blood Pressure", "bp_high_desc": "Restrict salt intake, increase monitoring.",
            "steps_low": "Low Step Count", "steps_low_desc": "7500 steps a day reduces sleep onset latency by 15%.",
            "steps_mid": "Movement Goal",
            "steps_mid_desc": "Increase your goal to 10000 steps for full recovery during sleep."
        },
        "disclaimer": "⚠️ SleepMetrics Core - Sleep Health & Risk Assessment Tool:"
                      "<br>This calculation tool is for informational purposes only and is not a substitute "
                      "<br>for professional medical advice, diagnosis, or treatment."
                      "<br>If you have concerns about your health, please consult a qualified healthcare professional."
    }
}

if 'lang' not in st.session_state: st.session_state.lang = "TR"
if 'theme_mode' not in st.session_state: st.session_state.theme_mode = "light"


def toggle_lang():
    st.session_state.lang = "EN" if st.session_state.lang == "TR" else "TR"


def toggle_theme():
    st.session_state.theme_mode = "dark" if st.session_state.theme_mode == "light" else "light"


is_dark = st.session_state.theme_mode == "dark"
bg_color = "#1e1e1e" if is_dark else "#f2f2f2"
card_bg = "#2b2b2b" if is_dark else "#ffffff"
text_col = TEXT_MAIN if is_dark else "#000000"
border_col = "#3d3d3d" if is_dark else "#e0e0e0"

current_logo = get_logo(is_dark)

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color}; color: {text_col}; }}

    div[data-testid="stButton"] > button[kind="primary"] {{ 
        width: 100% !important; 
        border-radius: 12px !important; 
        font-weight: bold !important; 
        background-color: {PRIMARY} !important; 
        color: {TEXT_MAIN} !important; 
        height: 50px !important; 
        border: none !important;
    }}
    div[data-testid="stButton"] > button[kind="primary"]:hover {{ 
        background-color: {SECONDARY} !important; 
        color: {TEXT_MAIN} !important;
    }}

    div[data-testid="stButton"] > button[kind="secondary"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        width: 100% !important;
        color: {text_col} !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }}

    div[data-testid="stButton"] > button[kind="secondary"]:hover,
    div[data-testid="stButton"] > button[kind="secondary"]:active,
    div[data-testid="stButton"] > button[kind="secondary"]:focus {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        color: {text_col} !important;
    }}

    div[data-testid="stButton"] > button[kind="secondary"] p {{
        font-size: 26px !important;
        margin: 0 !important;
        line-height: 1 !important;
    }}

    .panel-box {{ background-color: {card_bg}; padding: 15px; border-radius: 15px; margin-bottom: 15px; border: 1px solid {border_col}; }}
    .rec-card {{ background-color: {card_bg}; padding: 10px; border-radius: 10px; border: 1px solid; height: 85px; }}
    .rec-title {{ font-size: 13px; font-weight: bold; margin-bottom: 3px; }}
    .rec-text {{ font-size: 11px; line-height: 1.2; color: {text_col}; }}

    div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown div.risk-target) {{
        background-color: {card_bg};
        padding: 15px;
        border-radius: 15px;
        border: 1px solid {border_col};
        margin-bottom: 15px;
    }}
    .risk-target {{ display: none; }}

    div[data-testid="stNumberInput"] label p, div[data-testid="stSelectbox"] label p {{ color: {text_col} !important; }}
    div[data-testid="stNumberInput"] input {{ background-color: {card_bg} !important; color: {text_col} !important; border-color: {border_col} !important; }}
    div[data-baseweb="select"] > div {{ background-color: {card_bg} !important; color: {text_col} !important; border-color: {border_col} !important; }}
    div[data-baseweb="select"] span {{ color: {text_col} !important; }}
    </style>
""", unsafe_allow_html=True)

t = langs[st.session_state.lang]
f = t["fields"]

top_col1, top_col2 = st.columns([15, 1.2])
with top_col2:
    sub_c1, sub_c2 = st.columns(2, gap="small")
    with sub_c1:
        st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
        st.button("🌐", on_click=toggle_lang, key="lang_toggle")
        st.markdown('</div>', unsafe_allow_html=True)
    with sub_c2:
        st.markdown('<div class="icon-btn">', unsafe_allow_html=True)
        st.button("☀️" if is_dark else "🌙", on_click=toggle_theme, key="theme_toggle")
        st.markdown('</div>', unsafe_allow_html=True)

col_left, col_space, col_right = st.columns([1.1, 0.05, 1.85])

with col_left:
    l_spacer1, l_logo, l_spacer2 = st.columns([1, 4, 1])
    with l_logo:
        if isinstance(current_logo, str):
            st.markdown(f"<h1 style='text-align:center;'>{current_logo} SleepMetrics</h1>", unsafe_allow_html=True)
        else:
            st.image(current_logo, width=500)

    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input(f["age"], 10, 150, 30)
        height = st.number_input(f["height"], 10, 250, 175)
        duration = st.number_input(f["duration"], 0.0, 24.0, 7.5, step=0.5)
        sys_bp = st.number_input(f["sys_bp"], 0, 500, 120)
        hr = st.number_input(f["hr"], 0, 500, 70)
        steps = st.number_input(f["steps"], 0, 10000000, 8000, step=500)
    with c2:
        sex_val = st.selectbox(f["sex"], [1, 0], format_func=lambda x: f["sex_opts"][0] if x == 1 else f["sex_opts"][1])
        weight = st.number_input(f["weight"], 0.0, 500.0, 75.0, step=1.0)
        activity = st.number_input(f["activity"], 0, 100000000, 60)
        dia_bp = st.number_input(f["dia_bp"], 0, 500, 80)
        stress = st.number_input(f["stress"], 1, 10, 5)

    st.write("")
    analyze_clicked = st.button(t["btn_run"], type="primary", use_container_width=True)

with col_right:
    quality_score = 0
    disorder = ""

    if analyze_clicked:
        height_m = height / 100
        bmi_val = round(weight / (height_m ** 2), 2)

        model_input = [sex_val, age, duration, activity, stress, bmi_val, sys_bp, dia_bp, hr, steps]
        quality_score, disorder = engine.predict(model_input, lang=st.session_state.lang.lower())

    with st.container():
        st.markdown('<div class="risk-target"></div>', unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: center; margin-bottom: 0;'>{t['title_risk']}</h5>", unsafe_allow_html=True)

        gauge_color = SUCCESS if quality_score >= 8 else (WARNING if quality_score >= 5 else DANGER)
        status_text = f"{t['status_done']} 0/10" if analyze_clicked else t["status_wait"]

        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=quality_score,
            gauge={'axis': {'range': [0, 10], 'visible': False}, 'bar': {'color': "rgba(0,0,0,0)"},
                   'steps': [{'range': [0, quality_score], 'color': gauge_color if analyze_clicked else border_col},
                             {'range': [quality_score, 10], 'color': border_col}]}))
        fig.update_layout(height=110, margin=dict(l=10, r=10, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)',
                          font={'color': text_col})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            f"<p style='text-align: center; color: {gauge_color}; font-weight:bold; font-size: 14px; margin-top: -30px;'>{status_text}</p>",
            unsafe_allow_html=True)

    diagnosis_title = t["title_diagnosis"]
    diagnosis_text = disorder if analyze_clicked else t["status_wait"]
    diagnosis_color = gauge_color if analyze_clicked else TEXT_MUTED

    st.markdown(f"""
        <div class='panel-box' style='text-align: center; display: flex; flex-direction: column; justify-content: center; min-height: 120px;'>
            <div style='color: {PRIMARY}; font-size: 12px; font-weight: bold; margin-bottom: 8px; letter-spacing: 1px;'>{diagnosis_title}</div>
            <div style='color: {diagnosis_color}; font-size: 26px; font-weight: 800; line-height: 1.1;'>
                {diagnosis_text.upper()}
            </div>
        </div>
    """, unsafe_allow_html=True)

    notes_html = f"<div class='panel-box'><h6 style='color: {PRIMARY}; margin-bottom: 15px;'>{t['title_rec']}</h6>"

    if analyze_clicked:
        r_t, recs = t["recs"], []

        if "Apne" in disorder or "Apnea" in disorder:
            recs.append((r_t["apnea"], r_t["apnea_desc"], "🌬️", DANGER))
        elif "İnsomnia" in disorder or "Insomnia" in disorder:
            recs.append((r_t["insomnia"], r_t["insomnia_desc"], "📱", "#3498db"))

        if stress > 7: recs.append((r_t["stress"], r_t["stress_desc"], "🧘", "#9b59b6"))
        if duration < 6: recs.append((r_t["duration"], r_t["duration_desc"], "⏰", "#e67e22"))
        if activity < 30: recs.append((r_t["activity"], r_t["activity_desc"], "👟", SUCCESS))

        if not recs:
            recs.append((r_t["perfect"], r_t["perfect_desc"], "✅", SUCCESS))

        if hr > 100: recs.append((r_t["hr_high"], r_t["hr_high_desc"], "❤️", DANGER))
        if sys_bp > 140: recs.append((r_t["bp_high"], r_t["bp_high_desc"], "⚠️", DANGER))

        if steps < 5000:
            recs.append((r_t["steps_low"], r_t["steps_low_desc"], "👣", "#3498db"))
        elif steps < 8000:
            recs.append((r_t["steps_mid"], r_t["steps_mid_desc"], "🏃", WARNING))

        notes_html += "<div style='display: flex; flex-wrap: wrap; gap: 8px; width: 100%; align-items: stretch; justify-content: flex-start;'>"

        for title, desc, icon, color in recs:
            notes_html += f"""<div style="flex: 0 0 calc(50% - 4px); min-width: 220px; border: 1px solid {color};
            border-radius: 10px; padding: 10px; background-color: {card_bg};
            box-sizing: border-box; display: flex; flex-direction: column; margin-bottom: 0;">
            <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <span style="font-size: 18px; margin-right: 8px;">{icon}</span>
            <span style="color: {color}; font-weight: bold; font-size: 13px;">{title}</span>
            </div>
            <div style="color: {text_col}; font-size: 11px; line-height: 1.3;">{desc}</div>
            </div>"""
        notes_html += "</div>"
    else:
        notes_html += f"<p style='font-size: 12px; color: {TEXT_MUTED};'>{t['status_wait']}</p>"

    notes_html += "</div>"
    st.markdown(notes_html, unsafe_allow_html=True)

    st.markdown(f"""<div style="background-color: {'#2d1f1f' if is_dark else '#fff5f5'}; border: 1px solid {DANGER}; border-radius: 6px; padding: 10px; text-align: center;">
            <span style="color: {DANGER}; font-size: 11px; font-style: italic;">{t['disclaimer']}</span>
        </div>""", unsafe_allow_html=True)