import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM VIBE: SMART GUIDEBOOK LAYOUT]
# 가이드북 스타일은 집중도를 위해 'centered' 레이아웃이 훨씬 적합합니다.
st.set_page_config(page_title="D-Fi Smart Guide", page_icon="📙", layout="centered")

# --- CSS: 스마트 가이드 스타일링 (Aethir Guide Vibe) ---
st.markdown("""
    <style>
    /* 1. 전체 폰트 및 배경: 가이드북의 깔끔한 다크 모드 */
    .stApp { background-color: #0E1117; color: #FFFFFF !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* 2. 타이틀 영역 스타일 */
    .guide-title {
        font-size: 2.5em; font-weight: 800; color: #FFFFFF; margin-bottom: 0.2em; text-align: left;
    }
    .guide-subtitle {
        font-size: 1.2em; color: #8B949E; margin-bottom: 2em; text-align: left; border-bottom: 1px solid #30363D; padding-bottom: 20px;
    }

    /* 3. 챕터(Expander) 스타일 재정의 */
    .streamlit-expanderHeader {
        background-color: #161B22 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: 1px solid #30363D !important;
        border-radius: 8px !important;
        font-size: 1.1em !important;
    }
    
    /* 4. 가독성: 모든 텍스트 상시 노출 (호버 이슈 해결) */
    p, label, .stMarkdown, .stInfo {
        color: #FFFFFF !important; opacity: 1 !important; visibility: visible !important;
    }
    
    /* 5. 버튼 스타일: 가이드북의 액션 버튼 */
    .stButton>button {
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; font-weight: 800 !important; border-radius: 6px !important;
        border: none !important; width: 100% !important; padding: 12px !important;
        margin-top: 10px;
    }
    
    /* 삭제 버튼 (붉은 계열) */
    .delete-btn button {
        background: linear-gradient(90deg, #FF5252, #FF8A80) !important; color: white !important;
    }

    /* 입력창 디자인 */
    .stTextArea textarea, .stTextInput input {
        background-color: #0d1117 !important; color: #c9d1d9 !important; border: 1px solid #30363D !important;
    }

    /* 토큰 메시지 박스 */
    .token-box {
        background-color: #1F2937; border-left: 5px solid #10B981; padding: 20px; margin-top: 20px; border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE: 데이터 관리]
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
except: st.error("DB 연결 오류")

# --- HEADER: 가이드북 표지 ---
st.markdown("<div class='guide-title'>D-Fi Guide: Dream Insight</div>", unsafe_allow_html=True)
st.markdown("""
<div class='guide-subtitle'>
    <b>무의식의 미래를 선점하라</b><br>
    KO / EN | * 챕터를 클릭하면 상세 작업 도구가 펼쳐집니다.<br>
    <span style='font-size:0.8em; color:#D4AF37;'>⚠️ 본 가이드의 토큰은 심리적 자산 지표입니다.</span>
</div>
""", unsafe_allow_html=True)

# --- CHAPTER 0: 데이터 불러오기 (PROLOGUE) ---
with st.expander("📂 Prologue: 자산 불러오기 (Load)", expanded=False):
    st.info("과거에 기록한 꿈 자산을 불러와 수정하거나 삭제할 수 있습니다.")
    try:
        res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
        if res.data:
            for d in res.data:
                col_load, col_desc = st.columns([0.2, 0.8])
                with col_load:
                    if st.button("로드", key=f"btn_{d['id']}"):
                        st.session_state.current_dream_id = d['id']
                        st.session_state.dream_context = d.get('context', "")
                        st.session_state.s1_val = d.get('symbol', "")
                        st.session_state.s2_val = d.get('block', "")
                        st.session_state.s4_val = d.get('ritual_self', "")
                        st.session_state.interpretation_ready = True if d.get('meaning') else False
                        st.rerun()
                with col_desc:
                    st.write(f"**{d['created_at'][:10]}**: {d.get('context', '')[:30]}...")
        else:
            st.write("저장된 기록이 없습니다.")
    except: st.error("불러오기 실패")
    
    if st.button("🔄 새로운 꿈 기록 시작하기 (초기화)"):
        st.session_state.current_dream_id = None
        st.session_state.dream_context = ""
        st.session_state.s1_val = ""
        st.session_state.s2_val = ""
        st.session_state.s4_val = ""
        st.session_state.interpretation_ready = False
        st.rerun()

# --- CHAPTER 1: 무의식 원재료 ---
with st.expander("📓 Chapter 1: 무의식 원재료 (Record)", expanded=True):
    mode_text = f"현재 모드: 수정 (ID {st.session_state.current_dream_id})" if st.session_state.current_dream_id else "현재 모드: 신규 작성"
    st.caption(mode_text)
    
    with st.form("guide_ch1_form"):
        st.markdown("**꿈의 내용을 가감 없이 기록하세요 (30분의 정성)**")
        dream_raw = st.text_area("내용 입력", value=st.session_state.dream_context, height=300, label_visibility="collapsed")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 챕터 1 저장/수정"):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("업데이트 완료")
                else:
                    data = supabase.table("dreams").insert({"context": dream_raw}).execute()
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                        st.rerun()
        with c2:
            if st.session_state.current_dream_id:
                if st.form_submit_button("🗑️ 이 꿈 삭제하기"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.rerun()

# --- CHAPTER 2: 마스터의 연구실 ---
with st.expander("🚀 Chapter 2: Master's Lab (Analysis)", expanded=True):
    st.markdown("**Stage 1: 이미지 연상**")
    s1 = st.text_area("강렬한 상징", value=st.session_state.s1_val, height=80, key="guide_s1")
    
    st.markdown("**Stage 2: 내적 역학**")
    s2 = st.text_area("현실의 에너지 역학", value=st.session_state.s2_val, height=80, key="guide_s2")
    
    # 가이드북 스타일의 트리거 버튼
    st.markdown("---")
    if st.button("▼ 마스터 통합 해석 요청 (ENTER)"):
        if s1 and s2: st.session_state.interpretation_ready = True
        else: st.warning("위 상징과 역학 내용을 먼저 입력하세요.")

# --- CHAPTER 3: 통찰의 결과 ---
if st.session_state.interpretation_ready:
    with st.expander("📝 Chapter 3: Master's Insight (Result)", expanded=True):
        st.info("마스터들의 대화가 도착했습니다.")
        st.markdown(f"""
        <div style='background-color:#21262D; padding:15px; border-radius:8px; border-left:4px solid #D4AF37;'>
            <span style='color:#D4AF37; font-weight:bold;'>Carl Jung & Johnson:</span><br><br>
            "{s1[:15]}..."<br>
            이 상징은 당신의 현실 속 "{s2[:15]}..."라는 갈등을 해결하기 위한 무의식의 정교한 설계입니다. 
            지금 이 에너지를 회피하지 말고 직면하십시오. 그것이 부의 그릇을 넓히는 길입니다.
        </div>
        """, unsafe_allow_html=True)

# --- CHAPTER 4: 자산 발행 ---
with st.expander("💎 Chapter 4: Asset Minting (Token)", expanded=True):
    with st.form("guide_mint_form"):
        st.markdown("**Stage 4: 현실 의례 (Ritual)**")
        s4 = st.text_input("오늘 당장 실행할 행동", value=st.session_state.s4_val)
        
        st.markdown("---")
        btn_text = "🏛️ 수정 내역 업데이트" if st.session_state.current_dream_id else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(btn_text):
            if s1 and s4 and st.session_state.interpretation_ready:
                # 토큰 가중치 계산 (가이드북 로직)
                base = 1000
                bonus = len(s1+s2+s4) * 5
                token_val = min(5000, base + bonus)
                
                payload = {
                    "symbol": s1, "block": s2, "ritual_self": s4,
                    "meaning": f"Asset Value: {token_val}"
                }
                
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("자산 정보가 업데이트되었습니다.")
                else:
                    payload["context"] = st.session_state.dream_context
                    supabase.table("dreams").insert(payload).execute()
                
                st.balloons()
                st.markdown(f"""
                <div class='token-box'>
                    <h3>💎 Token Minted Successfully</h3>
                    <p>발행된 통찰 자산 가치: <b>{token_val:,} D-Fi Tokens</b></p>
                    <span style='font-size:0.8em; color:#9CA3AF;'>* 이 자산은 귀하의 계정에 영구 기록됩니다.</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("이전 챕터의 분석을 완료해주세요.")
