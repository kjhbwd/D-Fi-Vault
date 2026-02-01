import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM VIBE: AETHIR GUIDE STYLE - CLEAN & HIGH CONTRAST]
st.set_page_config(page_title="D-Fi Smart Guide", page_icon="📙", layout="centered")

# --- CSS: 에이셔 가이드 색감 및 버튼 가독성 완전 해결 ---
st.markdown("""
    <style>
    /* 1. 배경 및 폰트: 에이셔 가이드의 Deep Dark 테마 적용 */
    .stApp { 
        background-color: #050505 !important; /* 더 깊은 검정 */
        color: #E6E6E6 !important; /* 눈이 편안한 밝은 회색 */
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* 2. 타이틀 스타일: 깔끔하고 모던하게 */
    .guide-title {
        font-size: 2.2em; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em; margin-bottom: 0.2em;
    }
    .guide-subtitle {
        font-size: 1.0em; color: #888888; margin-bottom: 2.5em; border-bottom: 1px solid #333333; padding-bottom: 15px;
    }

    /* 3. 챕터(Expander) 스타일: 가이드북의 섹션 느낌 */
    .streamlit-expanderHeader {
        background-color: #111111 !important; /* 아주 어두운 회색 */
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderContent {
        background-color: #0A0A0A !important;
        border: 1px solid #333333 !important;
        border-top: none !important;
        color: #CCCCCC !important;
    }

    /* 4. 🔴 핵심 수정: 버튼 가독성 및 '끝글자 흐림' 해결 */
    .stButton > button {
        /* 황금색 그라데이션 유지하되, 텍스트 가독성 최우선 */
        background: linear-gradient(90deg, #FFD700 0%, #FDB931 100%) !important;
        color: #000000 !important; /* ⚠️ 완전한 검정색 글자로 고정 */
        font-weight: 800 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        opacity: 1 !important; /* 상시 노출 */
        text-shadow: none !important; /* 그림자 제거 (흐림 원인 차단) */
        transition: transform 0.1s ease;
    }
    .stButton > button:hover {
        transform: scale(1.01); /* 호버 시 살짝 커지는 효과만 줌 (색상 변경 X) */
        color: #000000 !important;
    }
    
    /* 삭제 버튼 (붉은 계열) */
    .delete-btn > button {
        background: linear-gradient(90deg, #FF5F6D, #FFC371) !important;
        color: #FFFFFF !important;
    }

    /* 5. 입력창 및 텍스트 상시 노출 */
    .stTextArea textarea, .stTextInput input {
        background-color: #161616 !important; 
        color: #FFFFFF !important; 
        border: 1px solid #444444 !important;
        font-size: 1rem !important;
    }
    /* 라벨, 설명글 등 모든 텍스트 강제 흰색/밝은회색 */
    p, label, .stMarkdown, div[data-testid="stMarkdownContainer"] {
        color: #E6E6E6 !important; opacity: 1 !important; visibility: visible !important;
    }

    /* 토큰 박스 스타일 */
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
except: st.error("데이터베이스 연결 실패")

# --- HEADER ---
st.markdown("<div class='guide-title'>D-Fi Smart Guide</div>", unsafe_allow_html=True)
st.markdown("""
<div class='guide-subtitle'>
    <b>무의식의 미래를 선점하라 (Chapter Ver.)</b><br>
    KO / EN | 챕터를 클릭하여 꿈 자산화 작업을 수행하세요.
</div>
""", unsafe_allow_html=True)

# --- PROLOGUE: LOAD ---
with st.expander("📂 Prologue: 내 자산 불러오기 (Load)", expanded=False):
    st.info("기록된 꿈 자산 목록입니다. 클릭하면 수정 모드로 진입합니다.")
    try:
        res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data:
            for d in res.data:
                col1, col2 = st.columns([0.25, 0.75])
                with col1:
                    if st.button("로드", key=f"load_{d['id']}"):
                        st.session_state.current_dream_id = d['id']
                        st.session_state.dream_context = d.get('context', "")
                        st.session_state.s1_val = d.get('symbol', "")
                        st.session_state.s2_val = d.get('block', "")
                        st.session_state.s4_val = d.get('ritual_self', "")
                        st.session_state.interpretation_ready = True if d.get('meaning') else False
                        st.rerun()
                with col2:
                    summary = d.get('context', '내용 없음')[:25].replace("\n", " ")
                    st.write(f"**{d['created_at'][5:10]}**: {summary}...")
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

# --- CHAPTER 1: RECORD ---
with st.expander("📓 Chapter 1: 무의식 원재료 (Record)", expanded=True):
    status = f"📝 수정 모드 (ID: {st.session_state.current_dream_id})" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
    st.caption(status)
    
    with st.form("ch1_form"):
        st.markdown("**꿈의 내용을 기록하세요 (30분의 정성)**")
        dream_raw = st.text_area("내용 입력", value=st.session_state.dream_context, height=250, label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 챕터 1 저장하기"):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("내용이 수정되었습니다.")
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

# --- CHAPTER 2: ANALYSIS ---
with st.expander("🚀 Chapter 2: Master's Lab (Analysis)", expanded=True):
    st.markdown("**Stage 1: 이미지 연상**")
    s1 = st.text_area("강렬한 상징", value=st.session_state.s1_val, height=80, key="s1_key")
    
    st.markdown("**Stage 2: 내적 역학**")
    s2 = st.text_area("현실의 에너지 역학", value=st.session_state.s2_val, height=80, key="s2_key")
    
    st.markdown("---")
    # 트리거 버튼 (가독성 강화)
    if st.button("▼ 마스터 통합 해석 가동 (ENTER)"):
        if s1 and s2: st.session_state.interpretation_ready = True
        else: st.warning("상징과 역학을 입력하세요.")

# --- CHAPTER 3: INSIGHT ---
if st.session_state.interpretation_ready:
    with st.expander("📝 Chapter 3: Master's Insight (Result)", expanded=True):
        st.markdown(f"""
        <div class='token-box' style='border-left-color: #D4AF37;'>
            <strong style='color:#D4AF37; font-size:1.1em;'>🏛️ Master's Dialogue</strong><br><br>
            "{s1[:10]}..." 상징은 당신의 현실 속 "{s2[:10]}..." 역동을 돌파하기 위한 무의식의 선물입니다.
            <br><br>
            <i>"이 에너지를 회피하지 말고 직면하십시오. 그것이 부의 그릇을 넓히는 길입니다."</i>
        </div>
        """, unsafe_allow_html=True)

# --- CHAPTER 4: MINTING ---
with st.expander("💎 Chapter 4: Asset Minting (Token)", expanded=True):
    with st.form("mint_form"):
        st.markdown("**Stage 4: 현실 의례 (Ritual)**")
        s4 = st.text_input("오늘 실행할 행동", value=st.session_state.s4_val)
        
        st.markdown("---")
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.current_dream_id else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if s1 and s4 and st.session_state.interpretation_ready:
                # 토큰 계산
                token_val = min(5000, 1000 + len(s1+s2+s4)*5)
                
                payload = {
                    "symbol": s1, "block": s2, "ritual_self": s4,
                    "meaning": f"Asset Value: {token_val}"
                }
                
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("자산 정보 업데이트 완료")
                else:
                    payload["context"] = st.session_state.dream_context
                    supabase.table("dreams").insert(payload).execute()
                
                st.balloons()
                st.markdown(f"""
                <div class='token-box'>
                    <h3 style='margin:0; color:#FDB931;'>💎 Token Minted</h3>
                    <p style='margin:10px 0; font-size:1.2em;'>발행된 자산 가치: <b>{token_val:,} D-Fi Tokens</b></p>
                    <span style='font-size:0.8em; color:#888;'>* 본 가치는 심리적 자산 지표입니다.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("분석 단계를 모두 완료해주세요.")
