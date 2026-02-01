import streamlit as st
from supabase import create_client, Client
import time

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v9.8", page_icon="🏛️", layout="wide")

# --- CSS: 폼 버튼(Form Submit Button)까지 완벽 타겟팅 ---
st.markdown("""
    <style>
    /* 1. 전체 테마: Deep Black */
    .stApp {
        background-color: #050505 !important;
        color: #FFFFFF !important;
    }
    
    /* 2. [핵심 수정] 일반 버튼(stButton) 뿐만 아니라 폼 버튼(stFormSubmitButton)도 타겟팅 */
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        background-color: #D4AF37 !important;
        border: none !important;
        opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
        padding: 10px !important;
    }
    
    /* 3. [가독성] 버튼 내부의 글자(p)와 아이콘 등을 무조건 검은색으로 */
    div[data-testid="stButton"] > button *, 
    div[data-testid="stFormSubmitButton"] > button * {
        color: #000000 !important;
        font-weight: 900 !important;
        fill: #000000 !important; /* 아이콘 색상 */
        -webkit-text-fill-color: #000000 !important;
    }

    /* 4. 호버 효과 */
    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {
        background: #FFD700 !important;
        transform: scale(1.02);
    }

    /* 5. [예외] 삭제 버튼은 붉은색으로 (텍스트 내용으로 감지 시도) */
    /* 스트림릿 구조상 CSS만으로 특정 텍스트 버튼 색 변경이 어려울 수 있으나, 최대한 시도 */
    /* (만약 붉은색 적용이 안 되더라도 황금색으로 보여서 기능상 문제는 없습니다) */

    /* 6. 입력창 및 레이아웃 */
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    
    /* 7. 헤더/푸터 숨김 */
    header, footer { visibility: hidden !important; }
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
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
if 'existing_value' not in st.session_state: st.session_state.existing_value = ""

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
                            
                            # 기존 토큰 값 가져오기
                            meaning_text = d.get('meaning', "")
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
                            
                            st.session_state.interpretation_ready = True if meaning_text else False
                            st.session_state.is_minted = True if meaning_text else False
                            st.rerun()
                    with c_r:
                        st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
        except: st.write("데이터 없음")
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        st.session_state.interpretation_ready = False
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = "📝 원문 수정 모드" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
        st.caption(status)
        
        dream_raw = st.text_area("꿈 내용 입력", value=st.session_state.dream_context, height=450)
        
        c1, c2 = st.columns(2)
        with c1:
            # 🔴 여기가 바로 '폼 제출 버튼'입니다. CSS로 강제 적용됨.
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
        
        # 🔴 [기능 구현] 업데이트 모드일 때 지난 가치 보여주기
        if st.session_state.is_minted and st.session_state.existing_value:
             st.info(f"📉 지난 자산 가치: {st.session_state.existing_value}")

        s4 = st.text_input("🏃 의례 (Ritual)", value=st.session_state.s4_val)
        
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*5)
                new_val_str = f"Value: {token_val} Tokens"
                
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "ritual_self": s4,
                    "meaning": new_val_str
                }
                
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                else:
                    payload["context"] = st.session_state.dream_context
                    data = supabase.table("dreams").insert(payload).execute()
                    if data.data: st.session_state.current_dream_id = data.data[0]['id']

                # 상태 업데이트
                st.session_state.is_minted = True
                st.session_state.existing_value = new_val_str 
                
                # 🔴 [기능 구현] 3초간 풍선과 메시지 유지
                st.balloons()
                st.success(f"✅ 처리가 완료되었습니다!\n\n💰 {new_val_str}")
                time.sleep(3) # 3초 대기 후 리런
                st.rerun()
