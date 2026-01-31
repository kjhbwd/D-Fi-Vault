import streamlit as st
from supabase import create_client, Client

# [SYSTEM VIBE: GOLDEN DARK]
st.set_page_config(page_title="D-Fi Prosperity Vault", page_icon="🏦")

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.title("🏦 D-Fi: Professional Vault")
st.info("빌더님의 철학: 나를 먼저 채우고, 그 여유로 세상을 돕습니다.")

with st.form("prosperity_form"):
    symbol = st.text_input("Stage 1: 꿈의 상징")
    block = st.selectbox("Stage 2: 나를 막는 인격", ["결핍 공포", "성공 회피", "무기력", "완벽주의"])
    context = st.text_input("Stage 2: 현실 맥락")
    meaning = st.text_area("Stage 3: 나를 위한 해석")
    ritual_self = st.text_input("Stage 4: 나를 위한 행동")
    ritual_share = st.text_input("Stage 4: 타인과 나눌 가치")
    social_val = st.slider("사회적 기여도 예상", 0, 100, 50)
    
    if st.form_submit_button("금고에 영구 저장"):
        if symbol and ritual_self:
            # SQL의 컬럼명 'social_value'와 맞춤
            data = {
                "symbol": symbol, "block": block, "context": context,
                "meaning": meaning, "ritual_self": ritual_self,
                "ritual_share": ritual_share, "social_value": social_val
            }
            try:
                supabase.table("dreams").insert(data).execute()
                st.balloons()
                st.success("보안 저장 완료! '실체'가 되기 위한 첫 로그가 기록되었습니다.")
            except Exception as e:
                st.error(f"저장 오류: {e}")
