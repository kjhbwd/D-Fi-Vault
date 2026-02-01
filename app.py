import streamlit as st
from supabase import create_client, Client

# [SYSTEM CONFIG: 50:50 LAYOUT]
st.set_page_config(page_title="D-Fi Vault v9.4", page_icon="🏛️", layout="wide")

# --- CSS: 버튼 하얀색 박멸 및 가독성 강제 ---
st.markdown("""
    <style>
    /* 1. 전체 테마 강제 (Dark Mode Force) */
    .stApp {
        background-color: #050505 !important;
        color: #FFFFFF !important;
    }
    
    /* 2. [최후의 수단] 버튼 스타일 강제 덮어쓰기 (모든 버튼 타겟팅) */
    button, 
    div[data-testid="stButton"] > button, 
    div[data-testid="baseButton-secondary"] {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        background-color: #D4AF37 !important; /* 그라데이션 실패 시 단색 백업 */
        color: #000000 !important; /* 글자는 무조건 검정 */
        border: none !important;
        font-weight: 900 !important;
        opacity: 1 !important;
        text-shadow: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
    }

    /* 버튼 내부 텍스트(p, div)까지 검정색 강제 전파 */
    button *, 
    div[data-testid="stButton"] > button *, 
    div[data-testid="baseButton-secondary"] * {
        color: #000000 !important;
    }

    /* 호버(마우스 올림), 포커스, 액티브 상태에서도 무조건 황금색 유지 */
    button:hover, button:focus, button:active,
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stButton"] > button:focus,
    div[data-testid="stButton"] > button:active {
        background: linear-gradient(90deg, #FDB931 0%, #FFD700 100%) !important;
        color: #000000 !important;
        border: none !important;
        outline: none !important;
        box-shadow: 0 0 10px #D4AF37 !important;
    }

    /* 3. 삭제 버튼만 붉은색으로 예외 처리 (CSS 우선순위 높임) */
    div[data-testid="column"] button:contains("삭제"), 
    div[data-testid="stButton"] > button:has(div:contains("삭제")) {
         background: linear-gradient(90deg, #FF5F6D, #FFC371) !important;
         color: #FFFFFF !important;
    }
    /* (위의 :has 선택자가 안 먹힐 경우를 대비한 붉은 버튼 클래스 별도 지정 불가하므로 전체 적용) 
       *참고: 스트림릿에서 특정 버튼만 색을 바꾸는 건 까다롭지만, 일단 전체 황금색이 급선무입니다. */

    /* 4. 입력창 및 레이아웃 스타일 (Aethir Guide) */
    div[data-testid="column"] {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 8px;
        padding: 20px;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important;
        color: #FFFFFF !important;
        border: 1px solid #666666 !important; /* 테두리 더 진하게 */
    }
    
    /* 5. 텍스트 가독성 */
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    
    /* 6. Expander 스타일 */
    .streamlit-expanderHeader {
        background-color: #222222 !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    div[data-testid="stExpanderDetails"] {
        background-color: #000000 !important;
        border: 1px solid #444444 !important;
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
                            st.session_state.interpretation_ready = True if d.get('meaning') else False
                            st.rerun()
                    with c_r:
                        st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
        except: st.write("데이터 없음")
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        st.session_state.current_dream_id = None
        st.session_state.dream_context = ""
        st.session_state.s1_val = ""
        st.session_state.s2_val = ""
        st.session_state.s4_val = ""
        st.session_state.interpretation_ready = False
        st.rerun()

    with st.form("left_form"):
        status = f"📝 수정 모드 (ID: {st.session_state.current_dream_id})" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
        st.caption(status)
        dream_raw = st.text_area("꿈 내용 입력", value=st.session_state.dream_context, height=450)
        
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 원문 저장 (Save)"):
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
                if st.form_submit_button("🗑️ 삭제 (Delete)"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
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
        
        final_btn = "🏛️ 업데이트" if st.session_state.current_dream_id else "💎 토큰 발행 (Mint)"
        
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
                    supabase.table("dreams").insert(payload).execute()
                st.balloons()
                st.success(f"자산 발행 완료: {token_val} D-Fi Tokens")
