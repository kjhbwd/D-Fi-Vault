import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM VIBE: ASSET MANAGEMENT & CLARITY]
st.set_page_config(page_title="D-Fi Vault v8.2", page_icon="🏛️", layout="wide")

# --- CSS: 가독성 최적화 (상시 노출) ---
st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; }
    .stApp { background-color: #0E1117; color: #FFFFFF !important; }
    
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; height: 100%; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; height: 100%; }
    
    /* 텍스트 & 라벨 상시 선명하게 */
    .stage-desc, label, p, .stSubheader, .stMarkdown, .stInfo, .stExpander { 
        color: #FFFFFF !important; font-size: 1.1em !important; opacity: 1 !important; visibility: visible !important; font-weight: 500 !important;
    }

    /* 버튼 스타일 (상시 노출) */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #FFFFFF) !important;
        color: #000000 !important; font-weight: 800 !important; border-radius: 8px !important;
        width: 100% !important; border: none !important; padding: 12px !important;
        opacity: 1 !important;
    }
    
    /* 삭제 버튼 전용 스타일 (붉은색) */
    .delete-btn > button {
        background: linear-gradient(90deg, #FF4B4B, #FF8F8F) !important;
        color: #FFFFFF !important;
    }

    /* 입력창 스타일 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important; color: #FFFFFF !important; border: 1px solid #484F58 !important;
    }
    
    .token-msg { background-color: #1A3A3A; color: #E0F2F1; padding: 20px; border-radius: 12px; border-left: 6px solid #00BFA5; }
    .master-dialogue { background-color: #2D2D2D; padding: 20px; border-radius: 12px; border-left: 6px solid #D4AF37; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE: 데이터 관리용]
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

col_left, col_right = st.columns(2)

# ================= LEFT PANEL: 기록 & 관리 =================
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    # [기능 1] 꿈 목록 불러오기 (Load)
    with st.expander("📂 보관된 꿈 목록 (클릭하여 불러오기)", expanded=True):
        try:
            # 최근 5개만 불러오기
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
            if res.data:
                for d in res.data:
                    date_str = d['created_at'][:10]
                    preview = d.get('context', '내용 없음')[:15]
                    # 불러오기 버튼
                    if st.button(f"📄 {date_str} | {preview}...", key=f"load_{d['id']}"):
                        # 선택한 데이터 세션에 로드
                        st.session_state.current_dream_id = d['id']
                        st.session_state.dream_context = d.get('context', "")
                        st.session_state.s1_val = d.get('symbol', "")
                        st.session_state.s2_val = d.get('block', "")
                        st.session_state.s4_val = d.get('ritual_self', "")
                        st.session_state.interpretation_ready = True if d.get('meaning') else False
                        st.rerun() # 화면 새로고침
            else:
                st.info("저장된 꿈이 없습니다.")
        except Exception as e: st.error(f"로드 실패: {e}")

    # [기능 2] 신규 작성 모드로 초기화
    if st.button("🔄 새 꿈 기록하기 (초기화)"):
        st.session_state.current_dream_id = None
        st.session_state.dream_context = ""
        st.session_state.s1_val = ""
        st.session_state.s2_val = ""
        st.session_state.s4_val = ""
        st.session_state.interpretation_ready = False
        st.rerun()

    # [입력 폼]
    with st.form("left_raw_form"):
        mode_msg = f"수정 모드 (ID: {st.session_state.current_dream_id})" if st.session_state.current_dream_id else "신규 작성 모드"
        st.markdown(f"<span class='stage-desc'>{mode_msg} - 내용을 기록하세요.</span>", unsafe_allow_html=True)
        
        # 세션 값 바인딩
        dream_raw = st.text_area("", value=st.session_state.dream_context, height=400)
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.form_submit_button("💾 저장 / 수정"):
                if st.session_state.current_dream_id:
                    # [수정] UPDATE
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("✅ 내용이 수정되었습니다.", icon="📝")
                else:
                    # [신규] INSERT
                    data = supabase.table("dreams").insert({"context": dream_raw}).execute()
                    # 저장 후 바로 수정 모드로 전환
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                        st.rerun()
                    st.toast("✅ 새 꿈이 저장되었습니다.", icon="📓")
        
        with col_btn2:
            # [삭제] DELETE (수정 모드일 때만 작동)
            if st.session_state.current_dream_id:
                if st.form_submit_button("🗑️ 삭제하기", type="primary"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).execute()
                    # 삭제 후 초기화
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT PANEL: 마스터 랩 =================
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    st.markdown(f"<p class='stage-desc'>현재 분석 중인 자산 ID: {st.session_state.current_dream_id if st.session_state.current_dream_id else '신규'}</p>", unsafe_allow_html=True)

    # 폼 외부 입력 (즉각 반응용)
    st.subheader("🚀 Stage 1: 이미지 연상")
    s1 = st.text_area("상징", value=st.session_state.s1_val, height=80, key="s1_input")
    
    st.subheader("🔍 Stage 2: 내적 역학")
    s2 = st.text_area("역학", value=st.session_state.s2_val, height=80, key="s2_input")

    # 엔터 트리거
    if st.button("↵ 마스터 통합 해석 가동 (ENTER)", type="primary"):
        if s1 and s2: st.session_state.interpretation_ready = True

    if st.session_state.interpretation_ready:
        st.markdown(f"""
        <div class='master-dialogue'>
            <span style='color:#D4AF37; font-weight:bold;'>Master's Insight:</span><br>
            "{s1[:10]}... 상징은 당신의 현실 역동 {s2[:10]}...을(를) 재편성하려는 시그널입니다."
        </div>
        """, unsafe_allow_html=True)

    with st.form("final_vault_form"):
        st.subheader("🏃 Stage 4: 현실 의례")
        s4 = st.text_input("행동", value=st.session_state.s4_val, placeholder="구체적 행동")
        
        # 최종 저장 버튼
        btn_label = "🏛️ 수정 내용 업데이트" if st.session_state.current_dream_id else "🏛️ 최종 자산 금고 저장 (토큰 발행)"
        
        if st.form_submit_button(btn_label):
            if s1 and s4 and st.session_state.interpretation_ready:
                # 점수 계산
                token_score = min(5000, len(s1+s2+s4)*5 + 1000)
                
                payload = {
                    "symbol": s1, "block": s2, "ritual_self": s4,
                    "meaning": f"자산 가치 {token_score}"
                }
                
                if st.session_state.current_dream_id:
                    # [수정]
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("✅ 분석 내용이 업데이트되었습니다.", icon="🔄")
                else:
                    # [신규] (왼쪽 원문 없이 바로 오른쪽부터 쓸 경우)
                    payload["context"] = st.session_state.dream_context # 왼쪽 내용 포함
                    data = supabase.table("dreams").insert(payload).execute()
                    if data.data: st.session_state.current_dream_id = data.data[0]['id']
                    
                    st.balloons()
                    st.markdown(f"""
                    <div class='token-msg'>
                        💎 [토큰 발행] 자산 가치: {token_score:,} D-Fi Tokens
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("모든 단계를 완료해주세요.")

    st.markdown("</div>", unsafe_allow_html=True)
