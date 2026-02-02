import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v13.15", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# 🔒 1. 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "2026"

# 🛡️ 2. 관리자 보안 설정
ADMIN_USER = "김지호bwd"  
MASTER_KEY = "1234" 

# 🪙 [TOKENOMICS]
MAX_SUPPLY = 21000000
HALVING_STEP = 2100000

# 🟢 [CORE] 언어 설정 초기화
if 'language' not in st.session_state: st.session_state.language = "KO"

# ==========================================
# 🌐 [LANGUAGE PACK]
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
        "left_title": "📓 무의식 원재료",
        "load_dreams": "📂 내 지난 꿈 불러오기",
        "load_btn": "로드",
        "reset_btn": "🔄 새로 쓰기 (Reset)",
        "status_edit": "📝 수정 모드",
        "status_new": "✨ 신규 작성 모드",
        "save_btn": "💾 내 금고에 저장",
        "delete_btn": "🗑️ 삭제 (Delete)",
        "right_title": "🏛️ D-Fi 연금술",
        "s1_label": "🚀 Stage 1: 연상 (Association)",
        "s1_help": """[수행 방법]
1. 꿈을 '이미지' 단위로 쪼갭니다.
2. 각 이미지마다 "이것을 보면 무엇이 떠오르는가?", "이 사람은 내 인생의 누구를 닮았는가?"라고 묻습니다.
3. 방사형 연상: 중심 이미지에서 시작해 떠오르는 기억, 감정, 사람을 거미줄처럼 적어 내려갑니다.

⚠️ 사각지대 (Critique):
꿈 해몽 사전 금지: "뱀은 태몽이다" 같은 통속적 해석은 융 심리학에서 무의미합니다. 답은 오직 빌더님의 개인적 맥락(연상) 안에만 있습니다.""",
        "s2_label": "🔍 Stage 2: 역학 (Dynamics)",
        "s2_help": """[수행 방법]
1. 주관적 해석 원칙: 꿈의 모든 등장인물은 외부인이 아니라, **내 내면의 일부(Part of Me)**라고 가정합니다. (예: 화내는 상사 = 내 안의 억압적 자아)
2. 각 부분이 내면에서 어떻게 갈등하고, 누가 주도권을 쥐고 있는지 '역학 관계'를 파악합니다.

⚠️ 사각지대 (Critique):
외부 투사 금지: "저 상사가 나쁜 놈이네"라며 남 탓으로 돌리면 실패입니다. 꿈은 95% 이상이 나 자신의 이야기임을 인정해야 합니다.""",
        "analyze_btn": "▼ 마스터 해석 가동 (ENTER)",
        "s3_label": "🏛️ Stage 3: 해석 (Interpretation)",
        "s4_label": "💎 Stage 4: 의례 (Ritual)",
        "s4_help": """[수행 방법]
해석된 메시지를 기리기(Honor) 위한 구체적인 행동을 합니다.
- 꿈이 '휴식'을 원했나요? -> 실제로 1시간 멍때리기를 하세요.
- 꿈이 '야성'을 원했나요? -> 숲길을 걷거나 소리를 지르세요.

⚠️ 사각지대 (Critique):
지적 유희 경계: 생각만 하고 끝내는 것은 "영혼에 대한 예의"가 아닙니다. 반드시 몸을 움직여 마침표를 찍으십시오.""",
        "mint_btn": "💎 최종 자산 발행 (Mint Token)",
        "update_btn": "🏛️ 자산 정보 업데이트",
        "success_msg": "🎉 채굴 성공! (Minted)",
        "mined_value": "채굴된 가치",
        "bonus_msg": "현재 반감기 보너스",
        "ledger_title": "📊 D-Fi 투명 장부 (Ledger)",
        "ledger_desc": "모든 유저의 활성 자산 현황입니다. (소각된 자산 제외)",
        "burn_title": "🔥 자산 소각 (Buy-back)",
        "burn_desc": "보유한 자산을 현금화(바이백)하고 소각합니다. 꿈 기록은 유지되지만 점수는 0이 됩니다.",
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
        "desc_1_text": "I am an ordinary person worrying about survival. But every night, I mine my <b>Dreams (Unconscious)</b> to awaken my potential. The accumulated <b>Dream Pts</b> are the <b>Proof of Growth</b> showing how deeply I have awakened.",
        "desc_2_title": "2. X-Factor (Reality Change)",
        "desc_2_text": "Insights refined here become content for <b>X (Twitter)</b> and reality. Witness how inspiration transforms into <b>Traffic</b> and <b>Revenue</b>.",
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
        "save_btn": "💾 Save to Vault",
        "delete_btn": "🗑️ Delete",
        "right_title": "🏛️ D-Fi Alchemy",
        "s1_label": "🚀 Stage 1: Association",
        "s1_help": """[How to]
1. Break the dream down into 'Images'.
2. Ask yourself: "What does this remind me of?", "Who does this person resemble in my life?"
3. Radial Association: Write down memories, feelings, and people like a web starting from the central image.

⚠️ Critique:
No Dream Dictionaries: Standard interpretations like "Snake = Wealth" are useless in Jungian psychology. The answer lies only in YOUR personal context.""",
        "s2_label": "🔍 Stage 2: Dynamics",
        "s2_help": """[How to]
1. Subjective Interpretation: Assume every character in the dream is a **Part of Me**, not the actual person. (e.g., Angry Boss = My internal oppressive self)
2. Identify the 'Power Dynamics' and conflicts between these parts within you.

⚠️ Critique:
No Projection: Do not blame the external person ("That boss is bad"). Acknowledge that the dream is 95% about your own inner story.""",
        "analyze_btn": "▼ Run Master Analysis (ENTER)",
        "s3_label": "🏛️ Stage 3: Interpretation",
        "s4_label": "💎 Stage 4: Ritual",
        "s4_help": """[How to]
Perform a concrete action to Honor the message.
- Did the dream ask for 'Rest'? -> Actually sit and do nothing for an hour.
- Did it show 'Wildness'? -> Walk in the woods or shout out loud.

⚠️ Critique:
Avoid Intellectual Games: Thinking alone is not enough. You must move your body to complete the ritual.""",
        "mint_btn": "💎 Mint Token",
        "update_btn": "🏛️ Update Asset",
        "success_msg": "🎉 Minting Successful!",
        "mined_value": "Mined Value",
        "bonus_msg": "Current Halving Bonus",
        "ledger_title": "📊 D-Fi Public Ledger",
        "ledger_desc": "Active assets of all users. (Burned assets excluded)",
        "burn_title": "🔥 Asset Burn (Buy-back)",
        "burn_desc": "Cash out (Buy-back) and burn your assets. Dream records remain, but points become 0.",
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
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False
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
    # 입장 전 화면: 중앙 상단 언어 설정
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
        
        # 입장 전 유저 수
        user_count = get_user_count()
        st.markdown(f"<div style='text-align:center; font-family:Cinzel; color:#D4AF37; margin-top:20px;'>✨ {T['reg_dreamers']} : {user_count:,}</div>", unsafe_allow_html=True)

    st.stop()

# ==========================================
# 🏛️ 2차/3차 관문 및 메인 로직
# ==========================================
T = LANG[st.session_state.language] 

if not st.session_state.user_id:
    # (ID 체크 및 로그인 화면)
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

# 1. 상단 헤더 분할
user_count = get_user_count()

# 2. 메인 로직 함수들
def analyze_dream_engine_v2(context, symbol, dynamics, lang="KO"):
    keywords = {
        "옷": "persona", "clothes": "persona", "uniform": "persona", "mask": "persona", "가면": "persona",
        "쫓김": "shadow", "chased": "shadow", "monster": "shadow", "ghost": "shadow", "attack": "shadow", "도망": "shadow",
        "돈": "wealth", "money": "wealth", "gold": "wealth", "rich": "wealth", "황금": "wealth",
        "집": "self", "house": "self", "room": "self", "building": "self", "clean": "self", "청소": "self",
        "물": "unconscious", "water": "unconscious", "ocean": "unconscious", "sea": "unconscious", "swim": "unconscious",
        "날다": "transcendence", "fly": "transcendence", "sky": "transcendence", "fall": "transcendence",
        "죽음": "rebirth", "death": "rebirth", "funeral": "rebirth", "fire": "rebirth", "불": "rebirth"
    }
    detected_type = "general"
    full_input = (symbol + " " + dynamics + " " + context).lower()
    for key, val in keywords.items():
        if key in full_input: detected_type = val; break

    rituals = {
        "KO": {
            "persona": [f"오늘 하루, 평소 스타일과 정반대의 옷을 입어보세요.", f"'{symbol}'의 이미지를 그리고, 그 위에 새로운 모습을 덧그리세요."],
            "shadow": [f"'{symbol}'에게 귀여운 이름을 지어주세요.", f"쫓기던 상황을 그림으로 그리고, 그 대상을 안아주는 결말을 그리세요."],
            "wealth": [f"지갑의 지폐를 세며 '감사합니다'라고 말하세요.", f"동전을 닦아 '풍요의 씨앗'이라 부르며 보관하세요."],
            "self": [f"내 방의 가구 배치를 하나만 바꿔보세요.", f"방의 가장 구석진 곳을 청소하세요."],
            "general": [f"'{symbol}' 단어를 적어 주머니에 넣고 다니세요.", f"자기 전 '나는 꿈을 기억한다'고 세 번 말하세요."]
        },
        "EN": {
            "persona": [f"Wear a style opposite to your usual one today.", f"Draw '{symbol}' and draw a new version of yourself over it."],
            "shadow": [f"Give a cute name to '{symbol}'.", f"Draw the chasing scene, but change the ending to hugging it."],
            "wealth": [f"Count the bills in your wallet and say 'Thank you'.", f"Clean a coin and keep it as a 'Seed of Abundance'."],
            "self": [f"Change the position of one furniture in your room.", f"Clean the most cornered part of your room."],
            "general": [f"Write '{symbol}' on paper and carry it in your pocket.", f"Say 'I remember my dreams' 3 times before bed."]
        }
    }
    interps = {
        "KO": {
            "persona": {"jung": "사회적 가면(Persona)입니다. 역할의 변화가 필요합니다.", "johnson": "맞지 않는 옷을 입고 있나요? 낡은 역할을 벗으세요.", "ko": "타인의 시선입니다. 본래 모습을 드러내세요."},
            "shadow": {"jung": "그림자(Shadow)입니다. 억눌린 에너지가 통합을 원합니다.", "johnson": "도망치지 마세요. 그 에너지는 당신의 힘입니다.", "ko": "그것은 당신의 분신입니다. 대화해보세요."},
            "wealth": {"jung": "영혼의 고귀한 가치(Self)를 상징합니다.", "johnson": "풍요를 받아들이세요. 창조적 에너지가 흐릅니다.", "ko": "당신은 충분합니다. 잠재력이 현실화될 것입니다."},
            "self": {"jung": "마음의 구조입니다. 확장이 일어나고 있습니다.", "johnson": "내면 공간을 점검하세요. 새로운 재능이 발견됩니다.", "ko": "그 공간의 감정을 기억하세요."},
            "general": {"jung": "무의식의 초대장입니다. 직관적인 해결책이 있습니다.", "johnson": "머리가 아닌 가슴으로 이미지를 품으세요.", "ko": "이것은 당신의 이야기입니다. 어디에 서 있습니까?"}
        },
        "EN": {
            "persona": {"jung": "It represents your Persona. You need a change in your role.", "johnson": "Are you wearing unfit clothes? Shed the old role.", "ko": "It is the gaze of others. Reveal your true self."},
            "shadow": {"jung": "It is your Shadow. Repressed energy seeks integration.", "johnson": "Do not run. That energy is your power.", "ko": "It is your alter ego. Talk to it."},
            "wealth": {"jung": "It symbolizes the noble value of the Self.", "johnson": "Accept abundance. Creative energy is flowing.", "ko": "You are enough. Potential will manifest."},
            "self": {"jung": "It is the structure of your mind. Expansion is happening.", "johnson": "Check your inner space. New talents are found.", "ko": "Remember the feeling of that space."},
            "general": {"jung": "An invitation from the unconscious. It holds intuitive solutions.", "johnson": "Feel the image with your heart, not your head.", "ko": "This is your story. Where do you stand?"}
        }
    }
    selected_ritual = random.choice(rituals[lang].get(detected_type, rituals[lang]["general"]))
    text_db = interps[lang].get(detected_type, interps[lang]["general"])
    return { "jung": text_db["jung"], "johnson": text_db["johnson"], "ko": text_db["ko"], "ritual": selected_ritual }

def calculate_dream_quality_score(context, s1, s2, s3, s4, current_halving_multiplier):
    base_score = 1000 
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
                        elif "Tokens" in score_text: part = score_text.split(" Tokens")[0]
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
                        elif "Tokens" in score_text: part = score_text.split(" Tokens")[0]
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

# 🟢 [CORE FIX] 메인 화면 최상단 레이아웃 (우측 상단 배치)
c_header_1, c_header_2 = st.columns([7, 3])
with c_header_1:
    st.markdown(f"### 🪙 {T['dash_global']} (Era: {current_era + 1})")
with c_header_2:
    # 우측 상단: 언어 설정 & Dreamers
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

# 👑 [ADMIN PANEL] - 메인 화면 중앙 배치 (사이드바 아님!)
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
                else:
                    st.error("Access Denied")
    else:
        # 관리자 모드 잠금 해제됨 - 대시보드 표시
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
        
        # 🚑 긴급 복구 버튼 (추가됨)
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
                            s1_loaded = d.get('symbol', "")
                            s2_loaded = d.get('block', "")
                            st.session_state.s1_val = s1_loaded
                            st.session_state.s2_val = s2_loaded
                            st.session_state['s1_key'] = s1_loaded
                            st.session_state['s2_key'] = s2_loaded
                            st.session_state.s4_val = d.get('ritual_self', "")
                            loaded_analysis = d.get('analysis', "") 
                            st.session_state.s3_val = loaded_analysis 
                            st.session_state['s3_key'] = loaded_analysis 
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
        for k in ['s1_key', 's2_key', 's3_key']:
            if k in st.session_state: del st.session_state[k]
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
    if 's1_key' not in st.session_state: st.session_state.s1_key = st.session_state.s1_val
    if 's2_key' not in st.session_state: st.session_state.s2_key = st.session_state.s2_val

    st.text_area(T['s1_label'], height=70, key="s1_key", help=T['s1_help'])
    st.text_area(T['s2_label'], height=70, key="s2_key", help=T['s2_help'])
    
    if st.button(T['analyze_btn']):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        if s1_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            result = analyze_dream_engine_v2(st.session_state.dream_context, s1_input, s2_input, st.session_state.language)
            analysis_text = f"""[D-Fi Analysis]\n\n1. C.G. Jung:\n"{result['jung']}"\n\n2. Robert A. Johnson:\n"{result['johnson']}"\n\n3. Projective Work:\n"{result['ko']}" """
            st.session_state['s3_key'] = analysis_text 
            st.session_state.s3_val = analysis_text
            st.session_state.s4_val = result['ritual']
            st.toast("Analysis Complete!")
            time.sleep(0.1) 
            st.rerun()

    if 's3_key' not in st.session_state: st.session_state.s3_key = st.session_state.s3_val
    st.text_area(T['s3_label'], height=350, disabled=False, key="s3_key")

    with st.form("mint_form"):
        st.markdown(f"#### {T['s4_label']}", help=T['s4_help'])
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 Prev Value: {st.session_state.existing_value}")
        s4 = st.text_input("Action", value=st.session_state.s4_val)
        final_btn = T['update_btn'] if st.session_state.is_minted else T['mint_btn']
        
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = calculate_dream_quality_score(st.session_state.dream_context, st.session_state.s1_val, st.session_state.s2_val, st.session_state.s3_val, s4, mining_multiplier)
                new_val_str = f"Value: {token_val:,} Dream Pts"
                payload = {"symbol": st.session_state.s1_val, "block": st.session_state.s2_val, "ritual_self": s4, "meaning": new_val_str, "analysis": st.session_state.s3_val}
                
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


