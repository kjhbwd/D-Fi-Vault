import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: INSTANT REACTION & HIGH CONTRAST]
st.set_page_config(page_title="D-Fi Vault v8.0", page_icon="🏛️", layout="wide")

# --- CSS: 시인성 극대화 및 엔터 버튼 스타일 ---
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF !important; }
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; }
    
    /* 모든 텍스트 상시 선명하게 */
    .stage-desc, label, p, .stSubheader, .stMarkdown, .stInfo { 
        color: #FFFFFF !important; font-size: 1.1em !important; opacity: 1 !important; visibility: visible !important; font-weight: 500 !important;
    }

    /* 기본 버튼 스타일 (황금 그라데이션) */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; font-weight: 800 !important; border-radius: 8px !important;
        width: 100% !important; border: none !important; padding: 12px !important;
    }

    /* 🔴 핵심: ENTER 트리거 전용 버튼 스타일 */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, #FF4B4B, #D4AF37) !important; /* 더 강렬한 색상 */
        font-size: 1.2em !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.5);
    }

    /* 입력창 스타일 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important; color: #FFFFFF !important; border: 1px solid #484F58 !important; font-size: 1.05em !important;
    }
    
    .master-dialogue { 
        background-color: #2D2D2D; padding: 20px; border-radius: 12px; 
        border-left: 6px solid #D4AF37; margin-top: 15px; margin-bottom: 20px; color: #FFFFFF;
    }
    .master-name { color: #D4AF37; font-weight: bold; margin-right: 5px; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE 초기화] - 임시 저장소 생성
if 'interpretation_html' not in st.session_state:
    st.session_state.interpretation_html = None
if 'final_meaning_summary' not in st.session_state:
    st.session_state.final_meaning_summary = ""

# [CONNECTION: SUPABASE]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("수파베이스 연결 설정을 확인하세요.")

col_left, col_right = st.columns(2)

# --- LEFT PANEL ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    with st.form("left_raw_form"):
        st.markdown("<span class='stage-desc'>꿈의 내용을 기록하세요.</span>", unsafe_allow_html=True)
        dream_raw = st.text_area("", height=400, placeholder="내용 입력...")
        if st.form_submit_button("📓 원문만 저장하기"):
            if dream_raw:
                supabase.table("dreams").insert({"context": dream_raw}).execute()
                st.toast("✅ 원문 저장 완료!", icon="📓")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 리액티브 마스터 랩 ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    # === 폼 바깥 영역 (즉시 반응) ===
    st.subheader("🚀 Stage 1: 이미지 연상")
    # key를 지정하여 입력값이 유지되도록 함
    s1 = st.text_area("상징 나열", height=100, key="s1_input")

    st.subheader("🔍 Stage 2: 내적 역학")
    s2 = st.text_area("에너지 관계 분석", height=100, key="s2_input")

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    # 🔴 핵심: ENTER 트리거 버튼 (폼 바깥에 위치)
    # kind="primary"를 주어 위에서 정의한 특별한 CSS 스타일을 적용
    trigger_btn = st.button("↵ 마스터 통합 해석 가동 (ENTER)", type="primary", use_container_width=True)

    if trigger_btn:
        if s1 and s2:
            # 해석 생성 및 세션 상태에 저장
            st.session_state.interpretation_html = f"""
            <div class='master-dialogue'>
                <div><span class='master-name'>Jung & Johnson:</span> "{s1[:15]}...의 상징은 당신이 {s2[:15]}...의 현실 역동을 돌파하기 위해 무의식이 보낸 보상적 에너지입니다."</div>
                <br>
                <div><span class='master-name'>Koh Hye-kyung:</span> "이 꿈은 살아있습니다. 지금 이 에너지를 직면하는 것이 경제적 그릇을 키우는 가장 빠른 길입니다."</div>
            </div>
            """
            st.session_state.final_meaning_summary = f"[{s1.splitlines()[0] if s1 else '상징'}] 기반 에너지 직면 및 통합 전략"
            st.rerun() # 화면을 즉시 새로고침하여 해석을 보여줌
        else:
            st.warning("⚠️ Stage 1과 2를 모두 입력해야 마스터들이 응답합니다.")

    # === 해석 결과 표시 영역 ===
    if st.session_state.interpretation_html:
        st.subheader("📝 Stage 3: 마스터 통합 해석 결과")
        st.markdown(st.session_state.interpretation_html, unsafe_allow_html=True)

    # === 최종 제출 폼 (Stage 4 & 저장) ===
    with st.form("final_submit_form"):
        st.subheader("🏃 Stage 4: 현실 의례")
        st.info("💡 추천: '상징을 시각화하고, 오늘 당장 실행할 구체적 행동을 정하세요.'")
        s4 = st.text_input("나의 행동 확정", placeholder="예: 목표 도달을 위한 구체적 행동 1가지")

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if st.form_submit_button("🏛️ 최종 자산 금고 저장"):
            # 세션 상태에 저장된 해석 요약본과 현재 입력된 s1, s2, s4를 사용
            if s1 and s4 and st.session_state.final_meaning_summary:
                supabase.table("dreams").insert({
                    "symbol": s1, "block": s2, 
                    "meaning": st.session_state.final_meaning_summary, 
                    "ritual_self": s4
                    # 필요시 context에 dream_raw 추가 가능 (세션 관리 필요)
                }).execute()
                st.balloons()
                st.success("🎉 빌더님의 완전한 분석 자산이 기록되었습니다!")
                
                # 저장 후 세션 초기화 (선택 사항)
                st.session_state.interpretation_html = None
                st.session_state.final_meaning_summary = ""
                st.rerun()
            else:
                st.warning("⚠️ 상징, 의례, 그리고 마스터 해석 가동이 모두 완료되어야 합니다.")

    st.markdown("</div>", unsafe_allow_html=True)
