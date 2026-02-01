import streamlit as st
from supabase import create_client, Client
import datetime
import random

# [SYSTEM CONFIG: 50:50 LAYOUT & WIDE MODE]
st.set_page_config(page_title="D-Fi Vault v9.3", page_icon="🏛️", layout="wide")

# --- CSS: 에이셔 가이드 스타일 강제 주입 (Aethir Style Injection) ---
st.markdown("""
    <style>
    /* 1. [핵심] 시스템 테마 무시 - 강제 다크 모드 변수 선언 */
    :root {
        --primary-color: #D4AF37;
        --background-color: #050505;
        --secondary-background-color: #111111;
        --text-color: #FFFFFF;
        --font: sans-serif;
    }
    
    /* 2. 전체 배경 및 폰트 설정 (Deep Black) */
    .stApp {
        background-color: #050505 !important;
        color: #FFFFFF !important;
    }
    
    /* 3. 좌우 패널 스타일 (Aethir Guide의 카드 느낌) */
    div[data-testid="column"] {
        background-color: #111111;
        border: 1px solid #333333;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* 4. 입력창 스타일 (하얀색 배경 박멸) */
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; /* 아주 어두운 검정 */
        color: #FFFFFF !important; /* 흰색 글씨 */
        border: 1px solid #444444 !important;
        border-radius: 4px !important;
    }
    .stTextArea label, .stTextInput label {
        color: #D4AF37 !important; /* 라벨은 황금색 */
        font-weight: bold !important;
    }

    /* 5. [문제 해결] 버튼 스타일 - 에이셔 골드 & 가독성 끝판왕 */
    .stButton > button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; /* 에이셔 골드 */
        color: #000000 !important; /* ⚠️ 글자는 무조건 검은색 (가독성 핵심) */
        font-weight: 800 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        opacity: 1 !important; /* 투명도 제거 */
        text-shadow: none !important;
        margin-top: 10px;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        color: #000000 !important; /* 호버 시에도 검은색 유지 */
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    
    /* 삭제 버튼 (붉은색 계열) */
    .delete-btn > button {
        background: linear-gradient(90deg, #FF5F6D, #FFC371) !important;
        color: #FFFFFF !important; /* 삭제 버튼은 흰 글씨 */
    }

    /* 6. 텍스트 가독성 강제 (모든 설명글 흰색) */
    p, .stMarkdown, .stInfo, .stExpander {
        color: #E6E6E6 !important;
    }
    
    /* 7. Expander(접는 메뉴) 스타일 커스텀 */
    .streamlit-expanderHeader {
        background-color: #1A1A1A !important;
        color: #FFFFFF !important;
        border: 1px solid #333333 !important;
    }
    div[data-testid="stExpander"] > details > div {
        background-color: #0A0A0A !important;
        color: #FFFFFF !important;
    }

    /* 8. 타이틀 스타일 */
    h1 { color: #FFFFFF !important; border-bottom: 2px solid #D4AF37; padding-bottom: 10px; }
    h3 { color: #D4AF37 !important; }
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

# --- LAYOUT: 50:50 SPLIT ---
col_left, col_right = st.columns(2)

# ================= LEFT PANEL: 기록 (Journal) =================
with col_left:
    st.markdown("### 📓 무의식 원재료 (Journal)")
    st.markdown("꿈의 내용을 가감 없이 기록하세요. (30분의 정성)")
    
    # [불러오기 기능]
    with st.expander("📂 지난 꿈 불러오기 (Load)", expanded=False):
        try:
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(5).execute()
            if res.data:
                for d in res.data:
                    col_l, col_r = st.columns([0.2, 0.8])
                    with col_l:
                        if st.button("로드", key=f"L_{d['id']}"):
                            st.session_state.current_dream_id = d['id']
                            st.session_state.dream_context = d.get('context', "")
                            st.session_state.s1_val = d.get('symbol', "")
                            st.session_state.s2_val = d.get('block', "")
                            st.session_state.s4_val = d.get('ritual_self', "")
                            st.session_state.interpretation_ready = True if d.get('meaning') else False
                            st.rerun()
                    with col_r:
                        st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:15]}...")
        except: st.write("데이터 없음")
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        st.session_state.current_dream_id = None
        st.session_state.dream_context = ""
        st.session_state.s1_val = ""
        st.session_state.s2_val = ""
        st.session_state.s4_val = ""
        st.session_state.interpretation_ready = False
        st.rerun()

    # [기록 폼]
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

# ================= RIGHT PANEL: 분석 (Analysis) =================
with col_right:
    st.markdown("### 🏛️ Master's Lab (Analysis)")
    
    # Stage 1 & 2
    st.text_area("🚀 Stage 1: 이미지 연상", value=st.session_state.s1_val, height=100, key="s1_key", placeholder="강렬한 상징 입력")
    st.text_area("🔍 Stage 2: 내적 역학", value=st.session_state.s2_val, height=100, key="s2_key", placeholder="현실의 에너지 관계")
    
    # 트리거 버튼 (에이셔 스타일)
    if st.button("▼ 마스터 통합 해석 가동 (ENTER)"):
        # 여기서 session_state 값을 업데이트하려면 text_area의 key와 동기화가 필요하지만, 
        # 직관성을 위해 form 밖에서 처리
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        
        if s1_input and s2_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            st.session_state.interpretation_ready = True
        else: st.warning("상징과 역학을 입력하세요.")

    # Stage 3: 결과
    if st.session_state.interpretation_ready:
        st.markdown(f"""
        <div style='background-color:#0A0A0A; border:1px solid #333; border-left:4px solid #D4AF37; padding:15px; margin-top:15px; border-radius:5px;'>
            <strong style='color:#D4AF37;'>🏛️ Master's Dialogue</strong><br><br>
            "{st.session_state.s1_val[:10]}..." 상징은 당신의 현실 속 "{st.session_state.s2_val[:10]}..." 역동을 돌파하기 위한 무의식의 선물입니다.
        </div>
        """, unsafe_allow_html=True)

    # Stage 4 & Minting
    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: Asset Minting")
        s4 = st.text_input("🏃 현실 의례 (Ritual)", value=st.session_state.s4_val, placeholder="오늘 실행할 행동")
        
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.current_dream_id else "💎 최종 자산 발행 (Mint Token)"
        
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4 and st.session_state.interpretation_ready:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + st.session_state.s2_val + s4)*5)
                
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "ritual_self": s4,
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
                <div style='background-color:#111; border:1px solid #D4AF37; padding:15px; border-radius:5px; margin-top:10px; text-align:center;'>
                    <h3 style='margin:0; color:#FDB931;'>💎 Token Minted</h3>
                    <p style='margin:10px 0; font-size:1.2em; color:white;'>Value: <b>{token_val:,} D-Fi Tokens</b></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("분석 단계를 모두 완료해주세요.")
