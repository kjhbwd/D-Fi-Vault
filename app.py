import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v15.0", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# 🔒 1. 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "2026"

# 🛡️ 2. 관리자 보안 설정 (빌더님 ID)
ADMIN_USER = "김지호bwd"
MASTER_KEY = "1234"

# 🪙 [TOKENOMICS]
MAX_SUPPLY = 21000000
HALVING_STEP = 2100000

# 🟢 [CORE] 언어 설정 초기화
if 'language' not in st.session_state: st.session_state.language = "KO"

# ==========================================
# 🌐 [LANGUAGE PACK] - 로버트 존슨 실례 가이드 통합
# ==========================================
LANG = {
    "KO": {
        "title": "D-Fi : 무의식의 연금술",
        "manifesto_quote": '"현실의 결핍은 무의식의 풍요로 채워진다.<br>이것은 평범한 개인이 자신의 운명을 바꾸는 <b>퀀텀 점프 실험실</b>입니다."',
        "tokenomics": "🪙 Tokenomics : 비트코인 모델 적용",
        "token_desc": "• 총 발행 한도: 21,000,000 Dream Pts<br>• 반감기(Halving): 매 2,100,000 Pts 채굴 시 보상 50% 감소",
        "desc_1_title": "1. 성장의 시각화 (Visualizing Growth)",
        "desc_1_text": "저는 생존을 고민하는 평범한 사람입니다. 하지만 매일 밤 <b>꿈(무의식)</b>을 채굴하여 제 잠재력을 깨우고 있습니다. 여기에 쌓이는 <b>Dream Pts</b>는 제가 얼마나 깊이 각성했는지를 보여주는 <b>성장의 증명</b>입니다.",
        "desc_2_title": "2. 현실의 변화 (X-Factor)",
        "desc_2_text": "이곳에서 제련된 통찰은 <b>X(트위터)</b>와 현실의 콘텐츠가 됩니다. 무의식의 영감이 어떻게 <b>노출수(Traffic)</b>와 <b>수익(Revenue)</b>으로 변환되는지 목격하십시오.",
        "login_placeholder": "입장 코드를 입력하세요 (2026)",
        "login_btn": "🗝️ 무의식 광산 입장하기",
        "login_error": "⛔ 코드가 틀렸습니다. (2026)",
        "id_check_title": "👤 Identity Check",
        "id_check_desc": "본인의 고유 닉네임(ID)을 입력하여 금고를 여세요.",
        "next_btn": "🚀 다음 (Next)",
        "welcome": "👋 환영합니다",
        "open_vault": "🔓 금고 열기",
        "hint_btn": "❓ 힌트 보기",
        "register_msg": "✨ 처음 오셨군요! 전용 금고를 생성합니다.",
        "register_btn": "📝 가입 및 입장",
        "pin_placeholder": "비밀번호 (PIN 4자리)",
        "hint_placeholder": "비밀번호 힌트 (선택사항)",
        "dash_global": "Global Mined",
        "dash_difficulty": "Mining Difficulty",
        "dash_my_asset": "My Active Assets",
        "logout": "🔒 로그아웃",
        "left_title": "📓 무의식 원재료 (Raw Dream)",
        "load_dreams": "📂 내 지난 꿈 불러오기",
        "load_btn": "로드",
        "reset_btn": "🔄 새로 쓰기 (Reset)",
        "status_edit": "📝 수정 모드",
        "status_new": "✨ 신규 작성 모드",
        "save_btn": "💾 임시 저장 (Save Draft)",
        "delete_btn": "🗑️ 삭제 (Delete)",
        "right_title": "🏛️ D-Fi 연금술 (4-Step Process)",
        
        # --- [NEW] 4단계 실례 가이드 (KO) ---
        "s1_label": "🚀 Stage 1: 연상 (Association)",
        "s1_help": """[가이드: 개인적 의미의 방사형 연결]
이미지(A)를 중심에 두고 떠오르는 직관을 포착하세요.
(실례)
- 초등학교 교실: 배움, 미성숙함, 규율, 답답함.
- 검은 옷의 남자: 권위적임, 무서움, 그림자(Shadow).
- 오래된 시계: 시간의 압박, 멈춰 있음, 수명이 다함.""",
        
        "s2_label": "🔍 Stage 2: 역학 (Dynamics)",
        "s2_help": """[가이드: 내면의 인격들과 연결하기]
"내 안의 어떤 부분이 이 이미지와 닮았는가?"를 자문하세요.
(실례)
- 초등학교 교실 → 나의 학습 태도: 과거의 방식에 갇혀 있음.
- 검은 옷의 남자 → 내면의 감독관: 나를 압박하는 초자아.
- 고장 난 시계 → 나의 생체 리듬: 에너지가 고갈되어 멈춤.""",
        
        "s3_label": "🏛️ Stage 3: 해석 (Interpretation)",
        "s3_help": """[가이드: 메시지의 통합]
꿈이 보내는 보상적(Compensatory) 메시지를 읽어냅니다.
(실례)
- 분석: 과거의 낡은 방식으로 문제를 해결하려 함. 내면의 권위자는 '내면의 질서' 회복을 명령함.
- 결론: 멈춰버린 리듬을 수리하고 전문가적 태도를 갖춰야 한다는 신호.""",
        
        "s4_label": "💎 Stage 4: 의례 (Ritual)",
        "s4_help": """[가이드: 구체적 행동으로의 육화]
깨달음을 물리적 행동으로 옮기세요. 상징적 의미가 명확해야 합니다.
(좋은 예)
- 실제로 멈춘 시계의 배터리를 교체함.
- 시간 계획표를 짜서 지갑에 넣음.
- 전문 서적을 한 권 사서 읽음.""",
        
        "mint_btn": "💎 최종 자산 발행 (Mint Token)",
        "update_btn": "🏛️ 자산 정보 업데이트",
        "success_msg": "🎉 채굴 성공! (Minted)",
        "mined_value": "채굴된 가치",
        "bonus_msg": "현재 반감기 보너스",
        "ledger_title": "📊 D-Fi 투명 장부 (Ledger)",
        "ledger_desc": "모든 유저의 활성 자산 현황입니다. (소각된 자산 제외)",
        "burn_title": "🔥 자산 소각 (Buy-back)",
        "burn_desc": "보유한 자산을 현금화(바이백)하고 소각합니다.",
        "burn_btn": "💸 정산 및 소각 신청",
        "burn_success": "✅ 정산 완료! 모든 포인트가 소각되었습니다.",
        "admin_unlock": "🔒 Admin Unlock",
        "master_key_ph": "Enter Master Key",
        "reg_dreamers": "Registered Dreamers"
    },
    "EN": {
        "title": "D-Fi : Alchemy of the Unconscious",
        "manifesto_quote": '"The lack in reality is filled by the abundance of the unconscious.<br>This is a <b>Quantum Jump Laboratory</b> where an individual changes their destiny."',
        "tokenomics": "🪙 Tokenomics : Bitcoin Model",
        "token_desc": "• Max Supply: 21,000,000 Dream Pts<br>• Halving: Reward -50% every 2,100,000 Pts mined",
        "desc_1_title": "1. Visualizing Growth",
        "desc_1_text": "I mine my <b>Dreams (Unconscious)</b> to awaken my potential. The accumulated <b>Dream Pts</b> are the <b>Proof of Growth</b>.",
        "desc_2_title": "2. X-Factor (Reality Change)",
        "desc_2_text": "Insights refined here become content for <b>X (Twitter)</b>. Inspiration transforms into <b>Traffic</b> and <b>Revenue</b>.",
        "login_placeholder": "Enter Access Code (2026)",
        "login_btn": "🗝️ Enter the Mine",
        "login_error": "⛔ Invalid Code (2026)",
        "id_check_title": "👤 Identity Check",
        "id_check_desc": "Enter your unique Nickname (ID) to open the vault.",
        "next_btn": "🚀 Next",
        "welcome": "👋 Welcome",
        "open_vault": "🔓 Open Vault",
        "hint_btn": "❓ Hint",
        "register_msg": "✨ First time here! Creating your vault.",
        "register_btn": "📝 Register & Enter",
        "pin_placeholder": "Password (4-digit PIN)",
        "hint_placeholder": "Password Hint (Optional)",
        "dash_global": "Global Mined",
        "dash_difficulty": "Mining Difficulty",
        "dash_my_asset": "My Active Assets",
        "logout": "🔒 Logout",
        "left_title": "📓 Raw Material",
        "load_dreams": "📂 Load Past Dreams",
        "load_btn": "Load",
        "reset_btn": "🔄 Reset",
        "status_edit": "📝 Edit Mode",
        "status_new": "✨ New Entry Mode",
        "save_btn": "💾 Save Draft",
        "delete_btn": "🗑️ Delete",
        "right_title": "🏛️ D-Fi Alchemy",
        
        # --- [NEW] 4-Step Guide (EN) ---
        "s1_label": "🚀 Stage 1: Association",
        "s1_help": """[Guide: Radial Association]
Focus on the image(A) and capture intuitive feelings.
(Example)
- School: Learning, Immaturity, Discipline.
- Man in Black: Authority, Fear, Shadow.
- Old Clock: Pressure of time, Stopped.""",
        
        "s2_label": "🔍 Stage 2: Dynamics",
        "s2_help": """[Guide: Inner Personas]
"Which part of me resembles this image?"
(Example)
- School → My learning attitude: Stuck in old ways.
- Man in Black → Inner supervisor: Superego.
- Broken Clock → My bio-rhythm: Energy depleted.""",
        
        "s3_label": "🏛️ Stage 3: Interpretation",
        "s3_help": """[Guide: Message Integration]
Read the compensatory message.
(Example)
- Analysis: Trying to solve problems with old ways.
- Conclusion: Signal to repair the stopped rhythm and adopt a professional attitude.""",
        
        "s4_label": "💎 Stage 4: Ritual",
        "s4_help": """[Guide: Physical Incarnation]
Move insight into physical action.
(Example)
- Replacing the battery of a stopped clock.
- Writing a schedule and putting it in your wallet.""",
        
        "mint_btn": "💎 Mint Token",
        "update_btn": "🏛️ Update Asset",
        "success_msg": "🎉 Minting Successful!",
        "mined_value": "Mined Value",
        "bonus_msg": "Current Halving Bonus",
        "ledger_title": "📊 D-Fi Public Ledger",
        "ledger_desc": "Active assets of all users.",
        "burn_title": "🔥 Asset Burn (Buy-back)",
        "burn_desc": "Cash out (Buy-back) and burn your assets.",
        "burn_btn": "💸 Cash Out & Burn",
        "burn_success": "✅ Burn Complete! Points reset to 0.",
        "admin_unlock": "🔒 Admin Unlock",
        "master_key_ph": "Enter Master Key",
        "reg_dreamers": "Registered Dreamers"
    }
}

# --- CSS: 디자인 (올블랙 & 가독성 & 폰트) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
    
    .stApp, .stApp > header, .stApp > footer, .stApp > main { background-color: #050505 !important; color: #FFFFFF !important; }
    header { background-color: #050505 !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333 !important; }
    [data-testid="stToolbar"] { visibility: hidden !important; display: none !important; }
    footer { visibility: hidden !important; display: none !important; }
    
    .streamlit-expanderHeader p { color: #FFFFFF !important; font-weight: bold !important; font-size: 1.1em !important; }
    .streamlit-expanderHeader:hover p { color: #D4AF37 !important; } 
    
    button { background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; background-color: #D4AF37 !important; border: none !important; opacity: 1 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important; padding: 0.5rem 1rem !important; border-radius: 0.5rem !important; }
    button p, button div, button span { color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important; }
    button:hover { background: #FFD700 !important; transform: scale(1.02); }
    
    .stTextArea textarea, .stTextInput input { background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important; }
    label, .stMarkdown label, p, .stMetricLabel { color: #E0E0E0 !important; }
    .stMetricValue { color: #D4AF37 !important; }
    div[data-testid="column"] { background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px; }
    
    /* 툴팁 스타일 */
    div[data-baseweb="popover"], div[data-baseweb="tooltip"] { background-color: #1A1A1A !important; border: 1px solid #D4AF37 !important; border-radius: 8px !important; max-width: 400px !important; }
    div[data-baseweb="popover"] > div, div[data-baseweb="tooltip"] > div { color: #FFFFFF !important; background-color: #1A1A1A !important; }
    
    /* Registered Dreamers 스타일 (Cinzel + Gold) */
    .dreamer-count-header { font-family: 'Cinzel', serif; color: #D4AF37; font-size: 1.2em; font-weight: bold; text-align: right; }
    
    .main-title { font-size: 2.5em; font-weight: 900; color: #D4AF37 !important; text-align: center; margin-bottom: 20px; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); font-family: 'Malgun Gothic', sans-serif; }
    .quote-box { background-color: #1A1A1A !important; border-left: 4px solid #D4AF37 !important; padding: 20px !important; margin: 20px 0 !important; color: #E0E0E0 !important; font-style: italic; font-size: 1.2em; border-radius: 5px; }
    .defi-desc-box { background-color: #111111 !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #333 !important; margin-top: 30px; margin-bottom: 30px; }
    .defi-desc-text { color: #BBBBBB !important; font-size: 1.0em; line-height: 1.8; font-family: sans-serif; }
    .highlight-gold { color: #FDB931 !important; font-weight: bold; font-size: 1.2em; margin-bottom: 15px; display: block; }
    .highlight-bold { color: #FFFFFF !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE]
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'auth_step' not in st.session_state: st.session_state.auth_step = "check_id"
if 'temp_username' not in st.session_state: st.session_state.temp_username = ""
if 'is_admin_unlocked' not in st.session_state: st.session_state.is_admin_unlocked = False

for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
    if key not in st.session_state: st.session_state[key] = "" if key != 'current_dream_id' else None
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB Connection Error")

# ==========================================
# 🟢 [CORE FUNCTION] 실시간 유저 수 조회
# ==========================================
def get_user_count():
    try:
        count_res = supabase.table("users").select("username", count="exact").execute()
        return count_res.count if count_res.count else 0
    except: return 0

# ==========================================
# 🚪 1차 관문: Manifesto (입장 전)
# ==========================================
if not st.session_state.access_granted:
    col_lang1, col_lang2, col_lang3 = st.columns([8, 2, 1])
    with col_lang2:
        lang_choice = st.radio("Language", ["KO", "EN"], horizontal=True, label_visibility="collapsed")
        st.session_state.language = lang_choice
    T = LANG[st.session_state.language]
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='main-title'>{T['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote-box'>{T['manifesto_quote']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='defi-desc-box'>
    <div class='defi-desc-text'>
        <span class='highlight-gold'>{T['tokenomics']}</span>
        <p>{T['token_desc']}</p>
        <p><span class='highlight-bold'>{T['desc_1_title']}</span><br>
        {T['desc_1_text']}</p>
        <p><span class='highlight-bold'>{T['desc_2_title']}</span><br>
        {T['desc_2_text']}</p>
    </div>
</div>""", unsafe_allow_html=True)
        
        with st.form("gate_form"):
            input_code = st.text_input("Entry Code", type="password", placeholder=T['login_placeholder'])
            if st.form_submit_button(T['login_btn']):
                if input_code.strip() == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.toast("✅ Access Granted.")
                    time.sleep(0.5)
                    st.rerun()
                else: st.error(T['login_error'])
        
        user_count = get_user_count()
        st.markdown(f"<div style='text-align:center; font-family:Cinzel; color:#D4AF37; margin-top:20px;'>✨ {T['reg_dreamers']} : {user_count:,}</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# 🏛️ 2차/3차 관문 및 메인 로직
# ==========================================
T = LANG[st.session_state.language]

if not st.session_state.user_id:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align: center;'>{T['id_check_title']}</h2>", unsafe_allow_html=True)
        if st.session_state.auth_step == "check_id":
            with st.form("id_check_form"):
                st.markdown(f"<p style='text-align:center; color:#AAA;'>{T['id_check_desc']}</p>", unsafe_allow_html=True)
                input_id = st.text_input("Nickname", placeholder="Ex: dreamer01")
                if st.form_submit_button(T['next_btn']):
                    if input_id:
                        clean_id = input_id.strip()
                        res = supabase.table("users").select("*").eq("username", clean_id).execute()
                        st.session_state.temp_username = clean_id
                        if res.data: st.session_state.auth_step = "login"
                        else: st.session_state.auth_step = "register"
                        st.rerun()
        elif st.session_state.auth_step == "login":
            st.info(f"{T['welcome']}, **{st.session_state.temp_username}**!")
            with st.form("login_pin_form"):
                input_pin = st.text_input("PIN", type="password", max_chars=4, placeholder=T['pin_placeholder'])
                c_a, c_b = st.columns(2)
                with c_a: login_btn = st.form_submit_button(T['open_vault'])
                with c_b: hint_btn = st.form_submit_button(T['hint_btn'])
                if login_btn:
                    res = supabase.table("users").select("*").eq("username", st.session_state.temp_username).eq("pin", input_pin).execute()
                    if res.data:
                        st.session_state.user_id = st.session_state.temp_username
                        st.rerun()
                    else: st.error("Wrong PIN")
                if hint_btn:
                    res = supabase.table("users").select("hint").eq("username", st.session_state.temp_username).execute()
                    if res.data and res.data[0]['hint']: st.warning(f"💡 {res.data[0]['hint']}")
            if st.button("⬅️ Back"):
                st.session_state.auth_step = "check_id"
                st.rerun()
        elif st.session_state.auth_step == "register":
            st.success(T['register_msg'])
            with st.form("register_form"):
                new_pin = st.text_input("PIN", type="password", max_chars=4, placeholder=T['pin_placeholder'])
                hint = st.text_input("Hint", placeholder=T['hint_placeholder'])
                if st.form_submit_button(T['register_btn']):
                    if len(new_pin) >= 1:
                        supabase.table("users").insert({"username": st.session_state.temp_username, "pin": new_pin, "hint": hint if hint else "None"}).execute()
                        st.session_state.user_id = st.session_state.temp_username
                        st.rerun()
            if st.button("⬅️ Back"):
                st.session_state.auth_step = "check_id"
                st.rerun()
    st.stop()

# ==========================================
# 💎 DASHBOARD (로그인 성공 후)
# ==========================================
user_count = get_user_count()

# 3. 보상 계산 로직 (유저 자율 입력 기반)
def calculate_dream_quality_score(context, s1, s2, s3, s4, current_halving_multiplier):
    base_score = 1000 
    # 글자 수 기반 정성 평가
    score_context = len(context) * 2 if context else 0
    score_s1 = len(s1) * 5 if s1 else 0
    score_s2 = len(s2) * 5 if s2 else 0
    score_s3 = len(s3) * 5 if s3 else 0 
    score_s4 = len(s4) * 10 if s4 else 0 
    raw_score = base_score + score_context + score_s1 + score_s2 + score_s3 + score_s4
    final_score = int(raw_score * current_halving_multiplier)
    return min(10000, final_score)

def get_ledger_data():
    try:
        res_all = supabase.table("dreams").select("user_id, meaning, is_burned").execute()
        ledger = {} 
        if res_all.data:
            for d in res_all.data:
                if d.get('is_burned') is True: continue
                uid = d['user_id']
                meaning = d.get('meaning', "")
                score = 0
                if meaning and "Value:" in meaning:
                    try:
                        score_text = meaning.split("Value: ")[1]
                        if "Dream Pts" in score_text: part = score_text.split(" Dream Pts")[0]
                        else: part = "0"
                        score = int(part.replace(",", ""))
                    except: pass
                if uid not in ledger: ledger[uid] = [0, 0]
                ledger[uid][0] += score
                ledger[uid][1] += 1
        ledger_list = []
        for uid, data in ledger.items():
            ledger_list.append({"User ID": uid, "Active Assets (Pts)": data[0], "Blocks": data[1]})
        df = pd.DataFrame(ledger_list)
        if not df.empty:
            df = df.sort_values(by="Active Assets (Pts)", ascending=False).reset_index(drop=True)
            df.index = df.index + 1
            df.index.name = "Rank"
        return df
    except: return pd.DataFrame()

def get_global_status(current_user):
    try:
        res_all = supabase.table("dreams").select("meaning, user_id, is_burned").execute()
        my_total = 0
        my_count = 0
        global_mined = 0
        if res_all.data:
            for d in res_all.data:
                score = 0
                meaning = d.get('meaning', "")
                if meaning and "Value:" in meaning:
                    try:
                        score_text = meaning.split("Value: ")[1]
                        if "Dream Pts" in score_text: part = score_text.split(" Dream Pts")[0]
                        else: part = "0"
                        score = int(part.replace(",", ""))
                    except: pass
                
                global_mined += score 
                if d['user_id'] == current_user and d.get('is_burned') is not True:
                    my_total += score
                    my_count += 1
        
        halving_era = global_mined // HALVING_STEP
        current_multiplier = 1 / (2 ** halving_era)
        return my_total, my_count, global_mined, current_multiplier, halving_era
    except: return 0, 0, 0, 1, 0

my_assets, my_mining_count, global_supply, mining_multiplier, current_era = get_global_status(st.session_state.user_id)
supply_progress = min(1.0, global_supply / MAX_SUPPLY)

# 상단 헤더
c_header_1, c_header_2 = st.columns([7, 3])
with c_header_1:
    st.markdown(f"### 🪙 {T['dash_global']} (Era: {current_era + 1})")
with c_header_2:
    sub_c1, sub_c2 = st.columns(2)
    with sub_c1:
        lang_dash = st.radio("Language", ["KO", "EN"], label_visibility="collapsed", horizontal=True, key="dash_lang")
        if lang_dash != st.session_state.language:
            st.session_state.language = lang_dash
            st.rerun()
    with sub_c2:
        st.markdown(f"<div class='dreamer-count-header'>✨ Dreamers: {user_count:,}</div>", unsafe_allow_html=True)

st.progress(supply_progress)
c_d1, c_d2, c_d3, c_d4 = st.columns(4)
with c_d1: st.metric(T['dash_global'], f"{global_supply:,} / {MAX_SUPPLY:,}", delta=f"{supply_progress*100:.2f}%")
with c_d2: st.metric(T['dash_difficulty'], f"Reward x{mining_multiplier}", delta="Halving Active" if current_era > 0 else "Genesis Era", delta_color="inverse")
with c_d3: st.metric(T['dash_my_asset'], f"{my_assets:,} Dream Pts", delta=f"{my_mining_count} blocks")
with c_d4: 
    if st.button(T['logout']):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

# 👑 [ADMIN PANEL]
if st.session_state.user_id == ADMIN_USER:
    st.markdown("---")
    st.markdown(f"#### 👑 Administrator Panel (ID: {st.session_state.user_id})")

    if not st.session_state.is_admin_unlocked:
        with st.form("admin_unlock_form"):
            st.caption("Enter Master Key to access Ledger & Burn functions")
            master_input = st.text_input(T['master_key_ph'], type="password")
            if st.form_submit_button("Unlock Admin Mode"):
                if master_input == MASTER_KEY:
                    st.session_state.is_admin_unlocked = True
                    st.toast("🔓 Admin Mode Unlocked!")
                    st.rerun()
                else: st.error("Access Denied")
    else:
        ad_c1, ad_c2 = st.columns(2)
        with ad_c1:
            st.info(f"📊 {T['ledger_title']}")
            if st.button("🔄 Refresh Ledger"): st.rerun()
            df_ledger = get_ledger_data()
            if not df_ledger.empty: st.dataframe(df_ledger, use_container_width=True)
            else: st.write("No active data.")
            
        with ad_c2:
            st.error(f"🔥 {T['burn_title']}")
            st.warning(T['burn_desc'])
            if st.button(T['burn_btn']):
                supabase.table("dreams").update({"is_burned": True}).eq("user_id", st.session_state.user_id).execute()
                st.toast(T['burn_success'])
                time.sleep(2)
                st.rerun()
        
        st.markdown("---")
        st.write("### 🚑 긴급 복구 (Emergency Restore)")
        if st.button("↩️ 소각 취소 및 자산 복구 (Unburn)"):
            supabase.table("dreams").update({"is_burned": False}).eq("user_id", st.session_state.user_id).execute()
            st.success("✅ 자산이 성공적으로 복구되었습니다! (Recovered)")
            time.sleep(2)
            st.rerun()
                
        if st.button("🔒 Lock Admin"):
            st.session_state.is_admin_unlocked = False
            st.rerun()

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### {T['left_title']}")
    with st.expander(T['load_dreams'], expanded=False):
        try:
            res = supabase.table("dreams").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).limit(5).execute()
            if res.data:
                for d in res.data:
                    c_l, c_r = st.columns([0.3, 0.7])
                    with c_l:
                        if st.button(T['load_btn'], key=f"L_{d['id']}"):
                            st.session_state.current_dream_id = d['id']
                            st.session_state.dream_context = d.get('context', "")
                            st.session_state.s1_val = d.get('symbol', "")
                            st.session_state.s2_val = d.get('block', "")
                            st.session_state.s3_val = d.get('analysis', "")
                            st.session_state.s4_val = d.get('ritual_self', "")
                            meaning_text = d.get('meaning', "")
                            st.session_state.existing_value = meaning_text if meaning_text else "N/A"
                            st.session_state.is_minted = True if meaning_text else False
                            st.rerun()
                    with c_r: st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
            else: st.info("No records")
        except: pass
    
    if st.button(T['reset_btn']):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = T['status_edit'] if st.session_state.current_dream_id else T['status_new']
        st.caption(status)
        dream_raw = st.text_area("Dream Content", value=st.session_state.dream_context, height=450)
        c1, c2 = st.columns(2)
        with c1:
            if st.form_submit_button(T['save_btn']):
                if st.session_state.current_dream_id:
                    supabase.table("dreams").update({"context": dream_raw}).eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                else:
                    data = supabase.table("dreams").insert({"context": dream_raw, "user_id": st.session_state.user_id}).execute()
                    if data.data:
                        st.session_state.current_dream_id = data.data[0]['id']
                        st.session_state.dream_context = dream_raw
                st.toast("Saved!")
                time.sleep(0.5)
                st.rerun()
        with c2:
            if st.session_state.current_dream_id:
                if st.form_submit_button(T['delete_btn']):
                    supabase.table("dreams").delete().eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                    st.session_state.current_dream_id = None
                    st.session_state.dream_context = ""
                    st.rerun()

with col_right:
    st.markdown(f"### {T['right_title']}")
    
    with st.form("mint_form"):
        # 1단계
        st.text_area(T['s1_label'], help=T['s1_help'], key="s1_val", height=100)
        # 2단계
        st.text_area(T['s2_label'], help=T['s2_help'], key="s2_val", height=100)
        # 3단계
        st.text_area(T['s3_label'], help=T['s3_help'], key="s3_val", height=150)
        # 4단계
        st.markdown(f"#### {T['s4_label']}", help=T['s4_help'])
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 Prev Value: {st.session_state.existing_value}")
        st.text_input("Action", key="s4_val")
        
        final_btn = T['update_btn'] if st.session_state.is_minted else T['mint_btn']
        
        if st.form_submit_button(final_btn):
            # 모든 필드가 채워져야 채굴 가능
            if st.session_state.s1_val and st.session_state.s2_val and st.session_state.s3_val and st.session_state.s4_val and st.session_state.dream_context:
                
                token_val = calculate_dream_quality_score(
                    st.session_state.dream_context, 
                    st.session_state.s1_val, 
                    st.session_state.s2_val, 
                    st.session_state.s3_val, 
                    st.session_state.s4_val, 
                    mining_multiplier
                )
                
                new_val_str = f"Value: {token_val:,} Dream Pts"
                
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "analysis": st.session_state.s3_val,
                    "ritual_self": st.session_state.s4_val, 
                    "meaning": new_val_str
                }
                
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
                msg = st.empty()
                msg.markdown(f"""
                <div style="background-color:#D4AF37; padding:20px; border-radius:10px; text-align:center; border:2px solid #FFFFFF;">
                    <h2 style='color:black; margin:0;'>{T['success_msg']}</h2>
                    <h3 style='color:black; margin:10px 0;'>💎 +{token_val:,} Dream Pts</h3>
                    <p style='color:black;'>{T['bonus_msg']}: x{mining_multiplier}</p>
                </div>
                """, unsafe_allow_html=True)
                time.sleep(3) 
                st.rerun()
            else:
                st.error("⚠️ 채굴 실패: 모든 단계(1~4단계)를 정성껏 작성해야 '성장의 증명'이 완료됩니다.")
