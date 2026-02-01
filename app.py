import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: SUPREME CLARITY & DYNAMIC ENGINE]
st.set_page_config(page_title="D-Fi Vault v7.9", page_icon="🏛️", layout="wide")

# --- CSS: 시각적 사각지대 0% 선언 및 고대비 UI ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF !important; }
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; }
    
    /* 🔴 가독성 핵심: 모든 텍스트 라벨과 설명글을 순백색으로 상시 고정 */
    .stage-desc, label, p, .stSubheader, .stMarkdown { 
        color: #FFFFFF !important; 
        font-size: 1.1em !important; 
        opacity: 1 !important; 
        visibility: visible !important;
        font-weight: 500 !important;
    }

    /* 🔴 버튼: 마우스와 상관없이 상시 황금빛으로 빛나며 검은 글씨로 대비 극대화 */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; 
        font-weight: 800 !important; 
        border-radius: 8px !important;
        width: 100% !important;
        opacity: 1 !important;
        display: block !important;
        border: none !important;
        padding: 12px !important;
    }

    /* 입력창: 배경은 어둡게, 글자는 순백색으로 선명하게 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border: 1px solid #484F58 !important;
        font-size: 1.05em !important;
    }
    
    .master-dialogue { 
        background-color: #2D2D2D; padding: 20px; border-radius: 12px; 
        border-left: 6px solid #D4AF37; margin-top: 15px; color: #FFFFFF;
    }
    .master-name { color: #D4AF37; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

col_left, col_right = st.columns(2)

# --- LEFT PANEL: 원재료 저장 및 이력 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    if st.button("📂 지난 꿈 원문 불러오기"):
        res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(3).execute()
        if res.data:
            for d in res.data:
                with st.expander(f"📅 {d['created_at'][:10]} | 기록"):
                    st.write(d.get('context', '내용 없음'))
    
    with st.form("left_raw_form"):
        st.markdown("<span class='stage-desc'>꿈의 내용을 가감 없이 기록하세요 (줄바꿈 지원).</span>", unsafe_allow_html=True)
        dream_raw = st.text_area("", height=400, placeholder="여기에 입력하는 꿈 내용은 이제 상시 선명하게 보입니다.")
        if st.form_submit_button("📓 이 꿈만 날것으로 저장하기"):
            if dream_raw:
                supabase.table("dreams").insert({"context": dream_raw}).execute()
                st.toast("✅ 원문이 금고에 저장되었습니다.", icon="📓")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 랩 (트리거 기능 포함) ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    if st.button("📂 분석 이력 및 의례 불러오기"):
        res = supabase.table("dreams").select("*").not_.is_("meaning", "null").order("created_at", desc=True).limit(3).execute()
        if res.data:
            for d in res.data:
                with st.expander(f"✨ {d['created_at'][:10]} | {d['symbol'][:15]}"):
                    st.write(f"**해석:** {d['meaning']}")
                    st.write(f"**의례:** {d['ritual_self']}")

    with st.form("right_master_form"):
        st.subheader("🚀 Stage 1: 이미지 연상")
        s1 = st.text_area("상징 나열 (Enter로 구분 가능)", height=100)

        st.subheader("🔍 Stage 2: 내적 역학")
        s2 = st.text_area("에너지 관계 분석 (Enter로 구분 가능)", height=100)

        # 🔴 빌더님 핵심 요청: 적용 버튼 및 자동 해석
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        apply_interpretation = st.checkbox("⚙️ 마스터 통합 해석 가동 (적용)")
        
        st.subheader("📝 Stage 3: 마스터 통합 해석")
        final_meaning = ""
        if apply_interpretation and s1 and s2:
            st.markdown(f"""
            <div class='master-dialogue'>
                <div><span class='master-name'>Jung & Johnson:</span> "{s1[:15]}...의 상징은 당신의 무의식이 현실의 {s2[:15]}... 지점을 돌파하려는 강력한 시그널입니다. 이는 개성화를 향한 필수적 진통입니다."</div>
                <br>
                <div><span class='master-name'>Koh Hye-kyung:</span> "영혼의 에너지가 현실의 옷을 갈아입고 있습니다. 목표를 향한 이 역동을 온몸으로 받아들이세요."</div>
            </div>
            """, unsafe_allow_html=True)
            final_meaning = f"[{s1.splitlines()[0]}] 기반 에너지 정렬 및 목표 달성 전략"
        else:
            st.info("💡 Stage 1, 2 입력 후 위 '마스터 통합 해석 가동'을 체크하면 해석이 생성됩니다.")

        st.subheader("🏃 Stage 4: 현실 의례")
        st.info("💡 추천: '이미지를 형상화한 뒤 오늘 당장 실행할 구체적 경제 지표 3개를 기록하세요.'")
        s4 = st.text_input("나의 행동 확정", placeholder="예: 목표 도달을 위한 구체적 행동 1가지")

        if st.form_submit_button("🏛️ 마스터의 지혜를 금고에 저장"):
            if s1 and s4:
                supabase.table("dreams").insert({
                    "symbol": s1, "block": s2, "meaning": final_meaning, "ritual_self": s4, "context": dream_raw
                }).execute()
                st.balloons()
                st.success("🎉 빌더님의 부의 로그가 성공적으로 자산화되었습니다!")
    st.markdown("</div>", unsafe_allow_html=True)
