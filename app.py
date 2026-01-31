import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: SUPREME CONTRAST & ACCESSIBILITY]
st.set_page_config(page_title="D-Fi Vault v7.7", page_icon="🏛️", layout="wide")

# --- CSS: 시인성 300% 강화 및 레이아웃 최적화 ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* 패널 스타일 */
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; }
    
    /* 🔴 핵심 수정 1: 모든 작은 설명글을 순백색(#FFFFFF)으로 고정 */
    .stage-desc, .stMarkdown p, .stTextArea label, .stTextInput label { 
        color: #FFFFFF !important; 
        font-size: 1.05em !important; 
        font-weight: 500 !important;
        opacity: 1 !important; /* 투명도 제거하여 항상 선명하게 */
        display: block;
        margin-bottom: 8px;
    }
    
    /* 🔴 핵심 수정 2: 입력창 내부 글자 가독성 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border: 1px solid #484F58 !important;
    }

    /* 🔴 핵심 수정 3: 버튼 텍스트 대비 강화 (검은색 글자) */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; /* 흰색/황금 배경에 검은 글씨로 가독성 확보 */
        font-weight: 800 !important; 
        border-radius: 8px;
        width: 100%;
    }

    /* 마스터 메시지 스타일 */
    .master-dialogue { 
        background-color: #2D2D2D; padding: 18px; border-radius: 12px; 
        border-left: 5px solid #D4AF37; margin-top: 15px; color: #FFFFFF;
    }
    .master-name { color: #D4AF37; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

col_left, col_right = st.columns(2)

# --- LEFT PANEL: 원재료 기록 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    # 원문 저장 폼
    with st.form("raw_save"):
        st.markdown("<span class='stage-desc'>꿈의 내용을 날것 그대로 기록하세요.</span>", unsafe_allow_html=True)
        dream_raw = st.text_area("", height=350, placeholder="여기에 적는 글자는 이제 아주 선명하게 보입니다.")
        if st.form_submit_button("📓 이 꿈만 날것으로 저장하기"):
            if dream_raw:
                supabase.table("dreams").insert({"context": dream_raw}).execute()
                st.toast("원문이 금고에 보관되었습니다.", icon="📓")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 연구소 및 이력 불러오기 ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    # 🔴 핵심 수정 4: 오른쪽에 분석 이력 불러오기 버튼 추가
    if st.button("📂 마스터 분석 이력 불러오기"):
        try:
            res = supabase.table("dreams").select("*").not_.is_("meaning", "null").order("created_at", desc=True).limit(3).execute()
            if res.data:
                for d in res.data:
                    with st.expander(f"✨ {d['created_at'][:10]} | {d['symbol'][:15]}"):
                        st.write(f"**역학:** {d['block']}")
                        st.write(f"**해석:** {d['meaning']}")
                        st.write(f"**의례:** {d['ritual_self']}")
            else: st.info("아직 분석된 기록이 없습니다.")
        except: st.error("데이터를 가져올 수 없습니다.")

    with st.form("master_lab"):
        # Stage 1 & 2
        st.subheader("🚀 Stage 1: 이미지 연상")
        st.markdown("<span class='stage-desc'>강렬한 상징들을 추출하세요. (줄바꿈 가능)</span>", unsafe_allow_html=True)
        s1 = st.text_area("상징", height=80)

        st.subheader("🔍 Stage 2: 내적 역학")
        st.markdown("<span class='stage-desc'>이미지와 현실의 에너지 줄다리기를 정의하세요.</span>", unsafe_allow_html=True)
        s2 = st.text_area("역학", height=100)

        # Stage 3: 통합 해석
        if s1 and s2:
            st.markdown(f"""
            <div class='master-dialogue'>
                <span class='master-name'>Master's Insight:</span> {s1}은(는) 당신의 내면 에너지가 현실의 {s2[:20]}... 지점과 결합하고 있음을 의미합니다.
            </div>
            """, unsafe_allow_html=True)

        # 저장 버튼
        if st.form_submit_button("🏛️ 마스터의 지혜를 금고에 저장"):
            if s1:
                supabase.table("dreams").insert({"symbol": s1, "block": s2, "meaning": "통합 해석 완료"}).execute()
                st.balloons()
    st.markdown("</div>", unsafe_allow_html=True)
