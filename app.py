import streamlit as st
from supabase import create_client, Client

# [SYSTEM CONFIG: CLEAN MODE & 50:50 LAYOUT]
st.set_page_config(page_title="D-Fi Vault v9.6", page_icon="🏛️", layout="wide")

# --- CSS: 상단 메뉴 삭제 & 버튼 가독성 유지 ---
st.markdown("""
    <style>
    /* 1. [핵심] 상단 스트림릿 기본 메뉴바 & 하단 푸터 삭제 (Clean View) */
    header, footer {
        visibility: hidden !important;
        height: 0px !important;
    }
    div[data-testid="stToolbar"] {
        visibility: hidden !important;
        display: none !important;
    }
    
    /* 2. 전체 테마 강제 (Deep Black) */
    .stApp {
        background-color: #050505 !important;
        color: #FFFFFF !important;
        margin-top: -50px !important; /* 헤더 삭제로 생긴 빈 공간 당기기 */
    }
    
    /* 3. 버튼 스타일 (황금색 + 검은 글씨 강제) */
    div[data-testid="stButton"] > button p,
    div[data-testid="stButton"] > button div,
    div[data-testid="stButton"] > button span {
        color: #000000 !important;
        font-weight: 900 !important;
    }
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        border: none !important;
        opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
    }

    /* 4. 삭제 버튼 예외 처리 (붉은색 + 흰 글씨) */
    div[data-testid="stButton"] > button:has(div:contains("삭제")) {
        background: linear-gradient(90deg, #FF5F6D, #FFC371) !important;
    }
    div[data-testid="stButton"] > button:has(div:contains("삭제")) p {
        color: #FFFFFF !important;
    }

    /* 5. 입력창 및 레이아웃 (Aethir Style) */
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    
    /* 6. 텍스트 가독성 */
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    .streamlit-expanderHeader { background-color: #222222 !important; color: #FFFFFF !important; }
    div[data-testid="stExpanderDetails"] { background-color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE]
if 'current_dream_id' not in st.session_state: st.session_state.current_dream_id = None
if 'dream_context' not in st.session_state: st.session_state.dream_context = ""
if 's1_val' not in st.session_state: st.session_state.s1_val = ""
if 's2_val' not in st.session_state: st.session_state.s2_val = ""
if 's4_val' not in st.session_state: st.session_state.s4_val = ""
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

# [CONNECTION]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB 연결 오류")

# --- LAYOUT ---
col_left, col_right = st.columns(2)

# ================= LEFT PANEL =================
with col_left:
    st.markdown("### 📓 무의식 원재료")
    st.markdown("꿈의 내용을 기록하세요. (30분의 정성)")
    
    with st.expander("📂 지난 꿈 불러오기", expanded=False):
        try:
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
            if res.data:
                for d in res.data:
                    c_l, c_r = st.columns([0.3, 0.7])
                    with c_l:
                        if st.button("로드", key=f"L_{d['id']}"):
                            st.session_state.current_dream_id = d['id']
                            st.session_state.dream_context = d.get('context', "")
                            st.session_state.s1_val = d.get('symbol', "")
                            st.session_state.s2_val = d.get('block', "")
                            st.session_state.s4_val = d.get('ritual_self', "")
                            # 토큰 발행 여부 체크
                            st.session_state.interpretation_ready = True if d.get('meaning') else False
                            st.session_state.is_minted = True if d.get('meaning') else False 
                            st.rerun()
                    with c_r:
                        st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
        except: st.write("데이터 없음")
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's4_val']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        st.session_state.interpretation_ready = False
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = "📝 원문 수정 모드 (토큰 발행 완료)" if st.session_state.is_minted and st.session_state.current_dream_id else "✨ 신규 작성 모드"
        st.caption(status)
        
        dream_raw = st.text_area("꿈 내용 입력", value=st.session_state.dream_context, height=450)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 원문 저장 (Save)"):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).execute()
                    st.toast("원문 수정 완료")
                else:
                    data = supabase.table("dreams").insert({"context": dream_raw}).execute()
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                        st.session_state.is_minted = False 
                        st.rerun()
        with c2:
            if st.session_state.current_dream_id:
                if st.form_submit_button("🗑️ 삭제 (Delete)"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.session_state.is_minted = False
                    st.rerun()

# ================= RIGHT PANEL =================
with col_right:
    st.markdown("### 🏛️ Master's Lab")
    
    st.text_area("🚀 Stage 1: 상징", value=st.session_state.s1_val, height=100, key="s1_key")
    st.text_area("🔍 Stage 2: 역학", value=st.session_state.s2_val, height=100, key="s2_key")
    
    if st.button("▼ 마스터 해석 가동 (ENTER)"):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        if s1_input and s2_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            st.session_state.interpretation_ready = True
        else: st.warning("입력 필요")

    if st.session_state.interpretation_ready:
        st.markdown(f"""
        <div style='background-color:#0A0A0A; border:1px solid #333; border-left:4px solid #D4AF37; padding:15px; margin-top:15px;'>
            <strong style='color:#D4AF37;'>🏛️ Insight:</strong><br>
            "{st.session_state.s1_val[:10]}..." 상징은 부의 그릇을 넓히는 열쇠입니다.
        </div>
        """, unsafe_allow_html=True)

    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: Asset Minting")
        s4 = st.text_input("🏃 의례 (Ritual)", value=st.session_state.s4_val)
        
        # 버튼 로직: 아직 발행 안 했으면 'Mint', 했으면 'Update'
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*5)
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "ritual_self": s4,
                    "meaning": f"Value: {token_val}"
                }
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                else:
                    payload["context"] = st.session_state.dream_context
                    data = supabase.table("dreams").insert(payload).execute()
                    if data.data: st.session_state.current_dream_id = data.data[0]['id']

                st.session_state.is_minted = True
                st.balloons()
                st.success(f"자산 발행 완료: {token_val} D-Fi Tokens")
                st.rerun()
