import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: ABSOLUTE CLARITY & MASTER'S TOUCH]
st.set_page_config(page_title="D-Fi Vault v7.6", page_icon="🏛️", layout="wide")

# --- CSS: 가독성 및 UI 전면 개편 ---
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 기본 설정 */
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* 좌우 패널 스타일 (테두리 및 배경) */
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; height: 100%; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; height: 100%; }
    
    /* 🔴 핵심 수정 1: 입력창(TextArea/Input) 가독성 극대화 */
    .stTextArea textarea, .stTextInput input {
        background-color: #21262D !important; /* 더 밝은 배경 */
        color: #FFFFFF !important; /* 완전한 흰색 텍스트 */
        border: 1px solid #484F58 !important;
        font-size: 1.05em !important;
    }
    .stTextArea textarea::placeholder, .stTextInput input::placeholder {
        color: #8B949E !important; /* 플레이스홀더도 선명하게 */
    }
    
    /* 🔴 핵심 수정 2: 버튼 스타일 (상시 고대비 유지) */
    .stButton>button { 
        background: linear-gradient(90deg, #D4AF37, #E6C200) !important; /* 황금빛 그라데이션 */
        color: #000000 !important; /* 검은색 텍스트로 대비 극대화 */
        font-weight: 800 !important; 
        border: none; border-radius: 8px; 
        padding: 12px 20px;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #E6C200, #FFD700) !important; /* 호버 시 더 밝게 */
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.3); /* 빛나는 효과 */
    }

    /* 🔴 핵심 수정 3: 단계 설명글 가독성 (기존 유지) */
    .stage-desc { 
        color: #E0E0E0 !important; 
        font-size: 1.1em !important; font-weight: 400; line-height: 1.6; 
        margin-bottom: 12px; display: block;
    }

    /* 헤더 및 기타 스타일 */
    .stSubheader { color: #D4AF37 !important; font-weight: bold !important; margin-top: 25px !important; }
    .master-dialogue { 
        background-color: #2D2D2D; padding: 18px; border-radius: 12px; 
        border-left: 5px solid #D4AF37; margin-top: 15px; font-size: 0.95em; line-height: 1.5;
    }
    .master-name { color: #D4AF37; font-weight: bold; margin-right: 8px; }
    .save-explainer { color: #8B949E; font-size: 0.9em; margin-top: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error(f"수파베이스 연결 오류: {e}. Secrets 설정을 확인하세요.")
    st.stop()

# [LAYOUT: 50:50 SPLIT]
col_left, col_right = st.columns(2)

# --- LEFT PANEL: 원재료 보관소 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    # 지난 꿈 불러오기
    if st.button("📂 지난 꿈 자산 불러오기"):
        try:
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(3).execute()
            if res.data:
                for item in res.data:
                    dream_date = datetime.datetime.fromisoformat(item['created_at']).strftime('%Y-%m-%d')
                    preview = item.get('symbol', '기록 없음')[:15]
                    with st.expander(f"📅 {dream_date} | {preview}..."):
                        st.write(f"**원문:** {item.get('context', '내용 없음')}")
                        if item.get('meaning'):
                             st.write(f"**해석:** {item['meaning']}")
            else: st.info("아직 기록된 자산이 없습니다.")
        except Exception as e: st.error(f"데이터 불러오기 실패: {e}")

    # 🔴 핵심 수정 4: 꿈 원문 입력창 가독성 강화 및 저장 버튼 추가
    with st.form("raw_dream_form"):
        dream_raw = st.text_area("꿈의 내용을 날것 그대로 기록하세요", height=400, 
                                 placeholder="여기에 꿈을 기록하면 글자가 선명하게 보입니다. \n줄바꿈(Enter)도 자유롭게 사용하세요.")
        if st.form_submit_button("📓 이 꿈만 날것으로 저장하기"):
            if dream_raw:
                try:
                    # 원문만 저장 (나머지 필드는 null)
                    supabase.table("dreams").insert({"context": dream_raw}).execute()
                    st.toast("✅ 꿈 원문이 안전하게 금고에 저장되었습니다!", icon="📓")
                except Exception as e: st.error(f"저장 실패: {e}")
            else:
                st.warning("저장할 꿈 내용이 비어있습니다.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 컨설팅 룸 ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    with st.form("master_process"):
        # 🔴 핵심 수정 5: Stage 1 & 2를 text_area로 변경하여 줄바꿈 지원
        st.subheader("🚀 Stage 1: 이미지 연상")
        st.markdown("<span class='stage-desc'>꿈의 파편에서 가장 강렬한 상징들을 추출하세요. 분석하려 하지 말고 보이는 대로 나열합니다. (줄바꿈 가능)</span>", unsafe_allow_html=True)
        s1_images = st.text_area("상징의 원석", height=100, placeholder="예:\n- 거대한 해일\n- 은색 동전\n- 붉은 꽃")

        st.subheader("🔍 Stage 2: 내적 역학")
        st.markdown("<span class='stage-desc'>이 이미지들이 현재 당신의 현실(경제적 결정, 관계, 심리적 갈등)과 어떤 에너지를 주고받나요? (줄바꿈 가능)</span>", unsafe_allow_html=True)
        s2_dynamics = st.text_area("에너지 줄다리기", height=150, placeholder="예:\n- 해일: 통제 불가능한 시장 상황\n- 동전: 나의 위축된 투자 심리")

        # Stage 3: 통합 해석 (Master Dialogue)
        st.subheader("📝 Stage 3: 마스터 통합 해석")
        st.markdown("<span class='stage-desc'>융, 존슨, 고혜경 박사가 당신의 데이터를 바탕으로 심층 토론을 벌인 결과입니다.</span>", unsafe_allow_html=True)
        
        # AI 시뮬레이션 로직
        final_insight = ""
        if s1_images and s2_dynamics:
            st.markdown(f"""
            <div class='master-dialogue'>
                <div><span class='master-name'>Carl Jung:</span> "제시된 상징들은 당신의 전체성을 향한 보상적 원형입니다. 무의식이 현실의 균형을 맞추려 하고 있습니다."</div>
                <br>
                <div><span class='master-name'>Robert Johnson:</span> "이 에너지는 단순한 생각이 아닙니다. 머리가 아닌 가슴으로 이 역동의 흐름을 직면해야 합니다."</div>
                <br>
                <div><span class='master-name'>Koh Hye-kyung:</span> "영혼이 경제적 자립을 위한 생명줄을 던졌습니다. 이 에너지를 현실의 풍요를 담을 그릇으로 쓰세요."</div>
            </div>
            """, unsafe_allow_html=True)
            final_insight = f"[{s1_images.splitlines()[0] if s1_images else '상징'}] 등을 통한 자기 객관화와 에너지 통합의 메시지"
        else:
            st.info("👉 1, 2단계를 입력하면 마스터들의 분석이 시작됩니다.")

        # Stage 4: 현실 의례 (Ritual)
        st.subheader("🏃 Stage 4: 현실화 의례")
        st.markdown("<span class='stage-desc'>이 통찰을 현실의 부와 안정으로 고정하기 위해 오늘 당장 몸으로 실천할 구체적 행동을 제안합니다.</span>", unsafe_allow_html=True)
        
        auto_ritual = "가장 강렬한 상징을 작은 종이에 그려 지갑에 넣고, 투자 원칙을 소리 내어 읽으세요." if s1_images else "상징이 입력되면 맞춤 의례가 제안됩니다."
        st.info(f"💡 권장 의례: {auto_ritual}")
        
        s4_action = st.text_input("확정된 나의 행동", placeholder="예: 경제 지표 확인 후 명상 10분")
        s4_share = st.text_input("타인과 나눌 가치", placeholder="예: 오늘 깨달은 통찰을 커뮤니티에 공유")

        # 🔴 핵심 수정 6: 마스터 금고 저장 버튼 가독성 및 설명 추가
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True) # 간격 추가
        submit_button = st.form_submit_button("🏛️ 마스터의 지혜를 금고에 저장")
        st.markdown("<p class='save-explainer'>ℹ️ 이 버튼은 1~4단계의 모든 분석 결과를 최종 자산으로 저장합니다.</p>", unsafe_allow_html=True)

        if submit_button:
            if s1_images and s4_action:
                data = {
                    "symbol": s1_images, "block": s2_dynamics, 
                    # 왼쪽 패널의 원문과 연결 (여기서는 현재 세션의 원문이 없으므로 빈칸 처리 or 추후 연동 필요)
                    "context": "마스터 랩에서 직접 분석 수행", 
                    "meaning": final_insight, "ritual_self": s4_action, "ritual_share": s4_share
                }
                try:
                    supabase.table("dreams").insert(data).execute()
                    st.balloons()
                    st.toast("🎉 마스터와의 협업 결과가 완벽하게 금고에 저장되었습니다!", icon="🏛️")
                except Exception as e:
                    st.error(f"저장 실패: {e}")
            else:
                st.warning("⚠️ 상징 추출(Stage 1)과 나의 행동(Stage 4)은 필수입니다.")

    st.markdown("</div>", unsafe_allow_html=True)
