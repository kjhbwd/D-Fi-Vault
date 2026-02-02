import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random
import pandas as pd

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v14.0: Alchemy", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

# 🔒 1. 커뮤니티 공통 암호 및 관리자 설정
COMMUNITY_PASSWORD = "2026"
ADMIN_USER = "김지호bwd"
MASTER_KEY = "1234"

# 🪙 [TOKENOMICS]
MAX_SUPPLY = 21000000
HALVING_STEP = 2100000

# 🟢 [CORE] 세션 상태 초기화
if 'language' not in st.session_state: st.session_state.language = "KO"
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'auth_step' not in st.session_state: st.session_state.auth_step = "check_id"
if 'temp_username' not in st.session_state: st.session_state.temp_username = ""
if 'is_admin_unlocked' not in st.session_state: st.session_state.is_admin_unlocked = False

# 입력을 위한 세션 상태
for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
    if key not in st.session_state: st.session_state[key] = "" if key != 'current_dream_id' else None
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

# ==========================================
# 🌐 [LANGUAGE PACK] - 실례 가이드 통합
# ==========================================
LANG = {
    "KO": {
        "title": "D-Fi : 무의식의 연금술 (Master)",
        "manifesto_quote": '"현실의 결핍은 무의식의 풍요로 채워진다.<br>이것은 빡빡한 현실을 걷는 사업가가 무의식의 광맥을 찾아 떠나는 <b>생존 실험</b>입니다."',
        "s1_label": "🚀 Stage 1: 연상 (Association)",
        "s1_help": """[가이드: 개인적 의미의 방사형 연결]
이미지(A)를 중심에 두고 떠오르는 직관을 포착하세요.
실례:
- 초등학교 교실: 배움, 미성숙함, 규율, 답답함.
- 검은 옷의 남자: 권위적임, 무서움, 그림자(Shadow).
- 오래된 시계: 시간의 압박, 멈춰 있음, 수명이 다함.""",
        "s2_label": "🔍 Stage 2: 역학 (Dynamics)",
        "s2_help": """[가이드: 내면의 인격들과 연결하기]
"내 안의 어떤 부분이 이 이미지와 닮았는가?"를 자문하세요.
실례:
- 초등학교 교실 → 나의 학습 태도: 과거의 방식에 갇혀 있음.
- 검은 옷의 남자 → 내면의 감독관: 나를 압박하는 초자아.
- 고장 난 시계 → 나의 생체 리듬: 에너지가 고갈되어 멈춤.""",
        "s3_label": "🏛️ Stage 3: 해석 (Interpretation)",
        "s3_help": """[가이드: 메시지의 통합]
꿈이 보내는 보상적 메시지를 읽어냅니다.
실례:
- 분석: 과거의 낡은 방식으로 문제를 해결하려 함. 내면의 권위자는 '내면의 질서' 회복을 명령함.
- 결론: 멈춰버린 리듬을 수리하고 전문가적 태도를 갖춰야 한다는 신호.""",
        "s4_label": "💎 Stage 4: 의례 (Ritual)",
        "s4_help": """[가이드: 구체적 행동으로의 육화]
깨달음을 물리적 행동으로 옮기세요. 상징적 의미가 명확해야 합니다.
좋은 예:
- 실제로 멈춘 시계의 배터리를 교체함.
- 시간 계획표를 짜서 지갑에 넣음.
- 전문 서적을 한 권 사서 읽음.""",
        "mint_btn": "💎 최종 자산 발행 (Mint Token)",
        "update_btn": "🏛️ 자산 정보 업데이트",
        "login_placeholder": "입장 코드를 입력하세요 (2026)",
        "id_check_desc": "본인의 닉네임과 비번을 설정하세요. 본인의 기록은 본인만 볼 수 있습니다.",
        "success_msg": "🎉 채굴 성공! 성장의 증명이 완료되었습니다.",
        "bonus_msg": "현재 반감기 보너스",
        "dash_global": "Global Mined",
        "dash_difficulty": "Mining Difficulty",
        "dash_my_asset": "My Active Assets",
        "logout": "🔒 로그아웃",
        "reg_dreamers": "Registered Dreamers"
    },
    "EN": {
        "title": "D-Fi : Alchemy of Unconscious",
        "manifesto_quote": '"Lack in reality is filled by abundance in unconscious.<br>A survival experiment of a builder mining the <b>Vein of Gold</b>."',
        "s1_label": "🚀 Stage 1: Association",
        "s1_help": """[Guide: Radial Association]
Focus on the image(A) and capture intuitive feelings.
Example:
- School: Learning, Immaturity, Discipline.
- Man in Black: Authority, Fear, Shadow.
- Old Clock: Pressure of time, Stopped, Lifespan.""",
        "s2_label": "🔍 Stage 2: Dynamics",
        "s2_help": """[Guide: Connecting Inner Personas]
Ask: "Which part of me resembles this image?"
Example:
- School → My learning attitude: Stuck in old ways.
- Man in Black → Inner supervisor: Superego pressing me.
- Broken Clock → My bio-rhythm: Energy depleted.""",
        "s3_label": "🏛️ Stage 3: Interpretation",
        "s3_help": """[Guide: Message Integration]
Read the compensatory message of the dream.
Example:
- Analysis: Trying to solve problems with old ways. Inner authority orders to restore 'Inner Order'.
- Conclusion: Signal to repair the stopped rhythm and adopt a professional attitude.""",
        "s4_label": "💎 Stage 4: Ritual",
        "s4_help": """[Guide: Physical Incarnation]
Move insight into physical action. 
Good Examples:
- Replacing the battery of a stopped clock.
- Writing a schedule and putting it in your wallet.
- Buying a professional book.""",
        "mint_btn": "💎 Mint Token",
        "update_btn": "🏛️ Update Asset",
        "login_placeholder": "Enter Code (2026)",
        "id_check_desc": "Set your ID/PW. Only you can access your records.",
        "success_msg": "🎉 Minting Successful! Proof of Growth completed.",
        "bonus_msg": "Halving Bonus",
        "dash_global": "Global Mined",
        "dash_difficulty": "Difficulty",
        "dash_my_asset": "My Assets",
        "logout": "🔒 Logout",
        "reg_dreamers": "Registered Dreamers"
    }
}

# --- CSS: Gold & Black Theme ---
st.markdown("""
    <style>
    .stApp { background-color: #050505 !important; color: #FFFFFF !important; }
    [data-testid="stSidebar"] { background-color: #111111 !important; border-right: 1px solid #333 !important; }
    button { background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important; border-radius: 8px !important; }
    button p { color: #000 !important; font-weight: 900 !important; }
    .main-title { font-size: 2.5em; font-weight: 900; color: #D4AF37; text-align: center; }
    .quote-box { background-color: #1A1A1A; border-left: 4px solid #D4AF37; padding: 20px; font-style: italic; }
    .stMetricValue { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

# Supabase 초기화
try:
    url, key = st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("Database connection failed.")

# --- 메인 로직 ---
def get_user_count():
    try: return supabase.table("users").select("username", count="exact").execute().count
    except: return 0

def get_global_status(current_user):
    try:
        res = supabase.table("dreams").select("meaning, user_id, is_burned").execute()
        my_total, my_count, global_mined = 0, 0, 0
        if res.data:
            for d in res.data:
                score = 0
                if d.get('meaning') and "Value: " in d['meaning']:
                    try: score = int(d['meaning'].split("Value: ")[1].split(" ")[0].replace(",", ""))
                    except: pass
                global_mined += score
                if d['user_id'] == current_user and not d.get('is_burned'):
                    my_total += score
                    my_count += 1
        era = global_mined // HALVING_STEP
        return my_total, my_count, global_mined, 1/(2**era), era
    except: return 0, 0, 0, 1, 0

# --- 1차 관문 (암호 입장) ---
if not st.session_state.access_granted:
    T = LANG[st.session_state.language]
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"<div class='main-title'>{T['title']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='quote-box'>{T['manifesto_quote']}</div>", unsafe_allow_html=True)
        with st.form("gate"):
            code = st.text_input("Entry Code", type="password", placeholder=T['login_placeholder'])
            if st.form_submit_button("ENTER"):
                if code == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.rerun()
        st.markdown(f"<p style='text-align:center;'>{T['reg_dreamers']}: {get_user_count()}</p>", unsafe_allow_html=True)
    st.stop()

# --- 2차 관문 (ID/PW 로그인) ---
if not st.session_state.user_id:
    T = LANG[st.session_state.language]
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.write(f"### {T['id_check_desc']}")
        # 로그인 및 가입 로직 (기존 코드 유지)
        input_id = st.text_input("Nickname (ID)")
        if st.button("Next"):
            st.session_state.temp_username = input_id
            res = supabase.table("users").select("*").eq("username", input_id).execute()
            st.session_state.auth_step = "login" if res.data else "register"
            st.rerun()
        
        if st.session_state.auth_step == "login":
            pin = st.text_input("PIN (4-digits)", type="password")
            if st.button("Open Vault"):
                res = supabase.table("users").select("*").eq("username", st.session_state.temp_username).eq("pin", pin).execute()
                if res.data: 
                    st.session_state.user_id = st.session_state.temp_username
                    st.rerun()
        elif st.session_state.auth_step == "register":
            new_pin = st.text_input("Set PIN (4-digits)", type="password")
            if st.button("Create Account"):
                supabase.table("users").insert({"username": st.session_state.temp_username, "pin": new_pin}).execute()
                st.session_state.user_id = st.session_state.temp_username
                st.rerun()
    st.stop()

# --- 메인 대시보드 및 4단계 채굴 로직 ---
T = LANG[st.session_state.language]
my_assets, my_mining_count, global_supply, multiplier, era = get_global_status(st.session_state.user_id)

st.markdown(f"## 🏛️ D-Fi Vault (Era: {era+1})")
c1, c2, c3, c4 = st.columns(4)
c1.metric(T['dash_global'], f"{global_supply:,}")
c2.metric(T['dash_difficulty'], f"x{multiplier}")
c3.metric(T['dash_my_asset'], f"{my_assets:,}")
if c4.button(T['logout']):
    for k in list(st.session_state.keys()): del st.session_state[k]
    st.rerun()

st.divider()

col_l, col_r = st.columns(2)

with col_l:
    st.markdown("### 📓 무의식 원재료 (Raw Dream)")
    dream_raw = st.text_area("당신의 꿈을 상세히 기록하세요.", height=500, value=st.session_state.dream_context)
    if st.button("💾 임시 저장"):
        st.session_state.dream_context = dream_raw
        st.toast("Saved!")

with col_r:
    st.markdown("### ⚒️ 4단계 채굴 프로세스")
    
    # 1단계
    s1 = st.text_area(T['s1_label'], help=T['s1_help'], key="s1_box")
    # 2단계
    s2 = st.text_area(T['s2_label'], help=T['s2_help'], key="s2_box")
    # 3단계
    s3 = st.text_area(T['s3_label'], help=T['s3_help'], height=200, key="s3_box")
    
    # 4단계 및 채굴 버튼
    with st.form("mint_form"):
        st.markdown(f"#### {T['s4_label']}", help=T['s4_help'])
        s4 = st.text_input("오늘의 구체적인 의례(Action)를 입력하세요.")
        
        if st.form_submit_button(T['mint_btn']):
            if all([dream_raw, s1, s2, s3, s4]):
                # 보상 계산: 글자수(정성) + 기본보상 * 반감기
                score = int((1000 + len(dream_raw + s1 + s2 + s3 + s4) * 5) * multiplier)
                val_str = f"Value: {score:,} Dream Pts"
                
                payload = {
                    "user_id": st.session_state.user_id,
                    "context": dream_raw,
                    "symbol": s1,
                    "block": s2,
                    "analysis": s3,
                    "ritual_self": s4,
                    "meaning": val_str
                }
                supabase.table("dreams").insert(payload).execute()
                
                st.balloons()
                st.success(f"{T['success_msg']} +{score:,} Pts")
                time.sleep(2)
                st.rerun()
            else:
                st.error("모든 단계를 정성껏 작성해야 채굴이 인정됩니다.")

# 관리자 모드 (생략 가능하나 유지)
if st.session_state.user_id == ADMIN_USER:
    st.divider()
    if st.checkbox("Admin Unlock"):
        key = st.text_input("Master Key", type="password")
        if key == MASTER_KEY:
            st.write("📊 Ledger & Burn Mode Active")
            # 관리자 전용 기능 (Ledger 출력 등)
