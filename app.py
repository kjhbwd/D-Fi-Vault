import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd
import pytz

# [SYSTEM CONFIG]
st.set_page_config(
    page_title="Dream-Fi Vault v27.1", 
    page_icon="🏛️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 🔒 1. 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "2026"

# 🛡️ 2. 관리자 보안 설정
ADMIN_USER = "김지호bwd"
MASTER_KEY = "1234"

# 🪙 [TOKENOMICS]
MAX_SUPPLY = 21000000
HALVING_STEP = 2100000
DAILY_CAP = 10000 # 하루 채굴 한도

# 🟢 [CORE] 언어 및 시간 설정
if 'language' not in st.session_state: st.session_state.language = "KO"
KST = pytz.timezone('Asia/Seoul')

# ==========================================
# 📜 [WHITE PAPER] - 백서 내용
# ==========================================
WHITE_PAPER_TEXT = """
### 📜 Dream-Fi White Paper (Ver 1.1)
#### : The Alchemy of the Unconscious (무의식의 연금술)

---

#### 1. 서문 (Problem Statement)
"현실의 결핍은 무의식의 풍요로 채워져야 한다."
현대인은 생존 경쟁에 매몰되어 자신의 잠재력을 잊고 살아갑니다. Dream-Fi는 매일 밤 버려지는 무의식(꿈)을 채굴하고 자산화하여, 평범한 개인이 자신의 운명을 바꾸는 퀀텀 점프(Quantum Jump)를 지원합니다.

#### 2. 솔루션 & 기술 (Methodology)
우리는 로버트 존슨의 4단계 프로토콜(4-Step Protocol)을 통해 무형의 꿈을 유형의 자산(Block)으로 변환합니다.
1. **연상 (Association):** 이미지의 직관적 연결.
2. **역학 (Dynamics):** 내면 인격들과의 대화.
3. **해석 (Interpretation):** 무의식의 메시지 해독.
4. **의례 (Ritual):** 깨달음을 현실의 구체적 행동으로 옮기는 행동 증명(Proof of Action).

#### 3. 토크노믹스 (Tokenomics)
비트코인 모델을 차용하여 내면 자산의 가치를 보존합니다.
* **총 발행량:** 21,000,000 Pts (희소성 확보)
* **반감기:** 2,100,000 Pts 채굴 시마다 보상 감소
* **일일 한도:** 10,000 Pts (무분별한 인플레이션 방지)

#### 4. 로드맵 및 비전 (Roadmap & Ecosystem)
Dream-Fi의 궁극적인 목표는 단순한 기록 저장소가 아닌, 실질적인 부(Wealth)의 창출과 순환입니다.

* **비즈니스 인큐베이팅 (From Dream to Business):**
SNS 광고 수익은 기초적인 단계일 뿐입니다. 우리는 꿈에서 얻은 창의적인 영감과 아이디어를 실제 사업 모델과 비즈니스로 연결합니다. 무의식의 통찰이 구체적인 제품과 서비스가 되어, 유저가 진정한 경제적 자유를 얻도록 돕습니다.

* **자발적 기여와 바이백 (Virtuous Cycle of Buy-back):**
이 시스템을 통해 사업적으로 성공하고 경제적 자유를 얻은 선구자들은 자발적으로 생태계에 기여하게 됩니다. 이렇게 조성된 생태계 후원금(Ecosystem Fund)은 다시 커뮤니티로 환원되어, 유저들이 열심히 채굴한 Dream Pts를 현실의 재화로 매입(Buy-back)하는 재원으로 사용됩니다.

결국 "꿈(채굴) → 사업화(성공) → 후원(펀드 조성) → 바이백(현금화)"이라는 완벽한 가치 순환 구조가 완성됩니다.
"""

# ==========================================
# 📚 [CONTENT PACK] - 가이드 텍스트
# ==========================================
GUIDE_S1_FULL = """
**[실례 상황 설정]**
꿈 내용: "나는 낡고 허름한 내 옛날 초등학교 교실에 앉아 있다. 칠판 앞에 검은 옷을 입은 낯선 남자가 서 있는데, 나에게 오래된 시계를 건네주며 '이걸 고치라'고 말한다. 나는 고칠 줄 몰라 당황한다."

**1. 연상 (Associations): 개인적 의미의 방사형 연결**
꿈의 이미지를 사전적 정의(보편적 상징)로 해석하지 마십시오. 존슨은 '방사형 연상(Starburst)'을 강조합니다. 꼬리에 꼬리를 무는 연상(A→B→C)이 아니라, 이미지(A)를 중심에 두고 떠오르는 직관(A→1, A→2, A→3)을 포착해야 합니다.
"""

GUIDE_S2_FULL = """
**2. 역학 (Dynamics): 내면의 인격들과 연결하기**
꿈의 모든 등장인물과 사물은 '나 자신의 분열된 자아'입니다. 역학 단계는 연상된 이미지들이 내면에서 어떤 '부분'을 담당하고 있는지 식별하는 과정입니다.
"""

GUIDE_S3_FULL = """
**3. 해석 (Interpretations): 메시지의 통합**
연상과 역학을 종합하여 꿈이 보내는 '보상적(Compensatory) 메시지'를 읽어냅니다. 꿈은 의식이 한쪽으로 치우쳤을 때 균형을 맞추려 합니다.
"""

GUIDE_S4_FULL = """
**4. 의례 (Rituals): 구체적 행동으로의 육화 (가장 중요)**
빌더님, 이 단계가 로버트 존슨 꿈 작업의 핵심입니다. 깨달음(Insight)만으로는 부족합니다. 반드시 물리적인 행동(Action)이 따라야 무의식이 변화를 인지합니다.
"""

LANG = {
    "KO": {
        "title": "Dream-Fi : 무의식의 연금술",
        "manifesto_quote": '"현실의 결핍은 무의식의 풍요로 채워진다.<br>이것은 평범한 개인이 자신의 운명을 바꾸는 <b>퀀텀 점프 실험실</b>입니다."',
        "tokenomics": "🪙 Tokenomics : 비트코인 모델 적용",
        "token_desc": "• 총 발행 한도: 21,000,000 Dream Pts<br>• 반감기(Halving): 매 2,100,000 Pts 채굴 시 보상 50% 감소",
        "desc_1_title": "1. 성장의 시각화 (Visualizing Growth)",
        "desc_1_text": "저는 생존을 고민하는 평범한 사람입니다. 하지만 매일 밤 <b>꿈(무의식)</b>을 채굴하여 제 잠재력을 깨우고 있습니다. 여기에 쌓이는 <b>Dream Pts</b>는 제가 얼마나 깊이 각성했는지를 보여주는 <b>성장의 증명</b>입니다.",
        "desc_2_title": "2. 현실의 변화 (X-Factor)",
        "desc_2_text": "이곳에서 제련된 통찰은 <b>SNS</b>와 현실의 콘텐츠가 됩니다. 무의식의 영감이 어떻게 <b>노출수(Traffic)</b>와 <b>수익(Revenue)</b>으로 변환되는지 목격하십시오.",
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
        "save_btn": "💾 꿈 내용 저장 (Save Dream)",
        "delete_btn": "🗑️ 삭제 (Delete)",
        "right_title": "🏛️ Dream-Fi 연금술 (4-Step)",
        "guide_s1": GUIDE_S1_FULL,
        "guide_s2": GUIDE_S2_FULL,
        "guide_s3": GUIDE_S3_FULL,
        "guide_s4": GUIDE_S4_FULL,
        "s1_label": "🚀 Stage 1: 연상 (Association)",
        "s2_label": "🔍 Stage 2: 역학 (Dynamics)",
        "s3_label": "🏛️ Stage 3: 해석 (Interpretation)",
        "s4_label": "💎 Stage 4: 의례 (Ritual)",
        "mint_btn": "💎 최종 자산 발행 (Mint Token)",
        "update_btn": "🏛️ 자산 정보 업데이트",
        "success_msg": "🎉 채굴 성공! (Minted)",
        "mined_value": "채굴된 가치",
        "bonus_msg": "현재 반감기 보너스",
        "ledger_title": "📊 Dream-Fi 투명 장부 (Ledger)",
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
        "title": "Dream-Fi : Alchemy of the Unconscious",
        "manifesto_quote": '"The lack in reality is filled by the abundance of the unconscious."',
        "tokenomics": "🪙 Tokenomics : Bitcoin Model",
        "token_desc": "Max Supply: 21M / Halving every 2.1M",
        "desc_1_title": "Visualizing Growth",
        "desc_1_text": "Mining dreams to awaken potential.",
        "desc_2_title": "Reality Change",
        "desc_2_text": "Turning insights into reality.",
        "login_placeholder": "Enter Access Code (2026)",
        "login_btn": "🗝️ Enter",
        "login_error": "⛔ Invalid Code",
        "id_check_title": "👤 Identity Check",
        "id_check_desc": "Enter Nickname.",
        "next_btn": "Next",
        "welcome": "Welcome",
        "open_vault": "Open Vault",
        "hint_btn": "Hint",
        "register_msg": "Creating vault.",
        "register_btn": "Register",
        "pin_placeholder": "PIN (4-digit)",
        "hint_placeholder": "Hint",
        "dash_global": "Global Mined",
        "dash_difficulty": "Difficulty",
        "dash_my_asset": "My Assets",
        "logout": "Logout",
        "left_title": "📓 Raw Material",
        "load_dreams": "Load Dreams",
        "load_btn": "Load",
        "reset_btn": "Reset",
        "status_edit": "Edit Mode",
        "status_new": "New Entry",
        "save_btn": "💾 Save Dream Content",
        "delete_btn": "Delete",
        "right_title": "🏛️ Dream-Fi Alchemy",
        "guide_s1": "Context hidden.",
        "guide_s2": "Context hidden.",
        "guide_s3": "Context hidden.",
        "guide_s4": "Context hidden.",
        "s1_label": "Stage 1: Association",
        "s2_label": "Stage 2: Dynamics",
        "s3_label": "Stage 3: Interpretation",
        "s4_label": "Stage 4: Ritual",
        "mint_btn": "Mint Token",
        "update_btn": "Update Asset",
        "success_msg": "Minting Successful!",
        "mined_value": "Mined Value",
        "bonus_msg": "Halving Bonus",
        "ledger_title": "Public Ledger",
        "ledger_desc": "Active assets.",
        "burn_title": "Asset Burn",
        "burn_desc": "Burn your assets.",
        "burn_btn": "Burn",
        "burn_success": "Burn Complete.",
        "admin_unlock": "Admin Unlock",
        "master_key_ph": "Master Key",
        "reg_dreamers": "Dreamers"
    }
}

# --- CSS: 디자인 (모바일 타이틀 최적화 & 로고 완전 삭제) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
    
    /* 1. 기본 배경 및 폰트 설정 */
    .stApp, .stApp > header, .stApp > footer, .stApp > main { 
        background-color: #050505 !important; 
        color: #FFFFFF !important; 
    }
    
    /* 2. 한글 줄바꿈 최적화 */
    p, div, span, label, h1, h2, h3, h4, h5, h6, li, button {
        word-break: keep-all !important; 
        overflow-wrap: break-word !important; 
    }

    /* 3. [초강력] Streamlit 로고/메뉴/푸터 강제 삭제 */
    header { visibility: hidden !important; height: 0px !important; }
    div[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }
    footer { display: none !important; visibility: hidden !important; }
    div[class*="viewerBadge"] { display: none !important; }
    .stDeployButton { display: none !important; }
    #MainMenu { display: none !important; }
    
    /* 4. [타이틀 최적화] clamp 함수 사용 (자동 크기 조절) */
    .responsive-title {
        /* 최소 22px ~ 화면의 6% ~ 최대 50px */
        font-size: clamp(22px, 6vw, 50px) !important;
        font-weight: 900 !important;
        color: #D4AF37 !important;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3);
        font-family: 'Malgun Gothic', sans-serif;
        line-height: 1.3 !important;
        width: 100%;
        display: block;
    }

    /* 5. UI 컴포넌트 스타일링 */
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333 !important; }
    
    .streamlit-expanderHeader { background-color: #1A1A1A !important; border-radius: 5px !important; border: 1px solid #333 !important; }
    .streamlit-expanderHeader p { color: #D4AF37 !important; font-weight: bold !important; font-size: 1.0em !important; }
    .streamlit-expanderContent { background-color: #111111 !important; color: #E0E0E0 !important; border-left: 2px solid #D4AF37 !important; }
    
    button { background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; background-color: #D4AF37 !important; border: none !important; opacity: 1 !important; box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important; padding: 0.5rem 1rem !important; border-radius: 0.5rem !important; }
    button p, button div, button span { color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important; }
    button:hover { background: #FFD700 !important; transform: scale(1.02); }
    
    .stTextArea textarea, .stTextInput input { background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important; }
    label, .stMarkdown label, p, .stMetricLabel { color: #E0E0E0 !important; }
    .stMetricValue { color: #D4AF37 !important; }
    div[data-testid="column"] { background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px; }
    
    .dreamer-count-header { font-family: 'Cinzel', serif; color: #D4AF37; font-size: 1.2em; font-weight: bold; text-align: right; }
    .quote-box { background-color: #1A1A1A !important; border-left: 4px solid #D4AF37 !important; padding: 20px !important; margin: 20px 0 !important; color: #E0E0E0 !important; font-style: italic; font-size: 1.2em; border-radius: 5px; }
    .defi-desc-box { background-color: #111111 !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #333 !important; margin-top: 30px; margin-bottom: 30px; }
    .defi-desc-text { color: #BBBBBB !important; font-size: 1.0em; line-height: 1.8; font-family: sans-serif; }
    .highlight-gold { color: #FDB931 !important; font-weight: bold; font-size: 1.2em; margin-bottom: 15px; display: block; }
    .highlight-bold { color: #FFFFFF !important; font-weight: bold; }
    
    div[data-testid="stProgress"] > div > div { background-color: #D4AF37 !important; }
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
# 🟢 [CORE FUNCTION] 기본 기능
# ==========================================
def get_user_count():
    try:
        count_res = supabase.table("users").select("username", count="exact").execute()
        return count_res.count if count_res.count else 0
    except: return 0

def get_today_mined_count(user_id):
    try:
        now_kst = datetime.datetime.now(KST)
        start_of_day = now_kst.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        res = supabase.table("dreams").select("*").eq("user_id", user_id).gte("created_at", start_of_day).execute()
        
        today_total = 0
        if res.data:
            for d in res.data:
                meaning = d.get('meaning', "")
                if meaning and "Value:" in meaning:
                    try:
                        score_text = meaning.split("Value: ")[1]
                        if "Dream Pts" in score_text: part = score_text.split(" Dream Pts")[0]
                        else: part = "0"
                        today_total += int(part.replace(",", ""))
                    except: pass
        return today_total
    except: return 0

# ==========================================
# 🚪 1차 관문: Manifesto
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
        # 🟢 [타이틀 변경] HTML 클래스 적용 (responsive-title)
        st.markdown(f"<div class='responsive-title'>{T['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote-box'>{T['manifesto_quote']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='defi-desc-box'>
    <div class='defi-desc-text'>
        <span class='highlight-gold'>{T['tokenomics']}</span>
        <p>{T['token_desc']}</p>
        <p><span class='highlight-bold'>{T['desc_1_title']}</span><br>
        {T['desc_1_text']}</p>
        <p><span class='highlight-bold'>{T['desc_2_title']}</span><br>
        {T['desc_2_text']}</p>
        <hr style='border-color: #333; margin: 20px 0;'>
        <p style='font-style: italic; color: #888; font-size: 0.9em; text-align: center; line-height: 1.6; word-break: keep-all;'>
            "어쩌면, 무의식의 연금술로 삶이 바뀐 선구자들이 자발적으로 이 생태계에 씨앗(Fund)을 뿌릴지도 모릅니다.
            그 후원금이 모인다면, 당신의 Dream Pts는 언젠가 현실의 재화로 '바이백(Buy-back)' 되어 돌아올 수도 있겠죠.
            마치 꿈이 현실이 되는 그날처럼 말입니다."
        </p>
    </div>
</div>""", unsafe_allow_html=True)
        
        with st.expander("📜 Dream-Fi White Paper (백서 읽기)"):
            st.markdown(WHITE_PAPER_TEXT)
        
        with st.form("gate_form"):
            input_code = st.text_input("Entry Code", type="password", placeholder=T['login_placeholder'])
            if st.form_submit_button(T['login_btn']):
                if input_code.strip() == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.toast("✅ Access Granted.")
                    time.sleep(0.5)
                    st.rerun()
                else: st.error(T['login_error'])
    st.stop()

# ==========================================
# 🏛️ 2차/3차 관문
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

def get_ledger_data():
    try:
        res_all = supabase.table("dreams").select("*").execute()
        ledger = {} 
        if res_all.data:
            for d in res_all.data:
                if d.get('is_burned', False) is True: continue
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
        res_all = supabase.table("dreams").select("*").execute()
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
                is_burned_val = d.get('is_burned', False)
                if d['user_id'] == current_user and is_burned_val is not True:
                    my_total += score
                    my_count += 1
        
        halving_era = global_mined // HALVING_STEP
        current_multiplier = 1 / (2 ** halving_era)
        return my_total, my_count, global_mined, current_multiplier, halving_era
    except: return 0, 0, 0, 1, 0

my_assets, my_mining_count, global_supply, mining_multiplier, current_era = get_global_status(st.session_state.user_id)
supply_progress = min(1.0, global_supply / MAX_SUPPLY)

today_mined = get_today_mined_count(st.session_state.user_id)
daily_remaining = max(0, DAILY_CAP - today_mined)
daily_progress = min(1.0, today_mined / DAILY_CAP)

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

st.markdown("---")
st.markdown(f"**⚡ Daily Mining Energy** ({today_mined:,} / {DAILY_CAP:,} Pts)")
st.progress(daily_progress)
if daily_remaining <= 0:
    st.warning("🌙 오늘은 더 이상 채굴할 수 없습니다. 내일 다시 도전하세요!")

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
        dream_raw = st.text_area("Dream Content", value=st.session_state.dream_context, height=680, help="스크롤하여 긴 내용을 확인하세요.")
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
    now_hour = datetime.datetime.now(KST).hour
    is_early_bird = 4 <= now_hour < 8
    
    st.markdown(f"### {T['right_title']}")
    
    if is_early_bird:
        st.markdown("#### 🌞 Early Bird Active (x1.5 Bonus)")
    else:
        st.markdown("#### ☕ Standard Mode (x1.0)")
    
    with st.form("mint_form"):
        with st.expander(f"💡 {T['s1_label']} (가이드 보기)"):
            st.markdown(T['guide_s1'])
        st.text_area("Enter Associations", key="s1_val", height=120, label_visibility="collapsed")

        with st.expander(f"💡 {T['s2_label']} (가이드 보기)"):
            st.markdown(T['guide_s2'])
        st.text_area("Enter Dynamics", key="s2_val", height=120, label_visibility="collapsed")

        with st.expander(f"💡 {T['s3_label']} (가이드 보기)"):
            st.markdown(T['guide_s3'])
        st.text_area("Enter Interpretation", key="s3_val", height=150, label_visibility="collapsed")

        with st.expander(f"💡 {T['s4_label']} (가이드 보기)"):
            st.markdown(T['guide_s4'])
        
        if st.session_state.is_minted and st.session_state.existing_value: 
            st.info(f"📉 Prev Value: {st.session_state.existing_value}")
        
        st.text_area("Enter Ritual Action", key="s4_val", height=100, label_visibility="collapsed")
        
        final_btn = T['update_btn'] if st.session_state.is_minted else T['mint_btn']
        
        if st.form_submit_button(final_btn):
            if not st.session_state.current_dream_id:
                st.error("⚠️ 왼쪽의 [꿈 내용 저장] 버튼을 먼저 눌러 내용을 확정해주세요!")
            else:
                errors = []
                if not st.session_state.dream_context: errors.append("꿈 내용(왼쪽)")
                if not st.session_state.s1_val: errors.append("1단계(연상)")
                if not st.session_state.s2_val: errors.append("2단계(역학)")
                if not st.session_state.s3_val: errors.append("3단계(해석)")
                if not st.session_state.s4_val: errors.append("4단계(의례)")
                
                if not errors:
                    if daily_remaining <= 0:
                        st.error("🛑 오늘의 채굴 한도(10,000 Pts)를 모두 소진했습니다. 내일 다시 시도하세요!")
                    else:
                        base_score_raw = 1000 + (len(st.session_state.dream_context) * 2) + \
                                         (len(st.session_state.s1_val) * 5) + \
                                         (len(st.session_state.s2_val) * 5) + \
                                         (len(st.session_state.s3_val) * 5) + \
                                         (len(st.session_state.s4_val) * 10)
                        
                        early_bonus = 1.5 if is_early_bird else 1.0
                        calculated_score = int(base_score_raw * mining_multiplier * early_bonus)
                        final_score = min(calculated_score, daily_remaining)
                        
                        new_val_str = f"Value: {final_score:,} Dream Pts"
                        
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
                        
                        bonus_text = f"(Early Bird x1.5)" if is_early_bird else ""
                        msg.markdown(f"""
                        <div style="background-color:#D4AF37; padding:20px; border-radius:10px; text-align:center; border:2px solid #FFFFFF;">
                            <h2 style='color:black; margin:0;'>{T['success_msg']}</h2>
                            <h3 style='color:black; margin:10px 0;'>💎 +{final_score:,} Dream Pts</h3>
                            <p style='color:black;'>Halving x{mining_multiplier} {bonus_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(3) 
                        st.rerun()
                else:
                    st.error(f"⚠️ 채굴 실패: {', '.join(errors)}이(가) 비어있습니다.")
