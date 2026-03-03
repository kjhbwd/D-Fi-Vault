import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd
import pytz

# [SYSTEM CONFIG]
st.set_page_config(
    page_title="Dream-Pi Vault v30.1", 
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
### 📜 Dream-Pi White Paper (Ver 1.1)
#### : The Alchemy of the Unconscious (무의식의 연금술)

---

#### 1. 서문 (Problem Statement)
"현실의 결핍은 무의식의 풍요로 채워져야 한다."
현대인은 생존 경쟁에 매몰되어 자신의 잠재력을 잊고 살아갑니다. Dream-Pi는 매일 밤 버려지는 무의식(꿈)을 채굴하고 자산화하여, 평범한 개인이 자신의 운명을 바꾸는 퀀텀 점프(Quantum Jump)를 지원합니다.

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
Dream-Pi의 궁극적인 목표는 단순한 기록 저장소가 아닌, 실질적인 부(Wealth)의 창출과 순환입니다.

* **비즈니스 인큐베이팅 (From Dream to Business):**
SNS 광고 수익은 기초적인 단계일 뿐입니다. 우리는 꿈에서 얻은 창의적인 영감과 아이디어를 실제 사업 모델과 비즈니스로 연결합니다. 무의식의 통찰이 구체적인 제품과 서비스가 되어, 유저가 진정한 경제적 자유를 얻도록 돕습니다.

* **자발적 기여와 바이백 (Virtuous Cycle of Buy-back):**
이 시스템을 통해 사업적으로 성공하고 경제적 자유를 얻은 선구자들은 자발적으로 생태계에 기여하게 됩니다. 이렇게 조성된 생태계 후원금(Ecosystem Fund)은 다시 커뮤니티로 환원되어, 유저들이 열심히 채굴한 Dream Pts를 현실의 재화로 매입(Buy-back)하는 재원으로 사용됩니다.

결국 "꿈(채굴) → 사업화(성공) → 후원(펀드 조성) → 바이백(현금화)"이라는 완벽한 가치 순환 구조가 완성됩니다.
"""

# ==========================================
# 📚 [CONTENT PACK] - 상세 가이드 복원
# ==========================================
GUIDE_S1_FULL = """
**[실례 상황 설정]**
꿈 내용: "나는 낡고 허름한 내 옛날 초등학교 교실에 앉아 있다. 칠판 앞에 검은 옷을 입은 낯선 남자가 서 있는데, 나에게 오래된 시계를 건네주며 '이걸 고치라'고 말한다. 나는 고칠 줄 몰라 당황한다."

**1. 연상 (Associations): 개인적 의미의 방사형 연결**
꿈의 이미지를 사전적 정의(보편적 상징)로 해석하지 마십시오. 로버트 존슨은 '방사형 연상(Starburst)'을 강조합니다. 
* **잘못된 예 (꼬리 물기):** 시계 -> 시간 -> 바쁨 -> 회사 가기 싫다. (이것은 잡념입니다)
* **올바른 예 (방사형):** * 시계 -> 할아버지가 주신 선물
    * 시계 -> 째깍거리는 소리의 압박감
    * 시계 -> 멈춰버린 성장
    
**Tip:** 이미지를 중심에 두고 떠오르는 직관(A→1, A→2, A→3)을 있는 그대로 포착하십시오.
"""

GUIDE_S2_FULL = """
**2. 역학 (Dynamics): 내면의 인격들과 연결하기**
꿈의 모든 등장인물과 사물은 '나 자신의 분열된 자아'입니다. 역학 단계는 연상된 이미지들이 내면에서 어떤 '부분'을 담당하고 있는지 식별하는 과정입니다.

* **질문:** 꿈속의 '검은 옷의 남자'는 내 안의 어떤 부분인가?
    * "그는 나에게 무리한 요구를 하는 권위적인 목소리다."
    * "혹은, 내가 외면하고 있는 나의 엄격한 양심일 수도 있다."
    
**Tip:** 꿈속 인물에게 말을 걸어보십시오. "왜 나에게 이 시계를 주었습니까?"라고 묻고, 내면에서 들려오는 대답을 적으십시오.
"""

GUIDE_S3_FULL = """
**3. 해석 (Interpretations): 메시지의 통합**
연상과 역학을 종합하여 꿈이 보내는 '보상적(Compensatory) 메시지'를 읽어냅니다. 꿈은 의식이 한쪽으로 치우쳤을 때 균형을 맞추려 합니다.

* **통찰:** 나는 현실에서 너무 완벽해지려고 애쓰고 있다(시계를 고치려 함). 하지만 내면의 초등학교 교실(순수함)은 낡아 있다.
* **메시지:** "성과를 내기 위해 스스로를 닦달하지 말고, 잊고 있던 순수한 호기심과 동심을 먼저 회복하라."

**Tip:** 해석이 올바르다면, 몸에서 전율이 느껴지거나 '아하!' 하는 안도감이 듭니다. (Click)
"""

GUIDE_S4_FULL = """
**4. 의례 (Rituals): 구체적 행동으로의 육화 (가장 중요)**
빌더님, 이 단계가 로버트 존슨 꿈 작업의 핵심입니다. 깨달음(Insight)만으로는 부족합니다. 반드시 물리적인 행동(Action)이 따라야 무의식이 변화를 인지합니다.

* **작은 의례의 예:**
    * 낡은 초등학교 사진을 찾아 책상에 둔다.
    * 멈춘 시계를 서랍에서 꺼내, 그것을 '휴식'의 상징으로 삼고 10분간 멍하니 바라본다.
    * 나 자신에게 "고치지 않아도 괜찮아"라고 쓴 쪽지를 선물한다.

**Tip:** 거창할 필요 없습니다. 아주 작고 구체적인 행동 하나가 무의식에 강력한 신호를 보냅니다.
"""

# ==========================================
# 🌍 [LANGUAGE PACK]
# ==========================================
LANG = {
    "KO": {
        "title": "Dream-Pi : 무의식의 연금술",
        "manifesto_quote": '"현실의 결핍은 무의식의 풍요로 채워집니다.<br>이곳은 평범한 개인이 내면의 그림자를 대면하며 자신의 운명을 바꾸는 <b>퀀텀성장 실험실</b>입니다."<br><br>',
        "desc_1_title": "1. 꿈을 통한 자기 응시 (Self-Reflecting)",
        "desc_1_text": "우리는 밖을 보는 자가 아니라, 안을 들여다보는 자가 되기를 선택합니다. 분석심리학의 거장 <b>칼 융(Carl Jung)</b>과 로버트 A. 존슨이 제시한 <b>'4단계 꿈 작업(연상-역동-해석-의례)'</b>을 통해, 일상의 소음 뒤에 숨겨진 '그림자(Shadow)'를 발견합니다. 이것은 단순한 기록을 넘어, 내면의 미답지(未踏地)를 개척하는 고도의 자기계발 도구입니다.",
        "desc_2_title": "2. 성장의 시각화 : Dream Pts (Dream Points)",
        "desc_2_text": "매일 밤 무의식에서 길어 올린 통찰은 당신의 잠재력을 깨우는 연료가 됩니다. 이곳에서 쌓이는 Dream Pts는 당신이 얼마나 깊이 자신과 마주하고 각성했는지를 보여주는 <b>'성장의 증명'</b>입니다. 보이지 않는 내면의 변화를 가시적인 지표로 확인하며 한계를 돌파하는 퀀텀 점프를 경험하십시오.",
        "desc_3_title": "3. 가치의 선순환 : 자발적 후원과 바이백(Buy-back)",
        "desc_3_text": """나의 무의식이 정제되어 현실의 콘텐츠(인사이트)가 될 때, 그것은 타인에게 강력한 영감이 됩니다. 이 여정에 공감하고 삶의 변화를 경험한 선구자들이 자발적으로 씨앗(Fund)을 뿌리는 생태계를 지향합니다.<br><br>
조성된 후원금은 여러분이 쌓아온 Dream Pts의 가치를 인정하여 현실의 재화로 되돌려 드리는 '바이백(Buy-back)' 시스템의 근간이 됩니다. 마치 간절했던 꿈이 어느덧 눈앞의 현실이 되는 그날처럼 말입니다.<br><br>
<span style="color:#D4AF37; font-style:italic; font-weight:bold;">"오늘 당신의 무의식은 어떤 보물을 품고 있습니까? 그림자 속의 빛을 찾아내는 이 경이로운 실험에 당신을 초대합니다."</span>""",
        
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
        "dash_global": "총 채굴량 (Global Mined)",
        "dash_difficulty": "현재 채굴 난이도",
        "dash_my_asset": "내 보유 자산",
        "logout": "🔒 로그아웃",
        "left_title": "📓 무의식 원재료 (Raw Dream)",
        "load_dreams": "📂 내 지난 꿈 불러오기",
        "load_btn": "로드",
        "reset_btn": "🔄 새로 쓰기 (Reset)",
        "status_edit": "📝 수정 모드 (채굴 완료됨)",
        "status_new": "✨ 신규 작성 모드",
        "save_btn": "💾 꿈 내용 저장 (Save Dream)",
        "delete_btn": "🗑️ 삭제 (Delete)",
        "right_title": "🏛️ Dream-Pi 연금술 (4-Step)",
        "guide_s1": GUIDE_S1_FULL,
        "guide_s2": GUIDE_S2_FULL,
        "guide_s3": GUIDE_S3_FULL,
        "guide_s4": GUIDE_S4_FULL,
        "s1_label": "1단계: 연상 (Association)",
        "s2_label": "2단계: 역학 (Dynamics)",
        "s3_label": "3단계: 해석 (Interpretation)",
        "s4_label": "4단계: 의례 (Ritual)",
        "mint_btn": "⛏️ Dream-Pi 채굴 (Mint)",
        "update_btn": "💾 꿈 수정 보완", 
        "success_msg": "Mining Successful!",
        "mined_value": "Mined Value",
        "bonus_msg": "Halving Bonus",
        "ledger_title": "공개 장부 (Public Ledger)",
        "ledger_desc": "Active assets.",
        "burn_title": "자산 소각 (Asset Burn)",
        "burn_desc": "경고: 모든 자산이 영구적으로 삭제됩니다.",
        "burn_btn": "🔥 소각 실행",
        "burn_success": "소각 완료.",
        "admin_unlock": "Admin Unlock",
        "master_key_ph": "Master Key",
        "reg_dreamers": "Dreamers"
    }
}

# --- CSS: [v30.1] 모바일 아이콘 멸망 CSS + 가독성 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&family=Noto+Sans+KR:wght@400;700&display=swap');
    
    /* 1. 기본 배경 및 폰트 설정 */
    .stApp, .stApp > header, .stApp > footer, .stApp > main { 
        background-color: #050505 !important; 
        color: #FFFFFF !important; 
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    /* 2. [흰색 막대 제거] */
    .streamlit-expanderHeader {
        background-color: #111111 !important; 
        color: #D4AF37 !important; 
        border: 1px solid #333 !important;
        border-radius: 5px !important;
    }
    .streamlit-expanderHeader:hover {
        color: #FDB931 !important; 
        border-color: #D4AF37 !important;
    }
    .streamlit-expanderContent, 
    .streamlit-expanderContent p, 
    .streamlit-expanderContent li,
    .streamlit-expanderContent div {
        background-color: #0A0A0A !important;
        color: #E0E0E0 !important;
        opacity: 1 !important;
        font-weight: 400 !important;
    }

    /* 3. [대시보드] 숫자 */
    div[data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 1.8em !important;
        text-shadow: 0 0 10px rgba(255,255,255,0.3) !important;
    }
    div[data-testid="stMetricLabel"] { color: #FDB931 !important; font-weight: bold !important; }

    /* 4. [입력창] 커서 */
    .stTextArea textarea, .stTextInput input { 
        background-color: #0A0A0A !important; 
        color: #FFFFFF !important; 
        border: 1px solid #444 !important; 
        caret-color: #FFFFFF !important; 
    }
    
    /* 5. 🚀 [STEALTH MODE: NUKE CSS] 스트림릿 배지 완벽 박멸 🚀 */
    header, footer, 
    [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stStatusWidget"], [data-testid="stDecoration"], 
    [data-testid="manage-app-button"], [data-testid="stAppDeployButton"],
    .stDeployButton, #MainMenu {
        display: none !important; 
        visibility: hidden !important; 
        opacity: 0 !important; 
        pointer-events: none !important;
        z-index: -9999 !important;
        height: 0 !important;
        width: 0 !important;
    }
    
    [class^="viewerBadge_"], [class*="viewerBadge_"], 
    .viewerBadge_container__1QSob, .styles_viewerBadge__1yB5_, 
    .viewerBadge_link__1S137, .viewerBadge_text__1JaDK,
    div[class*="st-emotion-cache-1"] > button[title="Manage app"],
    div[class*="st-emotion-cache-1"] > button[kind="header"] {
        display: none !important; 
        visibility: hidden !important; 
        opacity: 0 !important; 
        pointer-events: none !important;
        position: absolute !important;
        left: -9999px !important;
        top: -9999px !important;
        z-index: -9999 !important;
    }
    
    /* 6. 타이틀 */
    .responsive-title {
        font-size: clamp(24px, 5vw, 45px) !important;
        font-weight: 900 !important;
        color: #D4AF37 !important;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
        line-height: 1.3 !important;
        font-family: 'Cinzel', serif;
    }

    /* 7. 버튼 스타일 */
    button { 
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; 
        border: none !important; opacity: 1 !important; 
        color: #000 !important;
        padding: 0.6rem 1.2rem !important; border-radius: 0.5rem !important; 
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3) !important;
    }
    button:hover { transform: scale(1.03); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5) !important; }
    button p, button div, button span { color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important; }

    /* 로드 버튼 리스트용 정렬 버튼 */
    .load-btn-wide button {
        text-align: left !important;
        padding-left: 15px !important;
        font-weight: normal !important;
        background: #1A1A1A !important;
        color: #D4AF37 !important;
        border: 1px solid #333 !important;
        box-shadow: none !important;
        width: 100% !important;
    }
    .load-btn-wide button:hover {
        background: #222 !important;
        border: 1px solid #D4AF37 !important;
    }

    /* 8. [GALAXY THEME] */
    .galaxy-box {
        background: linear-gradient(135deg, #1a0b2e 0%, #2d1b4e 50%, #000000 100%) !important;
        border: 2px solid #D4AF37 !important;
        border-radius: 15px !important;
        padding: 30px !important;
        text-align: center !important;
        box-shadow: 0 0 30px rgba(138, 43, 226, 0.3), inset 0 0 20px rgba(212, 175, 55, 0.1) !important;
        margin-top: 20px !important;
    }
    .galaxy-title {
        font-family: 'Cinzel', serif; color: #FDB931 !important; font-size: 2.5em !important; font-weight: bold !important;
        text-shadow: 0 0 10px rgba(253, 185, 49, 0.5);
    }
    .galaxy-score {
        font-size: 3.5em !important; font-weight: 900 !important;
        background: -webkit-linear-gradient(#fff, #D4AF37); -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 20px 0 !important;
    }
    
    /* 9. [FIXED SCORE BOX] */
    .fixed-score-box {
        background-color: #111111;
        border: 1px solid #D4AF37;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 15px;
    }
    .fixed-score-title { color: #888; font-size: 0.9em; margin-bottom: 5px; }
    .fixed-score-val { color: #D4AF37; font-size: 1.5em; font-weight: bold; }
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
except: st.error("DB Connection Error: secrets.toml을 확인하세요.")

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
                        clean_score = score_text.replace("Dream Pts", "").replace("Pts", "").replace(",", "").strip()
                        today_total += int(clean_score)
                    except: pass
        return today_total
    except: return 0

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
                        clean_score = score_text.replace("Dream Pts", "").replace("Pts", "").replace(",", "").strip()
                        score = int(clean_score)
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
                        clean_score = score_text.replace("Dream Pts", "").replace("Pts", "").replace(",", "").strip()
                        score = int(clean_score)
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

def calculate_mining_score(context, s1, s2, s3, s4, multiplier, is_early):
    base_score = len(context) * 2
    quality_bonus = 0
    keywords = {
        "s2": ["내면", "목소리", "자아", "성격", "누구", "왜"],
        "s3": ["메시지", "통찰", "균형", "보상", "깨달음", "의미"],
        "s4": ["행동", "실천", "하기", "만들기", "가기", "쓰기"]
    }
    if len(s1) > 20: quality_bonus += 100
    if len(s2) > 30: quality_bonus += 150
    if any(k in s2 for k in keywords["s2"]): quality_bonus += 50
    if len(s3) > 30: quality_bonus += 150
    if any(k in s3 for k in keywords["s3"]): quality_bonus += 50
    if len(s4) > 20: quality_bonus += 200
    if any(k in s4 for k in keywords["s4"]): quality_bonus += 100
    
    if len(context) < 10 or len(s1) < 5: return 0

    total_raw = base_score + quality_bonus
    time_bonus = 1.5 if is_early else 1.0
    final_score = int(total_raw * multiplier * time_bonus)
    return final_score

# ==========================================
# 🚪 1차 관문: Manifesto
# ==========================================
if not st.session_state.access_granted:
    st.session_state.language = "KO" 
    T = LANG[st.session_state.language]
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='responsive-title'>{T['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote-box'>{T['manifesto_quote']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"""<div class='defi-desc-box'>
    <div class='defi-desc-text'>
        <p><span class='highlight-bold'>{T['desc_1_title']}</span><br>
        {T['desc_1_text']}</p>
        <p><span class='highlight-bold'>{T['desc_2_title']}</span><br>
        {T['desc_2_text']}</p>
        <p><span class='highlight-bold'>{T['desc_3_title']}</span><br>
        {T['desc_3_text']}</p>
    </div>
</div>""", unsafe_allow_html=True)
        
        with st.expander("📜 Dream-Pi White Paper (백서 읽기)"):
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

my_assets, my_mining_count, global_supply, mining_multiplier, current_era = get_global_status(st.session_state.user_id)
supply_progress = min(1.0, global_supply / MAX_SUPPLY)

today_mined = get_today_mined_count(st.session_state.user_id)
daily_remaining = max(0, DAILY_CAP - today_mined)
daily_progress = min(1.0, today_mined / DAILY_CAP)

c_header_1, c_header_2 = st.columns([7, 3])
with c_header_1:
    st.markdown(f"### 🪙 {T['dash_global']} (Era: {current_era + 1})")
with c_header_2:
    st.markdown(f"<div class='dreamer-count-header'>✨ Dreamers: {user_count:,}</div>", unsafe_allow_html=True)

st.progress(supply_progress)
c_d1, c_d2, c_d3, c_d4 = st.columns(4)
with c_d1: st.metric(T['dash_global'], f"{global_supply:,} / {MAX_SUPPLY:,}", delta=f"{supply_progress*100:.2f}%")
with c_d2: st.metric(T['dash_difficulty'], f"Reward x{mining_multiplier}", delta="반감기 적용 중" if current_era > 0 else "초기 채굴 단계", delta_color="inverse")
with c_d3: st.metric(T['dash_my_asset'], f"{my_assets:,} Dream Pts", delta=f"{my_mining_count} blocks")
with c_d4: 
    if st.button(T['logout']):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()

st.markdown("---")
st.markdown(f"**⚡ 일일 채굴 에너지 (Daily Energy)** ({today_mined:,} / {DAILY_CAP:,} Pts)")
st.progress(daily_progress)
if daily_remaining <= 0:
    st.warning("🌙 오늘은 더 이상 채굴할 수 없습니다. 내일 다시 도전하세요!")

# 👑 [ADMIN PANEL]
if st.session_state.user_id == ADMIN_USER:
    st.markdown("---")
    st.markdown(f"#### 👑 Administrator Panel (ID: {st.session_state.user_id})")

    if not st.session_state.is_admin_unlocked:
        with st.form("admin_unlock_form"):
            master_input = st.text_input(T['master_key_ph'], type="password")
            if st.form_submit_button("Unlock Admin Mode"):
                if master_input == MASTER_KEY:
                    st.session_state.is_admin_unlocked = True
                    st.rerun()
                else: st.error("Access Denied")
    else:
        ad_c1, ad_c2 = st.columns(2)
        with ad_c1:
            st.info(f"📊 {T['ledger_title']}")
            if st.button("🔄 장부 새로고침"): st.rerun()
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
        if st.button("↩️ 소각 취소 및 자산 복구"):
            supabase.table("dreams").update({"is_burned": False}).eq("user_id", st.session_state.user_id).execute()
            st.success("✅ 자산이 성공적으로 복구되었습니다!")
            time.sleep(2)
            st.rerun()

st.markdown("---")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown(f"### {T['left_title']}")
    with st.expander(T['load_dreams'], expanded=False):
        
        search_mode = st.radio("검색 방식", ["최근 10개 보기", "특정 날짜 검색"], horizontal=True, label_visibility="collapsed")
        
        try:
            if search_mode == "특정 날짜 검색":
                target_date = st.date_input("불러올 꿈의 날짜를 선택하세요", value=datetime.date.today())
                
                start_dt = KST.localize(datetime.datetime.combine(target_date, datetime.time.min)).astimezone(pytz.UTC).isoformat()
                end_dt = KST.localize(datetime.datetime.combine(target_date, datetime.time.max)).astimezone(pytz.UTC).isoformat()
                
                res = supabase.table("dreams").select("*").eq("user_id", st.session_state.user_id).gte("created_at", start_dt).lte("created_at", end_dt).order("created_at", desc=True).execute()
            else:
                res = supabase.table("dreams").select("*").eq("user_id", st.session_state.user_id).order("created_at", desc=True).limit(10).execute()
            
            if res.data:
                st.markdown("<div class='load-btn-wide'>", unsafe_allow_html=True)
                for d in res.data:
                    korean_time = datetime.datetime.fromisoformat(d['created_at'].replace("Z", "+00:00")).astimezone(KST)
                    display_date = korean_time.strftime("%Y-%m-%d")
                    
                    dream_text = d.get('context', '').replace('\n', ' ')
                    btn_label = f"📂 {display_date} | {dream_text[:20]}..."
                    if st.button(btn_label, key=f"L_{d['id']}", use_container_width=True):
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
                st.markdown("</div>", unsafe_allow_html=True)
            else: 
                if search_mode == "특정 날짜 검색":
                    st.info(f"{target_date} 에 기록된 꿈이 없습니다.")
                else:
                    st.info("기록이 없습니다.")
        except: pass
    
    if st.button(T['reset_btn']):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = T['status_edit'] if st.session_state.is_minted else T['status_new']
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
                st.toast("저장되었습니다!")
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
        st.markdown("#### 🌞 새벽 채굴 모드 (x1.5 가중치)")
    else:
        st.markdown("#### ☕ 일반 채굴 모드 (x1.0)")
    
    with st.form("mint_form"):
        with st.expander(f"💡 {T['s1_label']} (가이드 보기)"):
            st.markdown(T['guide_s1'])
        st.text_area("1. 연상 (떠오르는 이미지들)", key="s1_val", height=120, label_visibility="collapsed")

        with st.expander(f"💡 {T['s2_label']} (가이드 보기)"):
            st.markdown(T['guide_s2'])
        st.text_area("2. 역학 (내면 인격과의 대화)", key="s2_val", height=120, label_visibility="collapsed")

        with st.expander(f"💡 {T['s3_label']} (가이드 보기)"):
            st.markdown(T['guide_s3'])
        st.text_area("3. 해석 (메시지 발견)", key="s3_val", height=150, label_visibility="collapsed")

        with st.expander(f"💡 {T['s4_label']} (가이드 보기)"):
            st.markdown(T['guide_s4'])
        
        st.text_area("4. 의례 (구체적 행동 다짐)", key="s4_val", height=100, label_visibility="collapsed")
        
        if st.session_state.is_minted and st.session_state.existing_value:
             st.markdown(f"""
             <div class="fixed-score-box">
                <div class="fixed-score-title">🏆 최초 획득 가치 (고정됨)</div>
                <div class="fixed-score-val">{st.session_state.existing_value}</div>
             </div>
             """, unsafe_allow_html=True)
        
        final_btn = T['update_btn'] if st.session_state.is_minted else T['mint_btn']
        
        if st.form_submit_button(final_btn):
            if not st.session_state.current_dream_id:
                st.error("⚠️ 왼쪽의 [꿈 내용 저장] 버튼을 먼저 눌러 내용을 확정해주세요!")
            else:
                errors = []
                if not st.session_state.dream_context: errors.append("꿈 내용")
                if not st.session_state.s1_val: errors.append("1단계")
                if not st.session_state.s2_val: errors.append("2단계")
                if not st.session_state.s3_val: errors.append("3단계")
                if not st.session_state.s4_val: errors.append("4단계")
                
                if errors:
                    st.error(f"⚠️ 다음 내용이 비어있습니다: {', '.join(errors)}")
                else:
                    if st.session_state.is_minted:
                        supabase.table("dreams").update({
                            "symbol": st.session_state.s1_val, 
                            "block": st.session_state.s2_val, 
                            "analysis": st.session_state.s3_val,
                            "ritual_self": st.session_state.s4_val
                        }).eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                        st.toast("✅ 수정 보완 완료! (점수는 변하지 않습니다)")
                    else:
                        if daily_remaining <= 0:
                            st.error("🛑 오늘의 채굴 한도를 초과했습니다.")
                        else:
                            final_score = calculate_mining_score(
                                st.session_state.dream_context,
                                st.session_state.s1_val,
                                st.session_state.s2_val,
                                st.session_state.s3_val,
                                st.session_state.s4_val,
                                mining_multiplier,
                                is_early_bird
                            )
                            
                            if final_score == 0:
                                st.error("⚠️ 내용이 너무 짧거나 불충분하여 채굴에 실패했습니다.")
                            else:
                                final_score = min(final_score, daily_remaining)
                                new_val_str = f"{final_score:,} Pts"
                                
                                supabase.table("dreams").update({
                                    "symbol": st.session_state.s1_val, 
                                    "block": st.session_state.s2_val, 
                                    "analysis": st.session_state.s3_val,
                                    "ritual_self": st.session_state.s4_val, 
                                    "meaning": f"Value: {new_val_str}"
                                }).eq("id", st.session_state.current_dream_id).eq("user_id", st.session_state.user_id).execute()
                                
                                st.session_state.is_minted = True
                                st.session_state.existing_value = new_val_str
                                
                                st.balloons()
                                
                                msg = st.empty()
                                msg.markdown(f"""
                                <div class="galaxy-box">
                                    <div class="galaxy-title">DREAM MINED!</div>
                                    <div class="galaxy-score">+{final_score:,} Pts</div>
                                    <div class="galaxy-desc">The Alchemy of the Unconscious Complete</div>
                                </div>
                                """, unsafe_allow_html=True)
                                time.sleep(4) 
                                st.rerun()