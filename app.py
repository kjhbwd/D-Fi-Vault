import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: MAXIMUM CLARITY & GOLDEN ARCHETYPE]
st.set_page_config(page_title="D-Fi Vault v7.8", page_icon="🏛️", layout="wide")

# --- CSS: 시각적 사각지대 제거 및 고대비 설정 ---
st.markdown("""
    <style>
    /* 1. 배경 및 기본 텍스트: 완전한 어둠 속의 선명한 흰색 */
    .stApp { background-color: #0E1117; color: #FFFFFF !important; }
    
    /* 2. 패널 디자인: 좌(남색조), 우(황금조) */
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; }
    
    /* 🔴 핵심 수정: 모든 설명글(Stage Desc) 및 라벨 상시 백색 고정 */
    .stage-desc, .stMarkdown p, label, .stSubheader { 
        color: #FFFFFF !important; 
        font-size: 1.1em !important; 
        opacity: 1 !important; 
        visibility: visible !important;
        margin-bottom: 10px;
        font-weight: 500;
    }

    /* 🔴 핵심 수정: 버튼 - 마우스를 올리지 않아도 상시 선명하게 노출 */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; /* 배경과 대비되는 검은 글씨 */
        font-weight: 800 !important; 
        border-radius: 8px !important;
        width: 100% !important;
        opacity: 1 !important; /* 투명도 제거 */
        display: block !important;
        border: none !important;
        padding: 10px !important;
        margin-top: 10px;
    }

    /* 입력창 내부 글자 가독성 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border: 1px solid #484F58 !important;
    }

    /* 마스터 메시지 박스 */
    .master-dialogue { 
        background-color: #2D2D2D; padding: 20px; border-radius: 12px; 
        border-left: 5px solid #D4AF37; margin-top: 15px; color: #FFFFFF;
    }
    .master-name { color: #D4AF37; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# [LAYOUT: 50:50]
col_left, col_right = st.columns(2)

# --- LEFT PANEL: 원재료 기록 및 불러오기 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    # 📂 지난 꿈 불러오기 (원문 중심)
    if st.button("📂 지난 꿈 원문 불러오기"):
        try:
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(3).execute()
            if res.data:
                for d in res.data:
                    with st.expander(f"📅 {d['created_at'][:10]} | {d.get('symbol', '기록')[:10]}"):
                        st.write(d.get('context', '내용 없음'))
            else: st.info("기록이 없습니다.")
        except: st.error("연결 확인 필요")

    with st.form("left_raw_form"):
        st.markdown("<span class='stage-desc'>꿈의 내용을 날것 그대로 기록하세요. (줄바꿈 가능)</span>", unsafe_allow_html=True)
        dream_raw = st.text_area("", height=350, placeholder="여기에 적는 글자는 상시 선명하게 보입니다.")
        if st.form_submit_button("📓 이 꿈만 날것으로 저장하기"):
            if dream_raw:
                supabase.table("dreams").insert({"context": dream_raw}).execute()
                st.toast("원문이 금고에 저장되었습니다.", icon="📓")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 연구소 (4단계 공정) ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    # 📂 분석 이력 불러오기 (해석/의례 중심)
    if st.button("📂 마스터 분석 이력 불러오기"):
        try:
            res = supabase.table("dreams").select("*").not_.is_("meaning", "null").order("created_at", desc=True).limit(3).execute()
            if res.data:
                for d in res.data:
                    with st.expander(f"✨ {d['created_at'][:10]} | {d['symbol'][:15]}"):
                        st.write(f"**해석:** {d['meaning']}")
                        st.write(f"**의례:** {d['ritual_self']}")
            else: st.info("분석된 기록이 없습니다.")
        except: st.error("불러오기 실패")

    with st.form("right_master_form"):
        # Stage 1: 연상
        st.subheader("🚀 Stage 1: 이미지 연상")
        st.markdown("<span class='stage-desc'>강렬한 상징들을 추출하세요. (줄바꿈 지원)</span>", unsafe_allow_html=True)
        s1 = st.text_area("상징 나열", height=80)

        # Stage 2: 역학
        st.subheader("🔍 Stage 2: 내적 역학")
        st.markdown("<span class='stage-desc'>이미지와 현실의 에너지 관계를 정의하세요.</span>", unsafe_allow_html=True)
        s2 = st.text_area("관계 분석", height=80)

        # Stage 3: 통합 해석 (자동 생성)
        st.subheader("📝 Stage 3: 통합 해석")
        final_meaning = ""
        if s1 and s2:
            st.markdown(f"""
            <div class='master-dialogue'>
                <div><span class='master-name'>Jung & Johnson:</span> "{s1}은(는) 당신의 의식이 놓친 균형점을 가리킵니다. {s2[:20]}...의 역동에 주목하세요."</div>
            </div>
            """, unsafe_allow_html=True)
            final_meaning = f"[{s1.splitlines()[0]}] 기반 에너지 통합 해석"

        # Stage 4: 의례 제안
        st.subheader("🏃 Stage 4: 현실 의례")
        st.markdown("<span class='stage-desc'>부의 에너지를 고정할 구체적 행동을 정하세요.</span>", unsafe_allow_html=True)
        ritual_suggest = "상징을 시각화하고 투자 원칙을 재검토하세요." if s1 else "입력 대기 중..."
        st.info(f"💡 추천: {ritual_suggest}")
        s4 = st.text_input("나의 행동 확정", placeholder="예: 명상 10분 후 일지 쓰기")

        if st.form_submit_button("🏛️ 마스터의 지혜를 금고에 저장"):
            if s1 and s4:
                supabase.table("dreams").insert({
                    "symbol": s1, "block": s2, "meaning": final_meaning, "ritual_self": s4
                }).execute()
                st.balloons()
                st.success("자산화 완료!")
    st.markdown("</div>", unsafe_allow_html=True)
