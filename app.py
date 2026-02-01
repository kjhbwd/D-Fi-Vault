import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM VIBE: SUPREME CLARITY & TOKEN ASSET]
st.set_page_config(page_title="D-Fi Vault v8.1", page_icon="🏛️", layout="wide")

# --- CSS: 상단 공백 제거 및 모든 요소 상시 노출 (호버 효과 완전 제거) ---
st.markdown("""
    <style>
    /* 1. 상단 불필요한 레이어 및 여백 삭제 */
    .block-container { padding-top: 1rem !important; }
    .stApp { background-color: #0E1117; color: #FFFFFF !important; }
    
    /* 2. 패널 디자인: 좌(기록), 우(연구) */
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; height: 100%; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; height: 100%; }
    
    /* 3. 🔴 핵심: 모든 설명글 및 라벨 상시 순백색 노출 */
    .stage-desc, label, p, .stSubheader, .stMarkdown, .stInfo { 
        color: #FFFFFF !important; 
        font-size: 1.1em !important; 
        opacity: 1 !important; 
        visibility: visible !important;
        font-weight: 500 !important;
        margin-bottom: 8px;
    }

    /* 4. 🔴 핵심: 모든 버튼 상시 선명하게 노출 (검은 텍스트로 가독성 확보) */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; 
        font-weight: 800 !important; 
        border-radius: 8px !important;
        width: 100% !important; 
        border: none !important; 
        padding: 12px !important;
        opacity: 1 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* 엔터(Enter) 마스터 가동 버튼 전용 강렬한 스타일 */
    div[data-testid="stButton"] > button[kind="primary"] {
        background: linear-gradient(90deg, #FF4B4B, #D4AF37) !important;
        font-size: 1.2em !important;
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }

    /* 입력창 내부 가독성 강화 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important;
        color: #FFFFFF !important;
        border: 1px solid #484F58 !important;
        font-size: 1.05em !important;
    }
    
    /* 토큰 발행 및 해석 결과 박스 */
    .token-msg { 
        background-color: #1A3A3A; color: #E0F2F1; padding: 20px; border-radius: 12px; 
        border-left: 6px solid #00BFA5; font-weight: bold; margin-top: 15px;
    }
    .master-dialogue { 
        background-color: #2D2D2D; padding: 20px; border-radius: 12px; 
        border-left: 6px solid #D4AF37; margin-top: 10px; margin-bottom: 20px;
    }
    .disclaimer { font-size: 0.85em; color: #8B949E; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE] - 폼 외부 버튼 작동을 위한 상태 관리
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False

# [CONNECTION: SUPABASE]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("수파베이스 설정 오류")
    st.stop()

col_left, col_right = st.columns(2)

# --- LEFT PANEL: 오늘 꿈 기록 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    with st.form("left_raw_form"):
        st.markdown("<span class='stage-desc'>꿈의 내용을 가감 없이 기록하세요. (30분의 정성)</span>", unsafe_allow_html=True)
        dream_raw = st.text_area("", height=450, placeholder="내용을 입력하면 상시 선명하게 보입니다.")
        
        # 🔴 버튼명 수정: 오늘 꿈 저장하기
        if st.form_submit_button("📓 오늘 꿈 저장하기"):
            if dream_raw:
                supabase.table("dreams").insert({"context": dream_raw}).execute()
                st.toast("✅ 오늘 꿈 원문이 금고에 저장되었습니다.", icon="📓")
            else: st.warning("내용을 입력해주세요.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 랩 & 토큰 발행 ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    # 📂 기존 기록 불러오기 우측 상단 배치
    if st.button("📂 기존 꿈/분석 자산 불러오기"):
        res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(3).execute()
        if res.data:
            for d in res.data:
                with st.expander(f"✨ {d['created_at'][:10]} | {d.get('symbol', '기록')[:15]}..."):
                    st.write(f"**해석:** {d.get('meaning')}")
                    st.write(f"**의례:** {d.get('ritual_self')}")

    st.markdown("<hr style='border: 0.5px solid #30363D;'>", unsafe_allow_html=True)

    # Stage 1 & 2 (폼 외부 배치하여 즉각 반응)
    st.subheader("🚀 Stage 1: 이미지 연상")
    s1 = st.text_area("강렬한 상징 추출 (줄바꿈 가능)", height=80, key="s1_lab")
    
    st.subheader("🔍 Stage 2: 내적 역학")
    s2 = st.text_area("현실의 에너지 관계 분석", height=80, key="s2_lab")

    # 🔴 엔터 트리거 버튼
    if st.button("↵ 마스터 통합 해석 가동 (ENTER)", type="primary"):
        if s1 and s2: st.session_state.interpretation_ready = True
        else: st.warning("Stage 1과 2를 먼저 입력해주세요.")

    # Stage 3: 해석 결과 노출
    if st.session_state.interpretation_ready:
        st.markdown(f"""
        <div class='master-dialogue'>
            <span style='color:#D4AF37; font-weight:bold;'>Master's Dialogue:</span><br>
            "{s1[:10]}... 상징은 당신의 현실 역동인 {s2[:10]}...을 돌파하기 위한 무의식의 선물입니다. 이를 통해 개성화의 길로 들어섭니다."
        </div>
        """, unsafe_allow_html=True)

    # Stage 4 & 최종 금고 저장
    with st.form("final_vault_form"):
        st.subheader("🏃 Stage 4: 현실 의례")
        s4 = st.text_input("나의 행동 확정", placeholder="오늘 당장 실행할 물리적 행동 하나")
        
        # 🔴 최종 자산 금고 저장 버튼
        if st.form_submit_button("🏛️ 최종 자산 금고 저장 (토큰 발행)"):
            if s1 and s4 and st.session_state.interpretation_ready:
                # 🔴 토큰 발행 로직 (최대 5,000점)
                base_score = 1000
                input_quality = len(s1 + s2 + s4) * 2  # 입력 길이에 따른 가중치
                token_score = min(5000, base_score + input_quality + random.randint(100, 500))
                
                # DB 저장 (토큰 점수 포함)
                save_data = {
                    "symbol": s1, "block": s2, "ritual_self": s4,
                    "meaning": f"통찰 자산 가치 {token_score} 발행 완료"
                }
                supabase.table("dreams").insert(save_data).execute()
                
                # 시각적 효과 및 메시지
                st.balloons()
                st.markdown(f"""
                <div class='token-msg'>
                    💎 [토큰 발행 완료] 빌더님, 대가들의 지혜가 담긴 데이터 자산이 성공적으로 기록되었습니다.<br>
                    🎖️ 이번 통찰의 자산 가치: {token_score:,} D-Fi Tokens
                </div>
                <p class='disclaimer'>* 본 가치는 무의식 작업에 대한 심리적 측정 지표이며 법정 화폐가 아닙니다.</p>
                """, unsafe_allow_html=True)
                st.session_state.interpretation_ready = False
            else:
                st.warning("모든 입력을 마치고 '해석 가동'을 먼저 클릭하세요.")

    st.markdown("</div>", unsafe_allow_html=True)
