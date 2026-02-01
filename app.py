import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random # 풍요의 해석 로직을 위한 랜덤 모듈

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v11.5", page_icon="🏛️", layout="wide")

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
    
    /* 3. 입력창 및 텍스트 스타일 */
    .stTextArea textarea, .stTextInput input {
        background-color: #0A0A0A !important; color: #FFFFFF !important; border: 1px solid #666666 !important;
    }
    div[data-testid="column"] {
        background-color: #111111; border: 1px solid #333333; border-radius: 8px; padding: 20px;
    }
    header, footer { visibility: hidden !important; }
    h1, h2, h3, h4, p, label, .stMarkdown, .stMetricValue, .stMetricLabel { color: #FFFFFF !important; }
    
    /* 🏛️ Manifesto Style */
    .main-title {
        font-size: 2.5em; font-weight: 900; color: #D4AF37; text-align: center; margin-bottom: 20px;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.3); font-family: 'Malgun Gothic', sans-serif;
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
for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
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
# 🧠 [CORE LOGIC] 풍요의 해석 엔진 (Abundance Engine)
# ==========================================
def analyze_dream_engine(symbol, dynamics):
    """
    단순한 입력값을 받아서 3가지 관점의 깊이 있는 해석과 실천 의례를 생성합니다.
    """
    # 키워드 감지 로직 (확장 가능)
    keywords = {
        "쫓김": "shadow", "도망": "shadow", "괴물": "shadow", "귀신": "shadow",
        "돈": "wealth", "황금": "wealth", "보석": "wealth", "부자": "wealth",
        "집": "self", "방": "self", "건물": "self",
        "물": "unconscious", "바다": "unconscious", "강": "unconscious",
        "날다": "transcendence", "하늘": "transcendence", "추락": "transcendence",
        "죽음": "rebirth", "장례식": "rebirth", "시체": "rebirth"
    }
    
    # 입력값에서 키워드 추출
    detected_type = "general"
    full_text = (symbol + " " + dynamics).lower()
    for key, val in keywords.items():
        if key in full_text:
            detected_type = val
            break
            
    # 관점별 해석 데이터베이스
    interpretations = {
        "shadow": {
            "jung": "이 대상은 당신의 '그림자(Shadow)'입니다. 당신이 억누르거나 외면해온 거대한 잠재력이 의식의 문을 두드리고 있습니다.",
            "johnson": "도망치지 마십시오. 이 에너지는 당신을 해치려는 것이 아니라, 당신에게 통합되어 '힘'이 되기를 원합니다.",
            "ko": "그 추격자는 바로 '당신 자신'입니다. 외부로 투사된 나의 잃어버린 조각을 다시 내 안으로 거두어들여야 합니다.",
            "ritual": "추격자에게 이름을 붙여주고, '너는 나의 힘이다'라고 세 번 말하기"
        },
        "wealth": {
            "jung": "이것은 단순한 물질이 아니라, 당신 내면의 '자기(Self)'가 가진 고귀한 가치를 상징합니다. 당신의 영혼은 풍요롭습니다.",
            "johnson": "이 풍요로움을 죄책감 없이 받아들이십시오. 내면의 에너지가 현실의 물질로 치환될 준비가 되었습니다.",
            "ko": "당신은 이미 충분합니다. 이 상징은 당신이 가진 창조적 에너지가 현실화될 것임을 암시합니다.",
            "ritual": "지갑이나 통장을 손에 쥐고 '나는 이 풍요를 감당할 그릇이다'라고 선언하기"
        },
        "self": {
            "jung": "집은 당신의 '인격' 그 자체입니다. 새로운 방이나 공간을 발견했다면, 당신의 의식이 확장되고 있다는 증거입니다.",
            "johnson": "당신의 내면 공간을 정비하십시오. 낡은 것은 버리고 새로운 에너지가 들어올 공간을 마련해야 합니다.",
            "ko": "이 공간은 당신의 마음입니다. 꿈속의 그 장소가 어떤 느낌이었는지 기억하고, 현실의 내 방을 그와 비슷하게 꾸미십시오.",
            "ritual": "내 방의 물건 중 하나를 버리거나 위치를 바꾸어 에너지의 흐름 만들기"
        },
        "unconscious": {
            "jung": "물은 무의식의 생명력입니다. 감정의 흐름이자 창조성의 원천입니다. 당신은 지금 거대한 에너지의 흐름 속에 있습니다.",
            "johnson": "흐름에 저항하지 말고 몸을 맡기십시오. 통제하려 하기보다 직관을 따를 때 풍요가 찾아옵니다.",
            "ko": "물은 정화와 치유입니다. 당신의 묵은 감정들이 씻겨나가고 새로운 기운이 차오르고 있습니다.",
            "ritual": "따뜻한 물로 샤워를 하거나 물 한 잔을 마시며 '나는 흐른다'고 명상하기"
        },
        "transcendence": {
            "jung": "상승과 비행은 초월적 관점을 의미합니다. 당신은 지금 좁은 현실을 넘어 더 높은 차원의 해결책을 찾고 있습니다.",
            "johnson": "땅에 발을 디디는 것(Grounding)도 중요합니다. 높은 이상을 현실로 가져와 구체화하는 작업이 필요합니다.",
            "ko": "당신의 영혼은 자유롭기를 원합니다. 현실의 제약에서 벗어나 당신만의 비전을 펼칠 때입니다.",
            "ritual": "높은 곳에 올라가 아래를 내려다보거나, 점프를 10번 하며 땅의 에너지를 느끼기"
        },
        "rebirth": {
            "jung": "꿈에서의 죽음은 실제 죽음이 아니라, 낡은 자아의 해체와 '변형(Transformation)'을 의미합니다. 당신은 다시 태어나고 있습니다.",
            "johnson": "애도하십시오. 과거의 당신을 떠나보내야 새로운 당신이 들어올 수 있습니다. 이것은 축복입니다.",
            "ko": "껍질을 깨고 나오는 고통입니다. 하지만 그 끝에는 반드시 더 크고 단단한 당신이 기다리고 있습니다.",
            "ritual": "종이에 버리고 싶은 습관을 적어 찢어버리거나 태우는 상징적 행위 하기"
        },
        "general": { # 키워드가 없을 때의 일반적이지만 깊이 있는 해석
            "jung": f"'{symbol}'(이)라는 상징은 당신 무의식이 보낸 특별한 초대장입니다. 이것은 당신이 아직 알지 못하는 내면의 지혜와 연결되어 있습니다.",
            "johnson": "이 꿈의 이미지를 분석하려 하지 말고, 그저 바라보십시오. 그 안에 담긴 에너지가 당신의 삶을 역동적으로 바꿀 것입니다.",
            "ko": "꿈에 나온 모든 것은 결국 당신의 모습입니다. '{symbol}'(이)가 되어보는 상상을 해보십시오. 그것이 당신에게 무슨 말을 합니까?",
            "ritual": f"'{symbol}'의 이미지를 간단히 그리거나, 그 단어를 종이에 적어 오늘 하루 주머니에 넣고 다니기"
        }
    }
    
    return interpretations[detected_type]

# ==========================================
# 🚪 GATES & AUTH (v11.4 유지)
# ==========================================
# 1차 관문
if not st.session_state.access_granted:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-title'>D-Fi : 무의식의 연금술</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='quote-box'>
            "무의식에 다가가서 무의식의 상징 언어를 배운다면,<br>
            삶을 좀 더 풍요롭고 충만하게 살 수 있다."
            <span class='author'>- Carl Gustav Jung (심층 심리학자)</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class='step-container'>
            <div class='step-title'>🏛️ 로버트 A. 존슨의 꿈 작업 4단계</div>
            <div class='step-list'>
                <b>1단계 : 연상 (Association)</b> - 꿈속 상징의 개인적 의미 발견<br>
                <b>2단계 : 역학 (Dynamics)</b> - 내면 에너지의 흐름 파악<br>
                <b>3단계 : 해석 (Interpretation)</b> - 무의식의 메시지 통합<br>
                <b>4단계 : 의례 (Ritual)</b> - 구체적 행동으로 현실화 (자산 발행)
            </div>
        </div>
        """, unsafe_allow_html=True)
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

# 2차 관문
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
                            st.session_state.s1_val = d.get('symbol', "")
                            st.session_state.s2_val = d.get('block', "")
                            st.session_state.s4_val = d.get('ritual_self', "")
                            meaning_text = d.get('meaning', "")
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
                            st.session_state.interpretation_ready = True if meaning_text else False
                            # 로드시 해석 복원 (저장된 값이 없으면 빈칸)
                            st.session_state.s3_val = "" 
                            st.session_state.is_minted = True if meaning_text else False
                            st.rerun()
                    with c_r: st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
            else: st.info("기록 없음")
        except: pass
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
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
    st.markdown("### 🏛️ D-Fi 연금술")
    
    st.text_area("🚀 Stage 1: 연상 (Association)", value=st.session_state.s1_val, height=70, key="s1_key", placeholder="핵심 단어 입력 (예: 쫓김, 돈, 바다)")
    st.text_area("🔍 Stage 2: 역학 (Dynamics)", value=st.session_state.s2_val, height=70, key="s2_key", placeholder="어떤 기분이었나요?")
    
    if st.button("▼ 마스터 해석 가동 (ENTER)"):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        if s1_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            
            # [🔥 CORE] 해석 엔진 가동
            result = analyze_dream_engine(s1_input, s2_input)
            
            # 결과 포맷팅
            analysis_text = f"""[🏛️ D-Fi 심층 분석 결과]

1. 👤 칼 융 (C.G. Jung):
"{result['jung']}"

2. ⚖️ 로버트 A. 존슨 (Robert A. Johnson):
"{result['johnson']}"

3. 🕯️ 고혜경 박사 (Projective Work):
"{result['ko']}"
"""
            st.session_state.s3_val = analysis_text
            st.session_state.s4_val = result['ritual'] # 의례 자동 추천
            st.session_state.interpretation_ready = True
            st.toast("✨ 무의식 데이터 분석 완료!")
        else: st.warning("Stage 1(상징)을 입력해야 해석할 수 있습니다.")

    st.text_area("🏛️ Stage 3: 해석 (Interpretation)", value=st.session_state.s3_val, height=350, disabled=False, key="s3_key")

    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: 의례 (Ritual)")
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 지난 자산 가치: {st.session_state.existing_value}")
        
        # 의례 입력창 (자동 추천된 값이 기본값으로 들어감)
        s4 = st.text_input("구체적 실천 행동 (자동 추천됨, 수정 가능)", value=st.session_state.s4_val)
        
        final_btn = "🏛️ 자산 정보 업데이트" if st.session_state.is_minted else "💎 최종 자산 발행 (Mint Token)"
        if st.form_submit_button(final_btn):
            if st.session_state.s1_val and s4:
                token_val = min(5000, 1000 + len(st.session_state.s1_val + s4)*10)
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
