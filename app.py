import streamlit as st
from supabase import create_client, Client
import time
import datetime
import random

# [SYSTEM CONFIG]
st.set_page_config(page_title="D-Fi Vault v11.8", page_icon="🏛️", layout="wide")

# 🔒 1차 관문: 커뮤니티 공통 암호
COMMUNITY_PASSWORD = "korea2026"

# --- CSS: 디자인 (Manifesto & Golden Dark) ---
st.markdown("""
    <style>
    /* 1. 전체 테마: Deep Black */
    .stApp { background-color: #050505 !important; color: #FFFFFF !important; }
    
    /* 2. 버튼 스타일 */
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
    
    /* 4. 헤더/푸터 및 경고 숨김 */
    header, footer { visibility: hidden !important; }
    h1, h2, h3, h4, p, label, .stMarkdown, .stMetricValue, .stMetricLabel { color: #FFFFFF !important; }
    .stAlert { display: none; } 
    
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
    
    /* 멘트 스타일 수정 */
    .defi-desc {
        text-align: center; color: #BBBBBB; font-size: 1.0em; margin-top: 30px; margin-bottom: 30px; border-top: 1px solid #333; padding-top: 20px; line-height: 1.6;
    }
    .highlight { color: #FDB931; font-weight: bold; }
    .faint-hint { color: #666666; font-size: 0.9em; margin-top: 15px; font-style: italic; }
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
# 🧠 [CORE LOGIC] 문맥 반영 해석 엔진
# ==========================================
def analyze_dream_engine(symbol, dynamics):
    keywords = {
        "옷": "persona", "의복": "persona", "체육복": "persona", "유니폼": "persona", "가면": "persona",
        "쫓김": "shadow", "도망": "shadow", "괴물": "shadow", "귀신": "shadow", "공격": "shadow",
        "돈": "wealth", "황금": "wealth", "보석": "wealth", "부자": "wealth", "주식": "wealth",
        "집": "self", "방": "self", "건물": "self", "이사": "self", "청소": "self",
        "물": "unconscious", "바다": "unconscious", "강": "unconscious", "수영": "unconscious",
        "날다": "transcendence", "하늘": "transcendence", "비행기": "transcendence", "추락": "transcendence",
        "죽음": "rebirth", "장례식": "rebirth", "시체": "rebirth", "살인": "rebirth", "불": "rebirth",
        "똥": "wealth", "대변": "wealth"
    }
    detected_type = "general"
    full_text = (symbol + " " + dynamics).lower()
    for key, val in keywords.items():
        if key in full_text:
            detected_type = val
            break
            
    interpretations = {
        "persona": {
            "jung": f"'{symbol}'은(는) 당신의 사회적 가면(Persona)입니다. 당신이 '{dynamics}'라고 느낀 것은, 현재 역할에 변화가 필요함을 무의식이 알리는 신호입니다.",
            "johnson": f"우리는 종종 맞지 않는 옷을 입고 삽니다. '{dynamics}'의 느낌은 겉모습과 내면 사이의 조율이 필요함을 암시합니다.",
            "ko": f"남들에게 보여주고 싶은 당신의 모습이 '{symbol}'입니다. '{dynamics}'의 상황은 낡은 이미지를 벗고 진실된 나를 드러내도 좋다는 메시지입니다.",
            "ritual": f"오늘 하루, 평소에 입지 않던 스타일의 옷을 입거나 '{symbol}'과 관련된 물건 정리하기"
        },
        "shadow": {
            "jung": f"'{symbol}'은(는) 당신의 그림자(Shadow)입니다. 당신이 '{dynamics}'의 반응을 보인 것은, 억눌린 에너지가 통합을 요구하는 것입니다.",
            "johnson": f"도망치지 마십시오. '{dynamics}'의 상황은 공포가 아닌 초대입니다. 이 에너지는 당신의 힘이 되길 원합니다.",
            "ko": f"추격자는 곧 '당신 자신'입니다. '{dynamics}'하며 거부했던 그 힘을 받아들일 때 당신은 온전해집니다.",
            "ritual": f"'{symbol}'에게 이름을 붙여주고, '너는 나의 힘이다'라고 세 번 말하기"
        },
        "wealth": {
            "jung": f"'{symbol}'은(는) 내면의 '자기(Self)'가 가진 고귀한 가치입니다. '{dynamics}'의 상황은 영적 풍요가 현실화될 준비가 되었음을 뜻합니다.",
            "johnson": f"죄책감 없이 풍요를 받으십시오. '{dynamics}'의 흐름은 창조적 에너지가 밖으로 흘러나와야 함을 보여줍니다.",
            "ko": f"당신은 이미 충분합니다. 무의식은 당신의 잠재력이 '{dynamics}'의 방식으로 세상에 기여할 수 있음을 암시합니다.",
            "ritual": f"지갑이나 통장을 쥐고 '나는 이 풍요를 감당할 그릇이다'라고 선언하기"
        },
        "self": {
            "jung": f"'{symbol}'은(는) 당신의 인격 구조입니다. '{dynamics}'라고 묘사한 것은 의식이 새로운 영역으로 확장되고 있음을 뜻합니다.",
            "johnson": f"내면 공간을 정비하십시오. '{dynamics}'의 느낌을 살피고, 새로운 에너지가 들어올 공간을 마련하십시오.",
            "ko": f"이 공간은 당신의 마음입니다. '{symbol}'에서 느낀 '{dynamics}'의 감정을 현실의 내 방에 적용해보세요.",
            "ritual": f"내 방의 물건 중 하나를 버리거나 위치를 바꾸어 '{dynamics}'의 에너지 만들기"
        },
        "general": {
            "jung": f"'{symbol}'은(는) 무의식이 보낸 암호입니다. 특히 '{dynamics}'라고 느낀 부분에 당신 성장의 열쇠가 있습니다.",
            "johnson": f"분석하려 하지 말고 '{dynamics}'의 에너지 자체를 느끼십시오. '{symbol}'은(는) 삶을 바꿀 촉매제입니다.",
            "ko": f"꿈속의 모든 것은 당신입니다. 당신이 '{symbol}'이(가) 되어 '{dynamics}'의 상황을 겪는다고 상상해보세요.",
            "ritual": f"'{symbol}'의 이미지를 그리거나 단어를 적어 주머니에 넣고 다니기"
        }
    }
    return interpretations.get(detected_type, interpretations["general"])

# ==========================================
# 🚪 1차 관문: Manifesto & Story
# ==========================================
if not st.session_state.access_granted:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='main-title'>D-Fi : 무의식의 연금술</div>", unsafe_allow_html=True)
        st.markdown("""
        <div class='quote-box'>
            "현실의 결핍은 무의식의 풍요로 채워진다.<br>
            이것은 평범한 개인이 자신의 운명을 바꾸는 <span class='highlight'>퀀텀 점프 실험실</span>입니다."
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='defi-desc'>
            <p style='font-size:1.2em; color:#D4AF37; font-weight:bold;'>🪙 Dream Pts : 나의 퀀텀 에너지 지수</p>
            
            <p><b>1. 성장의 시각화 (Visualizing Growth)</b><br>
            저는 생존을 고민하는 평범한 사람입니다. <br>
            하지만 매일 밤 <b>꿈(무의식)</b>을 채굴하여 제 잠재력을 깨우고 있습니다.<br>
            여기에 쌓이는 포인트는 제가 얼마나 깊이 각성했는지를 보여주는 <b>성장의 증명</b>입니다.</p>

            <p><b>2. 현실의 변화 (X-Factor)</b><br>
            이곳에서 제련된 통찰은 <b>X(트위터)</b>와 현실의 콘텐츠가 됩니다.<br>
            무의식의 영감이 어떻게 <b>노출수(Traffic)</b>와 <b>수익(Revenue)</b>으로 변환되는지 목격하십시오.</p>

            <div class='faint-hint'>
            "상상해 보십시오. 제가 퀀텀 점프에 성공하는 날,<br>
            이곳에 남겨진 당신의 <b>초기 채굴 기록(Genesis Data)</b>들이<br>
            어떤 가치(Value)로 치환될지... 그 가능성은 열어두겠습니다."
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

# ==========================================
# 🚪 2차 관문 (Identity Check) - 유지
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
                            st.session_state.s1_val = d.get('symbol', "")
                            st.session_state.s2_val = d.get('block', "")
                            st.session_state.s4_val = d.get('ritual_self', "")
                            meaning_text = d.get('meaning', "")
                            st.session_state.existing_value = meaning_text if meaning_text else "미발행"
                            st.session_state.interpretation_ready = True if meaning_text else False
                            st.session_state.s3_val = "" 
                            if 's3_key' in st.session_state: del st.session_state.s3_key 
                            st.session_state.is_minted = True if meaning_text else False
                            st.rerun()
                    with c_r: st.write(f"{d['created_at'][:10]} | {d.get('context', '')[:10]}...")
            else: st.info("기록 없음")
        except: pass
    
    if st.button("🔄 새로 쓰기 (Reset)"):
        for key in ['current_dream_id', 'dream_context', 's1_val', 's2_val', 's3_val', 's4_val', 'existing_value']:
            st.session_state[key] = "" if key != 'current_dream_id' else None
        if 's3_key' in st.session_state: del st.session_state.s3_key 
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
    
    st.text_area("🚀 Stage 1: 연상 (Association)", value=st.session_state.s1_val, height=70, key="s1_key", placeholder="핵심 단어 입력 (예: 쫓김, 돈, 옷, 바다)")
    st.text_area("🔍 Stage 2: 역학 (Dynamics)", value=st.session_state.s2_val, height=70, key="s2_key", placeholder="어떤 기분이나 상황이었나요?")
    
    if st.button("▼ 마스터 해석 가동 (ENTER)"):
        s1_input = st.session_state.s1_key
        s2_input = st.session_state.s2_key
        if s1_input: 
            st.session_state.s1_val = s1_input
            st.session_state.s2_val = s2_input
            
            result = analyze_dream_engine(s1_input, s2_input)
            
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
            st.toast("✨ 분석 완료! 해석이 로딩되었습니다.")
            time.sleep(0.1) 
            st.rerun()
        else: st.warning("Stage 1(상징)을 입력해야 해석할 수 있습니다.")

    if 's3_key' not in st.session_state: st.session_state.s3_key = st.session_state.s3_val
    st.text_area("🏛️ Stage 3: 해석 (Interpretation)", height=350, disabled=False, key="s3_key")

    with st.form("mint_form"):
        st.markdown("#### 💎 Stage 4: 의례 (Ritual)")
        if st.session_state.is_minted and st.session_state.existing_value: st.info(f"📉 지난 자산 가치: {st.session_state.existing_value}")
        
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
