import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dampak Media Sosial", page_icon="📱")


@st.cache_resource
def load_artifacts():
    model = joblib.load("model.joblib")
    options = joblib.load("options.joblib")
    return model, options

# ---------- STYLE ----------
st.markdown("""<style>
#MainMenu, footer {visibility: hidden;}
.block-container {padding-top: 2rem; max-width: 1100px;}
.hero {padding: 2.2rem 2.4rem; border-radius: 24px; color: #fff; margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #7c3aed 0%, #ec4899 55%, #f59e0b 100%);
  box-shadow: 0 20px 50px rgba(124,58,237,.35);}
.hero .title {font-size: 2.3rem; font-weight: 800; line-height: 1.15;}
.hero .sub {margin-top: .6rem; opacity: .92; font-size: 1.05rem;}
.card {border-radius: 20px; padding: 1.4rem 1.6rem; height: 100%;
  background: rgba(128,128,128,.08); border: 1px solid rgba(128,128,128,.2);}
.card h4 {margin: 0 0 .8rem 0;}
.result {text-align: center; padding: 2rem 1.5rem; border-radius: 24px; color: #fff; height: 100%;
  animation: pop .5s ease-out;}
.result .emoji {font-size: 4.2rem; line-height: 1;}
.result .label {font-size: 2rem; font-weight: 800; margin: .4rem 0 .2rem;}
.result .conf {opacity: .92; font-size: 1.05rem;}
.bar-row {margin: .9rem 0;}
.bar-head {display: flex; justify-content: space-between; font-weight: 600; margin-bottom: .3rem;}
.bar-bg {height: 14px; border-radius: 999px; background: rgba(128,128,128,.2); overflow: hidden;}
.bar-fill {height: 100%; border-radius: 999px; animation: grow 1s ease-out;}
.tip {padding: .7rem 1rem; margin-bottom: .6rem; border-radius: 12px;
  background: rgba(128,128,128,.1); border-left: 4px solid #7c3aed;}
[data-testid="stMetric"] {padding: 1rem 1.2rem; border-radius: 16px;
  background: rgba(128,128,128,.08); border: 1px solid rgba(128,128,128,.2);}
.stButton > button, [data-testid="stFormSubmitButton"] > button {
  width: 100%; border: 0; border-radius: 12px; padding: .7rem 1rem; font-weight: 700; color: #fff;
  background: linear-gradient(135deg, #7c3aed, #ec4899); transition: all .2s ease;}
.stButton > button:hover, [data-testid="stFormSubmitButton"] > button:hover {
  transform: translateY(-2px); box-shadow: 0 8px 20px rgba(236,72,153,.4); color: #fff;}
@keyframes grow {from {width: 0;}}
@keyframes pop {from {opacity: 0; transform: scale(.92);} to {opacity: 1; transform: scale(1);}}
</style>""", unsafe_allow_html=True)

THEME = {  # emoji, judul, gradient kartu, warna bar
    "Positive": ("😄", "Dampak Positif", "linear-gradient(135deg,#10b981,#059669)", "#10b981"),
    "Neutral": ("😐", "Dampak Netral", "linear-gradient(135deg,#f59e0b,#d97706)", "#f59e0b"),
    "Negative": ("😟", "Dampak Negatif", "linear-gradient(135deg,#ef4444,#be123c)", "#ef4444"),
}


model, options = load_artifacts()

# ---------- HERO ----------
st.markdown(
    '<div class="hero"><div class="title">📱 Social Media Impact by Roff</div>'
    '<div class="sub">Prediksi dampak media sosial terhadap kehidupan mahasiswa '
    'dalam hitungan detik. Isi profil di sidebar, lalu klik Prediksi.</div></div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("## 🎛️ Profil Mahasiswa")
    with st.form("input_form"):
        st.caption("👤 Data diri")
        age = st.number_input("Usia", 15, 40, 21)
        gender = st.selectbox("Gender", options["Gender"])
        level = st.selectbox("Jenjang", ["High School", "Undergraduate", "Graduate"], index=1)
        country = st.selectbox("Negara", options["Country"])

        st.caption("📲 Kebiasaan digital")
        platform = st.selectbox("Platform favorit", options["Most_Used_Platform"])
        usage = st.slider("Pemakaian per hari (jam)", 0.0, 12.0, 4.0, 0.1)
        affects = st.radio("Mengganggu akademik?", ["No", "Yes"], horizontal=True)

        st.caption("🧠 Kesehatan")
        sleep = st.slider("Tidur per malam (jam)", 3.0, 12.0, 7.0, 0.1)
        mental = st.slider("Skor kesehatan mental", 1.0, 10.0, 6.0, 0.1)

        submitted = st.form_submit_button("✨ Prediksi Sekarang")

if not submitted:
    c1, c2, c3 = st.columns(3)
    for col, icon, title, text in [
        (c1, "📝", "1. Isi profil", "Lengkapi data mahasiswa di sidebar kiri."),
        (c2, "✨", "2. Klik Prediksi", "Model memproses semua fitur sekaligus."),
        (c3, "📊", "3. Lihat hasil", "Dapatkan prediksi beserta tingkat keyakinannya."),
    ]:
        col.markdown(f'<div class="card"><h4>{icon} {title}</h4>{text}</div>', unsafe_allow_html=True)
else:
    X_new = pd.DataFrame([{
        "Age": age, "Gender": gender, "Academic_Level": level, "Country": country,
        "Avg_Daily_Usage_Hours": usage, "Most_Used_Platform": platform,
        "Affects_Academic_Performance": affects,
        "Sleep_Hours_Per_Night": sleep, "Mental_Health_Score": mental,
    }])
    pred = model.predict(X_new)[0]
    proba = pd.Series(model.predict_proba(X_new)[0], index=model.classes_).sort_values(ascending=False)
    emoji, title, gradient, _ = THEME[pred]

    left, right = st.columns([1, 1.2])
    left.markdown(
        f'<div class="result" style="background:{gradient};box-shadow:0 18px 40px rgba(0,0,0,.25)">'
        f'<div class="emoji">{emoji}</div><div class="label">{title}</div>'
        f'<div class="conf">Keyakinan model: {proba[pred]*100:.1f}%</div></div>',
        unsafe_allow_html=True,
    )
    bars = "".join(
        f'<div class="bar-row"><div class="bar-head"><span>{THEME[c][0]} {c}</span>'
        f'<span>{p*100:.1f}%</span></div><div class="bar-bg"><div class="bar-fill" '
        f'style="width:{p*100:.1f}%;background:{THEME[c][3]}"></div></div></div>'
        for c, p in proba.items()
    )
    right.markdown(f'<div class="card"><h4>📊 Distribusi probabilitas</h4>{bars}</div>', unsafe_allow_html=True)

    st.write("")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("📲 Pemakaian", f"{usage:.1f} jam")
    m2.metric("😴 Tidur", f"{sleep:.1f} jam")
    m3.metric("🧠 Mental", f"{mental:.1f} / 10")
    m4.metric("🌍 Negara", country)

    if pred == "Positive":
        st.toast("Hasil positif! 🎉")

    st.balloons()
