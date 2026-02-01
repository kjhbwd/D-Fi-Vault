import streamlit as st
from supabase import create_client, Client
import time
import datetime

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v11.2", page_icon="🏛️", layout="wide")

# 🔒 1차 관문: 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "korea2026"

# --- CSS: 디자인 (Manifesto & Golden Dark) ---
st.markdown("""
    <style>
    /* 1. 전체 테마: Deep Black */
    .stApp { background-color: #050505 !important; color: #FFFFFF !important; }
    
    /* 2. 버튼 스타일 (황금색 강제) */
    button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        background-color: #D4AF37 !important;
        border: none !important;
        opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important;
        padding: 0.5rem 1rem !important;
        border-radius: 0.5rem !important;
    }
    button p, button div, button span {
        color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important;
    }
    button:hover { background: #FFD700 !important; transform: scale(1.02); }
    
    /* 3. 입력창 스타일 */
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    
    /* 4. 헤더/푸터 숨김 */
    header, footer { visibility: hidden !important; }
    h1, h2, h3, h4, p, label, .stMarkdown, .stMetricValue, .stMetricLabel { color: #FFFFFF !important; }
    
    /* 🏛️ [Manifesto 디자인] */
    .main-title {
        font-size: 2.5em; font-weight: 900; color: #D4AF37; text-align: center; margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
    }
    .quote-box {
        border-left: 3px solid #D4AF37; padding-left: 20px; margin: 20px 0; color: #E0E0E0; font-style: italic; font-size: 1.1em;
    }
    .author { font-size: 0.9em; color: #888; text-align: right; display: block; margin-top: 5px; }
    
    .step-container {
        background-color: #1A1A1A; padding: 20px; border-radius: 10px; border: 1px solid #333; margin: 20px 0;
    }
    .step-title { color: #D4AF37; font-weight: bold; font-size: 1.2em; margin-bottom: 10px; text-align: center; }
    .step-list { color: #CCCCCC; line-height: 1.8; }
    
    .defi-desc {
        text-align: center; color: #AAAAAA; font-size: 1.0em; margin-top: 30px; margin-bottom: 30px; border-top: 1px solid #333; padding-top: 20px;
    }
    .highlight { color: #FDB931; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE]
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'auth_step' not in st.session_state: st.session_state.auth_step = "check_id"
if 'temp_username' not in st.session_state: st.session_state.temp_username = ""

for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's4_val', 'existing_value']:
    if key not in st.session_state: st.session_state[key] = "" if key != 'current_dream_id' else None
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

# [CONNECTION]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB 연결 오류")

# ==========================================
# 🚪 1차 관문: Manifesto & Community Code
# ==========================================
if not st.session_state.access_granted:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. 메인 타이틀
        st.markdown("<div class='main-title'>D-Fi : The Alchemy of Unconscious</div>", unsafe_allow_html=True)
        
        # 2. 칼 융 인용구
        st.markdown("""
        <div class='quote-box'>
            "무의식에 다가가서 무의식의 상징 언어를 배운다면,<br>
            삶을 좀 더 풍요롭고 충만하게 살 수 있다."
            <span class='author'>- Carl Gustav Jung (심층 심리학자)</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. 로버트 존슨의 4단계 & D-Fi 개념
        st.markdown("""
        <div class='step-container'>
            <div class='step-title'>🏛️ Robert A. Johnson's Dream Work Protocol</div>
            <div class='step-list'>
                <b>1단계 : 연상 (Association)</b> - 꿈속 상징의 개인적 의미 발견<br>
                <b>2단계 : 역학 (Dynamics)</b> - 내면 에너지의 흐름 파악<br>
                <b>3단계 : 해석 (Interpretation)</b> - 무의식의 메시지 통합<br>
                <b>4단계 : 의례 (Ritual)</b> - 구체적 행동으로 현실화 (자산 발행)
            </div>
        </div>
        
        <div class='defi-desc'>
            <p><b>D-Fi (Dream Finance)란?</b></p>
            비트코인이 연산으로 가치를 만든다면,<br>
            D-Fi는 당신의 <span class='highlight'>'자각'과 '실천'</span>으로 가치를 만듭니다.<br><br>
            꿈을 현실의 행동(Ritual)으로 바꾸는 순간,<br>
            당신의 무의식 에너지는 영구적인 <b>'디지털 심리 자산(Token)'</b>으로 기록됩니다.
        </div>
        """, unsafe_allow_html=True)
        
        # 4. 입장 폼
        with st.form("gate_form"):
            input_code = st.text_input("Entry Code", type="password", placeholder="입장 코드를 입력하세요")
            if st.form_submit_button("🗝️ 무의식 광산 입장하기"):
                if input_code == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.toast("✅ 접속 승인. 환영합니다.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("⛔ 유효하지 않은 코드입니다.")
    st.stop()

# ==========================================
# 🚪 2차 관문: Identity Check (로그인/가입)
# ==========================================
if not st.session_state.user_id:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>👤 Identity Check</h2>", unsafe_allow_html=True)

        if st.session_state.auth_step == "check_id":
            with st.form("id_check_form"):
                st.markdown("<p style='text-align:center; color:#AAA;'>본인의 고유 닉네임(ID)을 입력하여 금고를 여세요.</p>", unsafe_allow_html=True)
                input_id = st.text_input("Nickname", placeholder="예: dreamer01")
                if st.form_submit_button("🚀 다음 (Next)"):
                    if input_id:
                        res = supabase.table("users").select("*").eq("username", input_id).execute()
                        st.session_state.temp_username = input_id
                        if res.data: st.session_state.auth_step = "login"
                        else: st.session_state.auth_step = "register"
                        st.rerun()
                    else: st.warning("닉네임을 입력해주세요.")

        elif st.session_state.auth_step == "login":
            st.info(f"👋 환영합니다, **{st.session_state.temp_username}**님! (기존 회원)")
            with st.form("login_pin_form"):
                input_pin = st.text_input("비밀번호 (PIN 4자리)", type="password", max_chars=4)
                c_a, c_b = st.columns(2)
                with c_a: login_btn = st.form_submit_button("🔓 금고 열기")
                with c_b: hint_btn = st.form_submit_button("❓ 힌트 보기")

                if login_btn:
                    res = supabase.table("users").select("*").eq("username", st.session_state.temp_username).eq("pin", input_pin).execute()
                    if res.data:
                        st.session_state.user_id = st.session_state.temp_username
                        st.toast("로그인 성공!")
                        st.rerun()
                    else: st.error("비밀번호가 일치하지 않습니다.")
                
                if hint_btn:
                    res = supabase.table("users").select("hint").eq("username", st.session_state.temp_username).execute()
                    if res.data and res.data[0]['hint']: st.warning(f"💡 힌트: {res.data[0]['hint']}")
                    else: st.warning("등록된 힌트가 없습니다.")
            
            if st.button("⬅️ 뒤로 가기"):
                st.session_state.auth_step = "check_id"
                st.rerun()

        elif st.session_state.auth_step == "register":
            st.success(f"✨ **{st.session_state.temp_username}**님은 처음 오셨군요! 전용 금고를 생성합니다.")
            with st.form("register_form"):
                new_pin = st.text_input("설정할 비밀번호 (4자리)", type="password", max_chars=4)
                hint = st.text_input("비밀번호 힌트 (선택사항)", placeholder="예: 내 생일, 반려견 이름")
                if st.form_submit_button("📝 가입 및 입장"):
                    if len(new_pin) >= 1:
                        supabase.table("users").insert({"username": st.session_state.temp_username, "pin": new_pin, "hint": hint if hint else "없음"}).execute()
                        st.session_state.user_id = st.session_state.temp_username
                        st.balloons()
                        st.rerun()
                    else: st.warning("비밀번호를 입력해주세요.")
            if st.button("⬅️ 뒤로 가기"):
                st.session_state.auth_step = "check_id"
                st.rerun()
    st.stop()

# ==========================================
# 🏛️ MAIN APP: 작업 공간 (Workspace)
# ==========================================
def get_daily_tokens(user):
    try:
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        res = supabase.table("dreams").select("*").eq("user_id", user).order("created_at", desc=True).limit(50).execute()
        total_score = 0
        count = 0
        if res.data:
            for d in res.data:
                if d['created_at'].startswith(today_str):
                    meaning = d.get('meaning', "")
                    if meaning and "Value:" in meaning:
                        try:
                            score_part = meaning.split("Value: ")[1].split(" Tokens")[0]
                            score = int(score_part.replace(",", ""))
                            total_score += score
                            count += 1
                        except: pass
        return total_score, count
    except: return 0, 0

daily_sum, daily_count = get_daily_tokens(st.session_state.user_id)

col_dash1, col_dash2, col_dash3 = st.columns([0.6, 0.2, 0.2])
with col_dash1: st.markdown(f"### 🏛️ Vault of {st.session_state.user_id}")
with col_dash2: st.metric(label="Today's Mining", value=f"{daily_sum:,} T", delta=f"{daily_count}건")
with col_dash3:
    if st.button("🔒 로그아웃"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### 📓 무의식 원재료")
    with st.expander("📂 내 지난 꿈 불러오기", expanded=False):
        try:
            res = supabase.table("dreams").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).limit(5).execute()
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
                            meaning_text = d.get('meaning', "")
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
                            st.session_state.interpretation_ready = True if meaning_text else False
                            st.session_state.is_minted = True if meaning_text else False
                            st.rerun()
                    with c_r: st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
            else: st.info("기록 없음")
        except: pass
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        st.session_state.interpretation_ready = False
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = "📝 수정 모드" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
        st.caption(status)
        dream_raw = st.text_area("꿈 내용 입력", value=st.session_state.dream_context, height=450)
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button("💾 내 금고에 저장"):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                    st.toast("수정 완료")
                else:
                    data = supabase.table("dreams").insert({"context": dream_raw, "user_id": st.session_state.user_id}).execute()
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                        st.session_state.is_minted = False 
                        st.rerun()
        with c2:
            if st.session_state.current_dream_id:
                if st.form_submit_button("🗑️ 삭제 (Delete)"):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.session_state.is_minted = False
                    st.rerun()

with col_right:
    st.markdown("### 🏛️ Master's Lab")
    st.text_area("🚀 Stage 1: 연상 (Association)", value=st.session_state.s1_val, height=100, key="s1_key", placeholder="꿈속 이미지의 개인적 의미를 발견하세요")
    st.text_area("🔍 Stage 2: 역학 (Dynamics)", value=st.session_state.s2_val, height=100, key="s2_key", placeholder="내면 에너지의 흐름을 파악하세요")
    if st.button("▼ 마스터 해석 가동 (ENTER)"):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        if s1_input and s2_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            st.session_state.interpretation_ready = True
        else: st.warning("내용을 입력해주세요.")

    if st.session_state.interpretation_ready:
        st.markdown(f"""
        <div style='background-color:#0A0A0A; border:1px solid #333; border-left:4px solid #D4AF37; padding:15px; margin-top:15px;'>
            <strong style='color:#D4AF37;'>🏛️ 3단계: 해석 (Interpretation)</strong><br>
            "{st.session_state.s1_val[:10]}..." 상징은 당신의 무의식이 보내는 통합의 메시지입니다.
        </div>
        """, unsafe_allow_html=True)

    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: 의례 (Ritual)")
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 지난 자산 가치: {st.session_state.existing_value}")
        s4 = st.text_input("구체적 실천 행동을 입력하세요", value=st.session_state.s4_val)
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*5)
                new_val_str = f"Value: {token_val} Tokens"
                payload = {"symbol": st.session_state.s1_val, "block": st.session_state.s2_val, "ritual_self": s4, "meaning": new_val_str}
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update(payload).eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                else:
                    payload["context"] = st.session_state.dream_context
                    payload["user_id"] = st.session_state.user_id
                    data = supabase.table("dreams").insert(payload).execute()
                    if data.data: st.session_state.current_dream_id = data.data[0]['id']
                st.session_state.is_minted = True
                st.session_state.existing_value = new_val_str 
                st.balloons()
                st.success(f"✅ 의례(Ritual) 등록 완료!\n\n💰 {new_val_str}")
                time.sleep(3)
                st.rerun()
