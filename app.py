import streamlit as st
from supabase import create_client, Client

# [SYSTEM VIBE: GOLDEN DARK & SACRED]
st.set_page_config(page_title="D-Fi Vault: Master Edition", page_icon="🏛️")

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("🏛️ D-Fi Vault: Master's Path")
st.markdown("---")

with st.form("master_dream_work"):
    
    # [Stage 1: Robert Johnson's Association]
    st.subheader("🚀 Stage 1: 연상 (Association)")
    st.info("💡 **Robert Johnson's View:** 상징을 분석하려 하지 말고, 그 상징에서 뻗어 나오는 모든 줄기를 나열하세요.")
    symbol = st.text_input("상징의 원석", placeholder="예: 거대한 바다, 낡은 열쇠")

    # [Stage 2: Carl Jung's Archetypal Dynamics]
    st.subheader("🔍 Stage 2: 역학관계 (Inner Dynamics)")
    st.info("💡 **Carl Jung's View:** 이 상징은 내 안의 '그림자'인가요, 아니면 나를 이끄는 '아니마'인가요? 내적 인격의 충돌을 확인하세요.")
    col1, col2 = st.columns(2)
    with col1:
        persona = st.selectbox("활성화된 원형(Archetype)", 
                               ["그림자(잠재력의 창고)", "아니마/무스(영혼의 인도자)", "현자(내면의 스승)", "페르소나(사회적 가면)"])
    with col2:
        context = st.text_input("현실의 경제/사회적 상황", placeholder="예: 새로운 투자 결정 전의 불안")

    # [Stage 3: Koh Hye-kyung's Soulful Interpretation]
    st.subheader("📝 Stage 3: 가치 해석 (Interpretation)")
    st.info("💡 **Koh Hye-kyung's View:** 꿈은 우리를 살리려고 옵니다. 이 메시지가 나의 '경제적 자립'과 '영혼의 성장'에 어떤 영양분을 주나요?")
    meaning = st.text_area("에너지의 가치 치환", placeholder="이 꿈은 내가 더 큰 풍요를 담을 그릇이 되기 위해 어떤 태도를 요구하나요?")

    # [Stage 4: Johnson & Koh's Ritual]
    st.subheader("🏃 Stage 4: 현실 의례 (Ritual)")
    st.info("💡 **Final View:** 로버트 존슨은 '신체적 의례'를 강조했습니다. 머리로만 이해하지 말고, 몸으로 그 에너지를 현실에 고정하세요.")
    ritual_self = st.text_input("나를 위한 실질적 행동", placeholder="예: 오늘 얻은 통찰을 바탕으로 경제 일지 한 장 쓰기")
    ritual_share = st.text_input("사회에 기여할 창의적 에너지", placeholder="예: 주변에 긍정적인 확언 나누기")
    
    social_val = st.slider("기여도 측정", 0, 100, 50)

    if st.form_submit_button("마스터의 관점으로 금고 저장"):
        if symbol and ritual_self:
            data = {
                "symbol": symbol, "block": persona, "context": context,
                "meaning": meaning, "ritual_self": ritual_self,
                "ritual_share": ritual_share, "social_value": social_val
            }
            try:
                supabase.table("dreams").insert(data).execute()
                st.balloons()
                st.success("빌더님, 대가들의 지혜가 담긴 데이터 자산이 성공적으로 기록되었습니다.")
            except Exception as e:
                st.error(f"저장 중 오류 발생: {e}")
