import streamlit as st
from supabase import create_client, Client
import pandas as pd

# [SYSTEM VIBE: GOLDEN DARK & SACRED GEOMETRY]
st.set_page_config(page_title="D-Fi Vault v7", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #FF4B4B); 
        color: white; font-weight: bold; border-radius: 10px; width: 100%;
    }
    .left-panel { background-color: #161B22; padding: 20px; border-radius: 15px; border: 1px solid #30363D; }
    .right-panel { background-color: #1E1E1E; padding: 20px; border-radius: 15px; border: 1px solid #D4AF37; }
    .master-msg { background-color: #2D2D2D; padding: 15px; border-radius: 10px; border-left: 4px solid #D4AF37; margin-bottom: 10px; font-size: 0.9em; }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# [LAYOUT SETUP: 50:50]
col_left, col_right = st.columns(2)

# --- LEFT PANEL: DREAM JOURNAL & HISTORY ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 Dream Journal")
    
    # 지난 꿈 불러오기 기능
    if st.button("📂 지난 꿈 자산 불러오기"):
        try:
            response = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
            if response.data:
                for d in response.data:
                    with st.expander(f"📅 {d['created_at'][:10]} - {d['symbol']}"):
                        st.write(f"**해석:** {d['meaning']}")
                        st.write(f"**의례:** {d['ritual_self']}")
            else:
                st.info("아직 저장된 자산이 없습니다.")
        except Exception as e:
            st.error(f"데이터 로드 실패: {e}")

    dream_content = st.text_area("꿈의 내용을 가감 없이 기록하세요 (원재료)", height=400, placeholder="어젯밤 꿈속에서 나는...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: ROBERT JOHNSON'S 4 STAGES ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    with st.form("inner_work_form"):
        # Stage 1: 이미지 연상 (Robert Johnson)
        st.subheader("🚀 Stage 1: 이미지 연상")
        associations = st.text_input("꿈에서 가장 강렬했던 이미지들을 나열하세요", placeholder="황금 열쇠, 끝없는 바다, 속삭이는 노인")

        # Stage 2: 역학관계 (Dynamics)
        st.subheader("🔍 Stage 2: 역학관계 분석")
        dynamics = st.text_area("꿈의 내용과 위 이미지가 현실의 어떤 에너지(경제/관계)와 줄다리기 중인가요?", 
                                placeholder="예: 바다는 나의 막연한 불안을, 열쇠는 이번 계약의 해답을 상징하는 듯함")

        # Stage 3: 자동 통합 해석 (Jung, Johnson, Koh)
        st.subheader("📝 Stage 3: 마스터 통합 해석")
        if st.checkbox("거장들의 토론 가동 (AI 분석 시뮬레이션)"):
            st.markdown(f"""
            <div class='master-msg'><b>Carl Jung:</b> "이 꿈은 당신의 의식이 {associations}에만 매몰된 것을 경고하며, 전체성을 위해 반대 에너지를 보상하고 있습니다."</div>
            <div class='master-msg'><b>Robert Johnson:</b> "이 에너지는 단순한 생각이 아닙니다. 당신의 내면에서 실제적인 힘의 이동이 일어나고 있습니다."</div>
            <div class='master-msg'><b>Koh Hye-kyung:</b> "이미지가 살아서 움직이게 하세요. {associations}는 당신의 영혼이 경제적 자립을 위해 던진 생명줄입니다."</div>
            """, unsafe_allow_html=True)
            auto_meaning = f"[{associations}]을 통한 에너지 정렬과 현실적 직면의 필요성"
        else:
            auto_meaning = st.text_area("마스터들의 조언을 바탕으로 직접 가치를 치환하세요")

        # Stage 4: 현실 의례 (Ritual)
        st.subheader("🏃 Stage 4: 현실화 의례")
        st.info("💡 마스터의 추천 의례: '이미지를 종이에 그리고, 그 뒤에 오늘 당장 확인해야 할 통장 잔고를 적으세요.'")
        ritual_self = st.text_input("나를 위한 물리적 행동", placeholder="예: 관련 서류 재검토 및 10분 명상")
        ritual_share = st.text_input("사회적 기여/공유", placeholder="예: 오늘 얻은 통찰 X에 포스팅")
        
        # 저장 버튼
        if st.form_submit_button("자산 금고에 영구 저장"):
            if associations and ritual_self:
                data = {
                    "symbol": associations, "block": "Master Logic v7", "context": dynamics,
                    "meaning": auto_meaning, "ritual_self": ritual_self,
                    "ritual_share": ritual_share
                }
                supabase.table("dreams").insert(data).execute()
                st.balloons()
                st.success("빌더님, 마스터들과의 협업 결과가 금고에 저장되었습니다.")
            else:
                st.warning("1단계와 4단계는 에너지를 현실로 가져오는 필수 장치입니다.")
    st.markdown("</div>", unsafe_allow_html=True)
