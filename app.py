import streamlit as st
from supabase import create_client, Client
import time  # 🔴 [추가] 3초 딜레이를 위한 라이브러리

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v9.7", page_icon="🏛️", layout="wide")

# --- CSS: 버튼 가독성 '핵폭탄' 수정 & 테마 고정 ---
st.markdown("""
    <style>
    /* 1. 전체 테마: Deep Black 강제 */
    .stApp {
        background-color: #050505 !important;
        color: #FFFFFF !important;
    }
    
    /* 2. [최종 해결] 버튼 스타일 강제 주입 (우선순위 최상) */
    /* 모든 버튼의 배경을 황금색으로 */
    div[data-testid="stButton"] > button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        background-color: #D4AF37 !important;
        border: none !important;
        opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
        padding: 10px !important;
    }
    
    /* [핵심] 버튼 안의 '글자'를 감싸는 모든 태그를 검은색으로 강제 변환 */
    div[data-testid="stButton"] > button p, 
    div[data-testid="stButton"] > button div, 
    div[data-testid="stButton"] > button span {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 1rem !important;
        -webkit-text-fill-color: #000000 !important; /* 웹킷 브라우저 강제 */
    }

    /* 3. 마우스 호버(Hover) 시 스타일 */
    div[data-testid="stButton"] > button:hover {
        background: #FFD700 !important;
        transform: scale(1.02);
    }
    div[data-testid="stButton"] > button:hover p {
        color: #000000 !important;
    }

    /* 4. 삭제 버튼만 예외처리 (붉은색 + 흰글씨) */
    div[data-testid="stButton"] > button:has(div:contains("삭제")) {
        background: linear-gradient(90deg, #FF5F6D, #FFC371) !important;
    }
    div[data-testid="stButton"] > button:has(div:contains("삭제")) p {
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    /* 5. 입력창 및 레이아웃 */
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    
    /* 6. 기타 텍스트 가독성 */
    h1, h2, h3, p, label, .stMarkdown { color: #FFFFFF !important; }
    .streamlit-expanderHeader { background-color: #222222 !important; color: #FFFFFF !important; }
    div[data-testid="stExpanderDetails"] { background-color: #000000 !important; }
    
    /* 7. 헤더/푸터 숨김 */
    header, footer { visibility: hidden !important; }
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
if 'existing_value' not in st.session_state: st.session_state.existing_value = "" # 🔴 [추가] 기존 토큰 값 저장

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
                            # 토큰 발행 여부 및 기존 값 체크
                            meaning_text = d.get('meaning', "")
                            st.session_state.interpretation_ready = True if meaning_text else False
                            st.session_state.is_minted = True if meaning_text else False
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
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
        
        # 🔴 [기능 추가] 수정 모드일 때 '기존 자산 가치' 보여주기
        if st.session_state.is_minted and st.session_state.existing_value:
             st.info(f"💎 기존 자산 기록: {st.session_state.existing_value}")

        s4 = st.text_input("🏃 의례 (Ritual)", value=st.session_state.s4_val)
        
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                # 토큰 점수 계산
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*5)
                val_str = f"Value: {token_val} Tokens"
                
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "ritual_self": s4,
                    "meaning": val_str
                }
                
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).execute()
                else:
                    payload["context"] = st.session_state.dream_context
                    data = supabase.table("dreams").insert(payload).execute()
                    if data.data: st.session_state.current_dream_id = data.data[0]['id']

                st.session_state.is_minted = True
                st.session_state.existing_value = val_str # 업데이트된 값 반영
                
                # 🔴 [기능 추가] 풍선과 메시지를 3초간 보여주고 리런
                st.balloons()
                st.success(f"✅ 자산 발행/업데이트 완료! \n\n💰 {val_str}")
                time.sleep(3) # 3초 대기
                st.rerun()
