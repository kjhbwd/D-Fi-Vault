import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd # 데이터프레임 출력을 위해 추가

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v13.1", page_icon="🏛️", layout="wide")

# 🔒 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "2026"

# 🪙 [TOKENOMICS]
MAX_SUPPLY = 21000000
HALVING_STEP = 2100000

# ==========================================
# 🌐 [LANGUAGE PACK]
# ==========================================
LANG = {
    "KO": {
        "title": "D-Fi : 무의식의 연금술",
        "manifesto_quote": '"현실의 결핍은 무의식의 풍요로 채워진다.<br>이것은 평범한 개인이 자신의 운명을 바꾸는 <b>퀀텀 점프 실험실</b>입니다."',
        "tokenomics": "🪙 Tokenomics : 비트코인 모델 적용",
        "token_desc": "• 총 발행 한도: 21,000,000 Dream Pts<br>• 반감기(Halving): 매 2,100,000 Pts 채굴 시 보상 50% 감소",
        "login_placeholder": "입장 코드를 입력하세요",
        "login_btn": "🗝️ 무의식 광산 입장하기",
        "login_error": "⛔ 유효하지 않은 코드입니다.",
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
        "dash_my_asset": "My Total Assets",
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
        "s1_help": "꿈을 훑어보며 떠오르는 이미지, 감정, 단어를 적으세요. '이 이미지를 보고 어떤 느낌이 드지?'라고 자문해보세요.",
        "s2_label": "🔍 Stage 2: 역학 (Dynamics)",
        "s2_help": "그 상징이 꿈에서 어떤 행동을 했나요? 나는 어떤 감정을 느꼈나요?",
        "analyze_btn": "▼ 마스터 해석 가동 (ENTER)",
        "s3_label": "🏛️ Stage 3: 해석 (Interpretation)",
        "s4_label": "💎 Stage 4: 의례 (Ritual)",
        "s4_help": "꿈의 에너지를 현실로 가져오는 구체적인 행동입니다.",
        "mint_btn": "💎 최종 자산 발행 (Mint Token)",
        "update_btn": "🏛️ 자산 정보 업데이트",
        "success_msg": "🎉 채굴 성공! (Minted)",
        "mined_value": "채굴된 가치",
        "bonus_msg": "현재 반감기 보너스",
        "ledger_title": "📊 D-Fi 투명 장부 (Ledger)",
        "ledger_desc": "모든 유저의 자산 보유 현황입니다. (바이백 기준 데이터)"
    },
    "EN": {
        "title": "D-Fi : Alchemy of the Unconscious",
        "manifesto_quote": '"The lack in reality is filled by the abundance of the unconscious.<br>This is a <b>Quantum Jump Laboratory</b> where an individual changes their destiny."',
        "tokenomics": "🪙 Tokenomics : Bitcoin Model",
        "token_desc": "• Max Supply: 21,000,000 Dream Pts<br>• Halving: Reward -50% every 2,100,000 Pts mined",
        "login_placeholder": "Enter Access Code",
        "login_btn": "🗝️ Enter the Mine",
        "login_error": "⛔ Invalid Code",
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
        "dash_my_asset": "My Total Assets",
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
        "s1_help": "Write down images, feelings, words from the dream. Ask yourself: 'What feeling does this image give me?'",
        "s2_label": "🔍 Stage 2: Dynamics",
        "s2_help": "What did the symbol do in the dream? How did you feel?",
        "analyze_btn": "▼ Run Master Analysis (ENTER)",
        "s3_label": "🏛️ Stage 3: Interpretation",
        "s4_label": "💎 Stage 4: Ritual",
        "s4_help": "Concrete action to bring dream energy into reality.",
        "mint_btn": "💎 Mint Token",
        "update_btn": "🏛️ Update Asset",
        "success_msg": "🎉 Minting Successful!",
        "mined_value": "Mined Value",
        "bonus_msg": "Current Halving Bonus",
        "ledger_title": "📊 D-Fi Public Ledger",
        "ledger_desc": "Real-time asset status of all users. (Standard for Buy-back)"
    }
}

# --- CSS: 디자인 ---
st.markdown("""
    <style>
    .stApp, .stApp > header, .stApp > footer, .stApp > main { background-color: #050505 !important; color: #FFFFFF !important; }
    button { background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; background-color: #D4AF37 !important; border: none !important; opacity: 1 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important; padding: 0.5rem 1rem !important; border-radius: 0.5rem !important; }
    button p, button div, button span { color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important; }
    button:hover { background: #FFD700 !important; transform: scale(1.02); }
    .stTextArea textarea, .stTextInput input { background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important; }
    label, .stMarkdown label, p, .stMetricLabel { color: #E0E0E0 !important; }
    .stMetricValue { color: #D4AF37 !important; }
    div[data-testid="column"] { background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px; }
    div[data-baseweb="popover"], div[data-baseweb="tooltip"] { background-color: #1A1A1A !important; border: 1px solid #D4AF37 !important; border-radius: 8px !important; max-width: 400px !important; }
    div[data-baseweb="popover"] > div, div[data-baseweb="tooltip"] > div { color: #FFFFFF !important; background-color: #1A1A1A !important; }
    header, footer { visibility: hidden !important; } .stAlert { display: none; } 
    .main-title { font-size: 2.5em; font-weight: 900; color: #D4AF37 !important; text-align: center; margin-bottom: 20px; text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); font-family: 'Malgun Gothic', sans-serif; }
    .quote-box { background-color: #1A1A1A !important; border-left: 4px solid #D4AF37 !important; padding: 20px !important; margin: 20px 0 !important; color: #E0E0E0 !important; font-style: italic; font-size: 1.2em; border-radius: 5px; }
    .defi-desc-box { background-color: #111111 !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #333 !important; margin-top: 30px; margin-bottom: 30px; }
    .defi-desc-text { color: #BBBBBB !important; font-size: 1.0em; line-height: 1.8; font-family: sans-serif; }
    .highlight-gold { color: #FDB931 !important; font-weight: bold; font-size: 1.2em; margin-bottom: 15px; display: block; }
    .highlight-bold { color: #FFFFFF !important; font-weight: bold; }
    .faint-hint { color: #888888 !important; font-size: 0.9em; margin-top: 25px; font-style: italic; text-align: center; border-top: 1px solid #333; padding-top: 20px;}
    
    /* 장부 테이블 스타일 */
    .stDataFrame { border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE]
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'auth_step' not in st.session_state: st.session_state.auth_step = "check_id"
if 'temp_username' not in st.session_state: st.session_state.temp_username = ""
if 'language' not in st.session_state: st.session_state.language = "KO"

for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
    if key not in st.session_state: st.session_state[key] = "" if key != 'current_dream_id' else None
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB Connection Error")

# 🟢 [SIDEBAR] 언어 설정 및 장부(Ledger)
with st.sidebar:
    lang_choice = st.radio("Language / 언어", ["KO", "EN"], horizontal=True)
    if lang_choice != st.session_state.language:
        st.session_state.language = lang_choice
        st.rerun()

# 언어 팩 로드
T = LANG[st.session_state.language]

# 🟢 [CORE FUNCTION] 모든 유저 자산 계산 (장부 생성용)
def get_ledger_data():
    try:
        # 모든 꿈 데이터 가져오기 (컬럼: user_id, meaning)
        res_all = supabase.table("dreams").select("user_id, meaning").execute()
        ledger = {} # {user_id: [total_score, count]}
        
        if res_all.data:
            for d in res_all.data:
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
                
                if uid not in ledger: ledger[uid] = [0, 0] # [총점, 개수]
                ledger[uid][0] += score
                ledger[uid][1] += 1
                
        # 리스트로 변환
        ledger_list = []
        for uid, data in ledger.items():
            ledger_list.append({"User ID": uid, "Total Assets (Pts)": data[0], "Mined Blocks": data[1]})
            
        # 데이터프레임 생성 및 정렬
        df = pd.DataFrame(ledger_list)
        if not df.empty:
            df = df.sort_values(by="Total Assets (Pts)", ascending=False).reset_index(drop=True)
            # 순위(Rank) 컬럼 추가
            df.index = df.index + 1
            df.index.name = "Rank"
        return df
    except: return pd.DataFrame()

# 🟢 [SIDEBAR] 장부 표시
if st.session_state.access_granted:
    with st.sidebar:
        st.markdown("---")
        with st.expander(f"{T['ledger_title']}", expanded=False):
            st.caption(T['ledger_desc'])
            if st.button("🔄 Refresh Ledger"):
                st.rerun()
            df_ledger = get_ledger_data()
            if not df_ledger.empty:
                st.dataframe(df_ledger, use_container_width=True)
            else:
                st.write("No data yet.")

# ==========================================
# 🧠 [CORE LOGIC] 해석 엔진
# ==========================================
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

# ==========================================
# 🚪 1차 관문 & 2차 관문 (동일 로직, 텍스트만 T[] 사용)
# ==========================================
if not st.session_state.access_granted:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='main-title'>{T['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote-box'>{T['manifesto_quote']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='defi-desc-box'>
    <div class='defi-desc-text'>
        <span class='highlight-gold'>{T['tokenomics']}</span>
        <p>{T['token_desc']}</p>
        <p>1. {T['desc_1_title']}<br>... (Manifesto omitted for brevity)</p>
    </div>
</div>""", unsafe_allow_html=True)
        
        with st.form("gate_form"):
            input_code = st.text_input("Entry Code", type="password", placeholder=T['login_placeholder'])
            if st.form_submit_button(T['login_btn']):
                if input_code == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.toast("✅ Access Granted.")
                    time.sleep(0.5)
                    st.rerun()
                else: st.error(T['login_error'])
    st.stop()

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
                        res = supabase.table("users").select("*").eq("username", input_id).execute()
                        st.session_state.temp_username = input_id
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
# 🏛️ MAIN APP
# ==========================================
# Global Status & Halving
def get_global_status(current_user):
    try:
        res_all = supabase.table("dreams").select("meaning, user_id").execute()
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
                if d['user_id'] == current_user:
                    my_total += score
                    my_count += 1
        
        halving_era = global_mined // HALVING_STEP
        current_multiplier = 1 / (2 ** halving_era)
        return my_total, my_count, global_mined, current_multiplier, halving_era
    except: return 0, 0, 0, 1, 0

my_assets, my_mining_count, global_supply, mining_multiplier, current_era = get_global_status(st.session_state.user_id)
supply_progress = min(1.0, global_supply / MAX_SUPPLY)

st.markdown(f"### 🪙 {T['dash_global']} (Era: {current_era + 1})")
st.progress(supply_progress)
c_d1, c_d2, c_d3, c_d4 = st.columns(4)
with c_d1: st.metric(T['dash_global'], f"{global_supply:,} / {MAX_SUPPLY:,}", delta=f"{supply_progress*100:.2f}%")
with c_d2: st.metric(T['dash_difficulty'], f"Reward x{mining_multiplier}", delta="Halving Active" if current_era > 0 else "Genesis Era", delta_color="inverse")
with c_d3: st.metric(T['dash_my_asset'], f"{my_assets:,} Dream Pts", delta=f"{my_mining_count} blocks")
with c_d4: 
    if st.button(T['logout']):
        for key in list(st.session_state.keys()): del st.session_state[key]
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
