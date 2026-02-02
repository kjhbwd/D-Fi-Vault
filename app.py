import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v12.6", page_icon="🏛️", layout="wide")

# 🔒 1차 관문: 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "korea2026"

# --- CSS: 디자인 (가독성 & Deep Dark & Tooltip Fix) ---
st.markdown("""
    <style>
    /* 1. 전체 테마 강제 적용 (Deep Black) */
    .stApp, .stApp > header, .stApp > footer, .stApp > main {
        background-color: #050505 !important; color: #FFFFFF !important;
    }
    
    /* 2. 버튼 스타일 (황금색) */
    button {
        background: linear-gradient(90deg, #D4AF37 0%, #FDB931 100%) !important;
        background-color: #D4AF37 !important; border: none !important; opacity: 1 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.5) !important; padding: 0.5rem 1rem !important; border-radius: 0.5rem !important;
    }
    button p, button div, button span {
        color: #000000 !important; font-weight: 900 !important; font-size: 1rem !important;
    }
    button:hover { background: #FFD700 !important; transform: scale(1.02); }
    
    /* 3. 입력창 및 텍스트 영역 스타일 */
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    
    /* 4. 라벨(제목) 색상 강제 지정 */
    label, .stMarkdown label, p {
        color: #E0E0E0 !important;
    }
    
    /* 5. 컨테이너 스타일 */
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    
    /* 6. [NEW] 툴팁(물음표) 가독성 패치 (검은 배경, 흰 글씨 강제) */
    div[data-baseweb="tooltip"], div[data-baseweb="popover"] {
        background-color: #333333 !important;
        color: #FFFFFF !important;
    }
    div[data-baseweb="tooltip"] div, div[data-baseweb="popover"] div {
        color: #FFFFFF !important; /* 내부 텍스트 흰색 강제 */
    }
    
    /* 7. 헤더/푸터 및 경고 숨김 */
    header, footer { visibility: hidden !important; }
    .stAlert { display: none; } 
    
    /* 🏛️ Manifesto Style */
    .main-title {
        font-size: 2.5em; font-weight: 900; color: #D4AF37 !important; text-align: center; margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); font-family: 'Malgun Gothic', sans-serif;
    }
    .quote-box {
        background-color: #1A1A1A !important; border-left: 4px solid #D4AF37 !important; padding: 20px !important; margin: 20px 0 !important;
        color: #E0E0E0 !important; font-style: italic; font-size: 1.2em; border-radius: 5px;
    }
    .defi-desc-box {
        background-color: #111111 !important; padding: 30px !important; border-radius: 15px !important; border: 1px solid #333 !important;
        margin-top: 30px; margin-bottom: 30px;
    }
    .defi-desc-text { color: #BBBBBB !important; font-size: 1.0em; line-height: 1.8; font-family: sans-serif; }
    .highlight-gold { color: #FDB931 !important; font-weight: bold; font-size: 1.2em; margin-bottom: 15px; display: block; }
    .highlight-bold { color: #FFFFFF !important; font-weight: bold; }
    .faint-hint { color: #888888 !important; font-size: 0.9em; margin-top: 25px; font-style: italic; text-align: center; border-top: 1px solid #333; padding-top: 20px;}
    </style>
    """, unsafe_allow_html=True)

# [SESSION STATE & CONNECTION]
if 'access_granted' not in st.session_state: st.session_state.access_granted = False
if 'user_id' not in st.session_state: st.session_state.user_id = None
if 'auth_step' not in st.session_state: st.session_state.auth_step = "check_id"
if 'temp_username' not in st.session_state: st.session_state.temp_username = ""

for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
    if key not in st.session_state: st.session_state[key] = "" if key != 'current_dream_id' else None
if 'interpretation_ready' not in st.session_state: st.session_state.interpretation_ready = False
if 'is_minted' not in st.session_state: st.session_state.is_minted = False

try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except: st.error("DB 연결 오류")

# ==========================================
# 🧠 [CORE LOGIC] 문맥 반영 심층 해석 엔진
# ==========================================
def analyze_dream_engine_v2(context, symbol, dynamics):
    keywords = {
        "옷": "persona", "의복": "persona", "체육복": "persona", "유니폼": "persona", "가면": "persona",
        "쫓김": "shadow", "도망": "shadow", "괴물": "shadow", "귀신": "shadow", "공격": "shadow",
        "돈": "wealth", "황금": "wealth", "보석": "wealth", "부자": "wealth", "주식": "wealth",
        "집": "self", "방": "self", "건물": "self", "이사": "self", "청소": "self",
        "물": "unconscious", "바다": "unconscious", "강": "unconscious", "수영": "unconscious",
        "날다": "transcendence", "하늘": "transcendence", "비행기": "transcendence", "추락": "transcendence",
        "죽음": "rebirth", "장례식": "rebirth", "시체": "rebirth", "살인": "rebirth", "불": "rebirth",
    }
    detected_type = "general"
    full_input = (symbol + " " + dynamics + " " + context).lower()
    for key, val in keywords.items():
        if key in full_input: detected_type = val; break

    ritual_options = {
        "persona": [
            f"오늘 하루, 평소 스타일과 정반대의 옷을 입고 거울 속 자신과 대화하기",
            f"옷장 정리를 하며 1년 이상 입지 않은 옷(낡은 페르소나) 한 벌 버리기",
            f"'{symbol}'의 이미지를 종이에 그리고, 그 위에 내가 원하는 새로운 나의 모습을 덧그리기"
        ],
        "shadow": [
            f"'{symbol}'에게 어울리는 귀여운 이름을 지어주고, 두려움이 들 때마다 그 이름을 불러주기",
            f"베개 밑에 칼(모형)이나 가위를 두고 자는 상상적 방어 의례 행하기",
            f"쫓기던 상황을 그림으로 그리고, 결말을 '내가 그 대상을 포옹하는 장면'으로 다시 그리기"
        ],
        "wealth": [
            f"지갑에 있는 모든 지폐를 꺼내어 액수를 소리 내어 세어보고 감사하다고 말하기",
            f"동전 하나를 깨끗이 닦아 '풍요의 씨앗'이라 명명하고 흙에 심거나 소중한 곳에 보관하기",
            f"작은 금액이라도 오늘 누군가를 위해 기부하거나 베풀기"
        ],
        "self": [
            f"내 방의 가구 배치나 소품 위치를 하나만 바꾸어 새로운 에너지 흐름 만들기",
            f"방이나 집의 가장 구석진 곳(무의식의 사각지대)을 청소하기",
            f"현관문을 닦으며 좋은 에너지가 들어오도록 환영하는 인사 건네기"
        ],
        "general": [
            f"'{symbol}' 단어를 종이에 적어 오늘 하루 주머니에 넣고 다니며 그 에너지를 느끼기",
            f"잠들기 전 물 한 잔을 마시며 '나는 꿈을 기억한다'고 세 번 암시하기",
            f"꿈 내용을 녹음기로 녹음해서 내 목소리로 다시 들어보기"
        ]
    }
    selected_ritual = random.choice(ritual_options.get(detected_type, ritual_options["general"]))

    interpretations = {
        "persona": {
            "jung": f"꿈속의 '{symbol}'은(는) 당신의 사회적 인격(Persona)을 대변합니다. 당신이 기록한 정체성의 변화나 갈등은, 현재 당신이 세상에 보여주는 모습과 내면의 진실 사이에 새로운 조율이 시작되었음을 의미합니다.",
            "johnson": f"우리는 때로 맞지 않는 옷을 입고 살아갑니다. 이 꿈은 당신에게 묻습니다. '지금 입고 있는 역할이 편안한가?' 낡은 역할을 벗어던질 용기가 필요한 시점입니다.",
            "ko": f"이것은 타인의 시선이 만들어낸 '나'입니다. 하지만 꿈은 이제 당신이 그 껍질을 깨고 나와도 안전하다고 말합니다. 당신의 본래 모습을 드러내십시오."
        },
        "shadow": {
            "jung": f"등장한 '{symbol}'은(는) 당신의 그림자(Shadow)입니다. 이것은 외부의 적이 아니라, 당신이 아직 인정하지 않은 당신 자신의 일부입니다. 그 강렬한 에너지는 통합을 기다리고 있습니다.",
            "johnson": f"도망치거나 싸우려 하지 마십시오. 꿈속의 추격이나 공포는 '나를 봐달라'는 무의식의 절규입니다. 그 에너지를 존중할 때 그것은 당신의 가장 큰 아군이 됩니다.",
            "ko": f"모든 등장인물은 당신의 분신입니다. '{symbol}'이 되어보십시오. 그리고 그가 왜 그렇게 화가 났거나 쫓아오는지 들어보십시오. 그곳에 답이 있습니다."
        },
        "wealth": {
            "jung": f"'{symbol}'은(는) 세속적 재물이 아니라, 당신 영혼의 고귀한 가치(Self)를 상징합니다. 무의식은 당신이 이미 내적으로 충만한 상태임을 보여주고 있습니다.",
            "johnson": f"이 풍요로움을 의심하지 말고 받아들이십시오. 내면의 에너지가 임계점을 넘어 현실의 창조적 결과물로 흘러나오려 하고 있습니다.",
            "ko": f"당신은 결핍되지 않았습니다. 이 꿈은 당신의 잠재력이 현실에서 구체적인 성과로 드러날 준비가 되었음을 확증하는 보증수표입니다."
        },
        "self": {
            "jung": f"'{symbol}'은(는) 당신의 마음의 구조 그 자체입니다. 꿈속 공간의 상태는 현재 당신 의식의 상태를 반영합니다. 확장이 일어나고 있거나, 재건축이 필요한 시점입니다.",
            "johnson": f"내면의 공간을 점검하십시오. 어수선했다면 정리가 필요하고, 새로운 방을 보았다면 당신의 새로운 재능이 발견된 것입니다.",
            "ko": f"꿈속의 그 장소에서 느꼈던 감정을 기억하십시오. 그 공간은 당신이 쉬어야 할 곳이거나, 용기 내어 들어가야 할 마음의 방입니다."
        },
        "general": {
            "jung": f"'{symbol}' 상징은 당신 무의식이 보낸 특별한 초대장입니다. 전체적인 꿈의 맥락을 볼 때, 이것은 당신이 현재 겪고 있는 상황에 대한 직관적인 해결책을 담고 있습니다.",
            "johnson": f"이 꿈을 머리로 해석하려 하기보다, 그 이미지 자체를 마음에 품으십시오. '{dynamics}'의 에너지가 당신의 삶을 올바른 방향으로 이끌 것입니다.",
            "ko": f"이 꿈은 온전히 당신의 이야기입니다. 꿈속의 상황을 현실의 비유로 바라보십시오. 당신은 지금 어디에 서 있습니까?"
        }
    }
    
    result = interpretations.get(detected_type, interpretations["general"])
    result['ritual'] = selected_ritual
    return result

# ==========================================
# 🚪 1차 관문: Manifesto
# ==========================================
if not st.session_state.access_granted:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-title'>Dream-Fi : 무의식의 연금술</div>", unsafe_allow_html=True)
        
        st.markdown("""<div class='quote-box'>
    "현실의 결핍은 무의식의 풍요로 채워진다.<br>
    이것은 평범한 개인이 자신의 운명을 바꾸는 <b>퀀텀 점프 실험실</b>입니다."
</div>""", unsafe_allow_html=True)
        
        st.markdown("""<div class='defi-desc-box'>
    <div class='defi-desc-text'>
        <span class='highlight-gold'>🪙 Dream Pts : 나의 퀀텀 에너지 지수</span>
        <p><span class='highlight-bold'>1. 성장의 시각화 (Visualizing Growth)</span><br>
        저는 생존을 고민하는 평범한 사람입니다. 하지만 매일 밤 <b>꿈(무의식)</b>을 채굴하여 제 잠재력을 깨우고 있습니다. 여기에 쌓이는 <b>Dream Pts</b>는 제가 얼마나 깊이 각성했는지를 보여주는 <b>성장의 증명</b>입니다.</p>
        <p><span class='highlight-bold'>2. 현실의 변화 (X-Factor)</span><br>
        이곳에서 제련된 통찰은 <b>X(트위터)</b>와 현실의 콘텐츠가 됩니다. 무의식의 영감이 어떻게 <b>노출수(Traffic)</b>와 <b>수익(Revenue)</b>으로 변환되는지 목격하십시오.</p>
        <div class='faint-hint'>
        "상상해 보십시오. 제가 퀀텀 점프에 성공하는 날, 이곳에 남겨진 당신의 <b>초기 채굴 기록(Genesis Data)</b>들이 어떤 가치(Value)로 치환될지... 그 가능성은 열어두겠습니다."
        </div>
    </div>
</div>""", unsafe_allow_html=True)
        
        with st.form("gate_form"):
            input_code = st.text_input("Entry Code", type="password", placeholder="입장 코드를 입력하세요")
            if st.form_submit_button("🗝️ 무의식 광산 입장하기"):
                if input_code == COMMUNITY_PASSWORD:
                    st.session_state.access_granted = True
                    st.toast("✅ 접속 승인. 환영합니다.")
                    time.sleep(0.5)
                    st.rerun()
                else: st.error("⛔ 유효하지 않은 코드입니다.")
    st.stop()

# ==========================================
# 🚪 2차 관문: Identity Check
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
                    else: st.error("비밀번호 불일치")
                if hint_btn:
                    res = supabase.table("users").select("hint").eq("username", st.session_state.temp_username).execute()
                    if res.data and res.data[0]['hint']: st.warning(f"💡 힌트: {res.data[0]['hint']}")
                    else: st.warning("힌트가 없습니다.")
            if st.button("⬅️ 뒤로 가기"):
                st.session_state.auth_step = "check_id"
                st.rerun()
        elif st.session_state.auth_step == "register":
            st.success(f"✨ **{st.session_state.temp_username}**님은 처음 오셨군요! 전용 금고를 생성합니다.")
            with st.form("register_form"):
                new_pin = st.text_input("설정할 비밀번호 (4자리)", type="password", max_chars=4)
                hint = st.text_input("비밀번호 힌트 (선택사항)", placeholder="예: 내 생일")
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
# 🏛️ MAIN APP: WORKSPACE
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
with col_dash2: st.metric(label="Today's Mining", value=f"{daily_sum:,} Dream Pts", delta=f"{daily_count}건")
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
                            
                            # 데이터 로드 및 위젯 키 동기화
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
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
                            st.session_state.interpretation_ready = True if meaning_text else False
                            st.session_state.is_minted = True if meaning_text else False
                            
                            st.rerun()
                            
                    with c_r: st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
            else: st.info("기록 없음")
        except: pass
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        for k in ['s1_key', 's2_key', 's3_key']:
            if k in st.session_state: del st.session_state[k]
        st.session_state.interpretation_ready = False
        st.session_state.is_minted = False
        st.rerun()

    with st.form("left_form"):
        status = "📝 수정 모드" if st.session_state.current_dream_id else "✨ 신규 작성 모드"
        st.caption(status)
        dream_raw = st.text_area("꿈 내용 입력", value=st.session_state.dream_context, height=450, help="여기에 기억나는 꿈 내용을 최대한 자세히 적으세요.")
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
    st.markdown("### 🏛️ D-Fi 연금술")
    
    if 's1_key' not in st.session_state: st.session_state.s1_key = st.session_state.s1_val
    if 's2_key' not in st.session_state: st.session_state.s2_key = st.session_state.s2_val

    # 🟢 [수정 완료] Stage 1 가이드 전면 교체 및 툴팁
    s1_help_text = """먼저 꿈을 훑어 보면서 꿈 이미지 각각에 대해 연상되는 것들을 전부 적어본다.
꿈에 사람이나 사물 상황, 색, 소리에 대화 등이 등장했을 것이다.

이 하나하나를 이미지로 들여다볼 필요가 있다.
기본 기법은 이렇다.
우선 꿈에 처음 등장한 이미지를 적고 스스로 자문한다.

'이 이미지를 보고 어떤 느낌이 들지?'
'보고 있으면 어떤 말이나 생각이 떠오르지?'

꿈에 등장하는 이미지에서 불쑥 떠오르는 단어나 생각, 심상, 감정, 기억도 연상이다.
이 이미지와 자동적으로 연결 짓게 되는 그런 것도 연상이다."""

    st.text_area("🚀 Stage 1: 연상 (Association)", height=70, key="s1_key", 
                 placeholder="핵심 단어 입력 (예: 쫓김, 돈, 옷)", 
                 help=s1_help_text)
    
    st.text_area("🔍 Stage 2: 역학 (Dynamics)", height=70, key="s2_key", 
                 placeholder="어떤 기분이나 상황이었나요?",
                 help="그 상징이 내 꿈에서 어떤 행동을 했나요? 나는 어떤 감정을 느꼈나요? (예: 무서워서 도망침, 따뜻해서 안아줌)")
    
    if st.button("▼ 마스터 해석 가동 (ENTER)"):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        
        if s1_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            
            result = analyze_dream_engine_v2(st.session_state.dream_context, s1_input, s2_input)
            
            analysis_text = f"""[🏛️ D-Fi 심층 분석 결과]

1. 👤 칼 융 (C.G. Jung):
"{result['jung']}"

2. ⚖️ 로버트 A. 존슨 (Robert A. Johnson):
"{result['johnson']}"

3. 🕯️ 고혜경 박사 (Projective Work):
"{result['ko']}"
"""
            st.session_state['s3_key'] = analysis_text 
            st.session_state.s3_val = analysis_text
            st.session_state.s4_val = result['ritual']
            st.session_state.interpretation_ready = True
            st.toast("✨ 심층 분석 완료!")
            time.sleep(0.1) 
            st.rerun()
        else: st.warning("Stage 1(상징)을 입력해야 해석할 수 있습니다.")

    if 's3_key' not in st.session_state: st.session_state.s3_key = st.session_state.s3_val
    st.text_area("🏛️ Stage 3: 해석 (Interpretation)", height=350, disabled=False, key="s3_key",
                 help="3인의 전문가 관점으로 분석된 무의식의 메시지입니다.")

    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: 의례 (Ritual)", help="꿈의 에너지를 현실로 가져오는 구체적인 행동입니다. 이 행동을 함으로써 무의식은 변화를 시작합니다.")
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 지난 자산 가치: {st.session_state.existing_value}")
        
        s4 = st.text_input("구체적 실천 행동 (자동 추천됨, 수정 가능)", value=st.session_state.s4_val)
        
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*10)
                new_val_str = f"Value: {token_val} Dream Pts"
                
                payload = {
                    "symbol": st.session_state.s1_val, 
                    "block": st.session_state.s2_val, 
                    "ritual_self": s4, 
                    "meaning": new_val_str,
                    "analysis": st.session_state.s3_val
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
                st.success(f"✅ 의례(Ritual) 등록 완료!\n\n💰 {new_val_str}")
                time.sleep(3)
                st.rerun()
