import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM VIBE: FORCE DARK THEME & AETHIR STYLE]
st.set_page_config(page_title="D-Fi Smart Guide", page_icon="📙", layout="centered")

# --- CSS: 테마 강제 주입 및 화이트 플래시(White Flash) 제거 ---
st.markdown("""
    <style>
    /* 1. [핵심] 시스템 테마 무시하고 다크 모드 변수 강제 주입 */
    :root {
        --primary-color: #D4AF37;
        --background-color: #050505;
        --secondary-background-color: #111111;
        --text-color: #E6E6E6;
        --font: sans-serif;
    }
    
    /* 2. 전체 앱 배경 강제 설정 */
    .stApp {
        background-color: #050505 !important;
        color: #E6E6E6 !important;
    }

    /* 3. [문제 해결] 챕터 박스(Expander)가 하얗게 나오는 현상 제거 */
    /* 헤더 (눌러서 펼치는 부분) */
    .streamlit-expanderHeader {
        background-color: #161616 !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
    }
    /* 바디 (펼쳐진 내용 부분) - image_3ffc60.png의 하얀 배경 범인 */
    div[data-testid="stExpander"] > details > div {
        background-color: #0A0A0A !important;
        border: 1px solid #333333 !important;
        border-top: none !important;
        color: #E6E6E6 !important;
    }
    /* Expander 내부의 모든 텍스트 강제 흰색 */
    div[data-testid="stExpander"] p, 
    div[data-testid="stExpander"] label, 
    div[data-testid="stExpander"] span {
        color: #E6E6E6 !important;
    }

    /* 4. [문제 해결] 버튼 스타일 - 가독성 끝판왕 */
    .stButton > button {
        background: linear-gradient(90deg, #FFD700 0%, #FDB931 100%) !important;
        color: #000000 !important; /* 완전 검정 글씨 */
        font-weight: 900 !important; /* 더 두껍게 */
        border: none !important;
        padding: 0.8rem 1rem !important;
        border-radius: 4px !important;
        opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3); /* 입체감 추가 */
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #FDB931 0%, #FFD700 100%) !important;
        color: #000000 !important;
        transform: translateY(-1px);
    }
    /* 버튼 내부 텍스트 컨테이너 강제 검정 (스트림릿 내부 구조 침투) */
    .stButton > button p {
        color: #000000 !important;
    }

    /* 5. 입력창 스타일 (다크 모드 유지) */
    .stTextArea textarea, .stTextInput input {
        background-color: #161616 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    /* 입력창 라벨 숨기거나 색상 변경 */
    .stTextArea label, .stTextInput label {
        color: #CCCCCC !important;
    }

    /* 6. 타이틀 및 기타 */
    .guide-title {
        font-size: 2.2em; font-weight: 700; color: #FFFFFF; margin-bottom: 0.2em;
    }
    .guide-subtitle {
        font-size: 1.0em; color: #888888; margin-bottom: 2em; border-bottom: 1px solid #333333; padding-bottom: 15px;
    }
    .token-box {
        background-color: #111111; border: 1px solid #333333; border-left: 4px solid #FDB931; 
        padding: 20px; border-radius: 4px; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE]
if 'current_dream_id' not in st.session_state: st.session_state.current_dream_id = None
if 'dream_context' not in st.session_state: st.session_state.dream_context = ""
if 's1_val' not in st.session_state: st.session_state.s1_val = ""
if 's2_val' not in st.session_state: st.session_state.s2_val = ""
if 's4_val' not in st.session_state: st.session_state.s4_val = ""
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False

# [CONNECTION]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB 연결 실패")

# --- HEADER ---
st.markdown("<div class='guide-title'>D-Fi Smart Guide</div>", unsafe_allow_html=True)
st.markdown("""
<div class='guide-subtitle'>
    <b>무의식의 미래를 선점하라 (Dark Mode Ver.)</b><br>
    KO / EN | 챕터를 클릭하여 꿈 자산화 작업을 수행하세요.
</div>
""", unsafe_allow_html=True)

# --- PROLOGUE ---
with st.expander("📂 Prologue: 내 자산 불러오기 (Load)", expanded=False):
    st.info("기록된 꿈 자산 목록입니다. (수정 모드 진입)")
    try:
        res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data:
            for d in res.data:
                col1, col2 = st.columns([0.2, 0.8])
                with col1:
                    if st.button("로드", key=f"ld_{d['id']}"):
                        st.session_state.current_dream_id = d['id']
                        st.session_state.dream_context = d.get('context', "")
                        st.session_state.s1_val = d.get('symbol', "")
                        st.session_state.s2_val = d.get('block', "")
                        st.session_state.s4_val = d.get('ritual_self', "")
                        st.session_state.interpretation_ready = True if d.get('meaning') else False
                        st.rerun()
                with col2:
                    st.write(f"**{d['created_at'][:10]}**: {d.get('context', '')[:20]}...")
        else:
            st.write("저장된 기록이 없습니다.")
    except: pass
    
    st.markdown("---")
    if st.button("🔄 초기화 (새로운 꿈 기록하기)"):
        st.session_state.current_dream_id = None
        st.session_state.dream_context = ""
        st.session_state.s1_val = ""
        st.session_state.s2_val = ""
        st.session_state.s4_val = ""
        st.session_state.interpretation_ready = False
        st.rerun()

# --- CHAPTER 1 ---
with st.expander("📓 Chapter 1: 무의식 원재료 (Record)", expanded=True):
    status = f"📝 수정 모드 (ID: {st.session_state.current_dream_id})" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
    st.caption(status)
    
    with st.form("ch1_form"):
        st.markdown("**꿈의 내용을 기록하세요 (30분의 정성)**")
        dream_raw = st.text_area("내용 입력", value=st.session_state.dream_context, height=250, label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            # 버튼 텍스트 색상 강제 검정 확인
            if st.form_submit_button("💾 챕터 1 저장하기"):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("수정 완료")
                else:
                    data = supabase.table("dreams").insert({"context": dream_raw}).execute()
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                        st.rerun()
        with c2:
            if st.session_state.current_dream_id:
                if st.form_submit_button("🗑️ 삭제하기"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.rerun()

# --- CHAPTER 2 ---
with st.expander("🚀 Chapter 2: Master's Lab (Analysis)", expanded=True):
    st.markdown("**Stage 1: 이미지 연상**")
    s1 = st.text_area("강렬한 상징", value=st.session_state.s1_val, height=80)
    
    st.markdown("**Stage 2: 내적 역학**")
    s2 = st.text_area("현실의 에너지 역학", value=st.session_state.s2_val, height=80)
    
    st.markdown("---")
    if st.button("▼ 마스터 통합 해석 가동 (ENTER)"):
        if s1 and s2: st.session_state.interpretation_ready = True
        else: st.warning("내용을 입력하세요.")

# --- CHAPTER 3 ---
if st.session_state.interpretation_ready:
    with st.expander("📝 Chapter 3: Master's Insight (Result)", expanded=True):
        st.markdown(f"""
        <div class='token-box' style='border-left-color: #D4AF37;'>
            <strong style='color:#D4AF37; font-size:1.1em;'>🏛️ Master's Dialogue</strong><br><br>
            "{s1[:10]}..." 상징은 당신의 현실 속 "{s2[:10]}..." 역동을 돌파하기 위한 무의식의 선물입니다.
        </div>
        """, unsafe_allow_html=True)

# --- CHAPTER 4 ---
with st.expander("💎 Chapter 4: Asset Minting (Token)", expanded=True):
    with st.form("mint_form"):
        st.markdown("**Stage 4: 현실 의례 (Ritual)**")
        s4 = st.text_input("오늘 실행할 행동", value=st.session_state.s4_val)
        
        st.markdown("---")
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.current_dream_id else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if s1 and s4 and st.session_state.interpretation_ready:
                token_val = min(5000, 1000 + len(s1+s2+s4)*5)
                
                payload = {
                    "symbol": s1, "block": s2, "ritual_self": s4,
                    "meaning": f"Asset Value: {token_val}"
                }
                
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("업데이트 완료")
                else:
                    payload["context"] = st.session_state.dream_context
                    supabase.table("dreams").insert(payload).execute()
                
                st.balloons()
                st.markdown(f"""
                <div class='token-box'>
                    <h3 style='margin:0; color:#FDB931;'>💎 Token Minted</h3>
                    <p style='margin:10px 0; font-size:1.2em;'>발행된 자산 가치: <b>{token_val:,} D-Fi Tokens</b></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("분석을 완료해주세요.")
