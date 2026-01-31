import streamlit as st
import json, os, time

# [SYSTEM VIBE: DARK & DREAMY]
st.set_page_config(page_title="D-Fi Vault", page_icon="🌙")

# 디자인 커스텀 (깔끔한 다크 테마 반영)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { width: 100%; border-radius: 5px; background-color: #FF4B4B; color: white; }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    if os.path.exists("dream_vault.json"):
        with open("dream_vault.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user_score": 0, "history": []}

data = load_data()

st.title("🌙 D-Fi: Unconscious Asset")
st.write(f"현재 당신의 내면 자산 점수: **{data['user_score']} pts**")

# 입력 세션
with st.container():
    st.subheader("🛠️ 오늘 아침의 상징 마이닝")
    symbol = st.text_input("꿈의 상징", placeholder="예: 헹글라이더")
    somatic = st.select_slider("신체 반응 (수축 ↔ 확장)", options=["수축", "보통", "확장"])
    context = st.text_input("현실의 영역", placeholder="예: 크립토 투자")

    if st.button("자산화 엔진 가동"):
        with st.status("분석 중...", expanded=True) as status:
            time.sleep(1)
            st.write("로버트 존슨 역학 분석 중...")
            time.sleep(1)
            st.write("고혜경 박사 소마틱 필터링 중...")
            status.update(label="분석 완료!", state="complete", expanded=False)
        
        # 결과 리포트
        st.success(f"분석 결과: {symbol}은(는) {context} 영역의 {somatic} 에너지입니다.")
        st.balloons()
