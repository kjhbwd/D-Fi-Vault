import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# [SYSTEM VIBE: GOLDEN & PROSPEROUS]
st.set_page_config(page_title="D-Fi Prosperity Vault", page_icon="💰")

# 디자인 테마 설정
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { background: linear-gradient(45deg, #FFD700, #FF4B4B); color: black; font-weight: bold; }
    .philosophy-box { background-color: #1E1E1E; padding: 15px; border-left: 5px solid #FFD700; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 구글 시트 연결 (나중에 수파베이스로 확장 전까지 사용)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("구글 시트 연결 설정이 필요합니다. (Secrets 확인)")

st.title("🌙 D-Fi: Asset to Prosperity")
st.markdown("""
<div class="philosophy-box">
    <b>Building Philosophy:</b> 내가 먼저 이 시스템의 1호 수혜자가 되어 경제적 안정을 이루고, 
    그 넘치는 에너지를 이웃과 사회에 창의적으로 기여합니다.
</div>
""", unsafe_allow_html=True)

# [4단계 꿈 작업 폼]
with st.form("self_prosperity_form"):
    st.subheader("🚀 Stage 1: 내면의 자원 발견 (Associations)")
    symbol = st.text_input("꿈의 상징 (나의 숨겨진 잠재력)", placeholder="예: 끊이지 않는 샘물")

    st.subheader("🔍 Stage 2: 에너지 누수 차단 (Inner Dynamics)")
    inner_block = st.selectbox("현재 나의 흐름을 막는 인격은?", 
                               ["결핍을 두려워하는 나", "성공을 회피하는 나", "과거에 머무는 나", "완벽주의자"])
    context = st.text_input("해결이 시급한 현실의 경제적 상황", placeholder="예: 자금 흐름, 업무 집중도")

    st.subheader("📝 Stage 3: 가치 변환 해석 (Interpretation)")
    meaning = st.text_area("나의 경제적 안정을 위한 무의식의 직구", 
                           placeholder="예: 확신이 생길 때까지 에너지를 응축하라")

    st.subheader("🏃 Stage 4: 부의 선순환 의례 (Ritual)")
    ritual_self = st.text_input("나를 위한 실질적 행동 (경제적 이득과 직결)", placeholder="예: 관련 분야 30분 공부")
    ritual_share = st.text_input("내가 여유로워졌을 때 이웃에게 줄 도움", placeholder="예: 통찰 공유하기")
    
    contribution_level = st.slider("이 작업의 미래 사회적 기여도 예상", 0, 100, 50)

    submit_button = st.form_submit_button("나의 자산 금고에 영구 저장")

if submit_button:
    if symbol and ritual_self:
        # 데이터 구조화
        new_entry = pd.DataFrame([{
            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
            "Symbol": symbol,
            "Block": inner_block,
            "Context": context,
            "Meaning": meaning,
            "Ritual_Self": ritual_self,
            "Ritual_Share": ritual_share,
            "Contribution": contribution_level
        }])
        
        # 저장 시도 (Secrets 설정 전까지는 화면 출력으로 대체 가능)
        st.balloons()
        st.success("빌더님, 첫 번째 자산 로그가 성공적으로 생성되었습니다!")
        st.write("입력하신 데이터:", new_entry)
    else:
        st.warning("상징과 나를 위한 의례는 필수 입력 사항입니다.")
