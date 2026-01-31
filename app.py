import streamlit as st
from supabase import create_client, Client
import datetime

# [SYSTEM VIBE: SUPREME CONTRAST & PHILOSOPHICAL DEPTH]
st.set_page_config(page_title="D-Fi Vault v7.5", page_icon="🏛️", layout="wide")

# CSS: 전 스테이지 가독성 강화 및 50:50 레이아웃 최적화
st.markdown("""
    <style>
    /* 전체 배경 및 텍스트 기본 설정 */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* 좌우 패널 구분 */
    .left-panel { background-color: #161B22; padding: 25px; border-radius: 15px; border: 1px solid #30363D; height: 100%; }
    .right-panel { background-color: #1E1E1E; padding: 25px; border-radius: 15px; border: 1px solid #D4AF37; height: 100%; }
    
    /* 🔴 빌더님 핵심 요청: 전 스테이지(1~4) 설명글 가독성 강화 */
    .stage-desc { 
        color: #E0E0E0 !important; /* 고대비 밝은 미색 */
        font-size: 1.1em !important; 
        font-weight: 400;
        line-height: 1.6; 
        margin-bottom: 12px;
        display: block;
        padding: 5px 0;
    }
    
    /* 헤더 스타일 */
    .stSubheader { color: #D4AF37 !important; font-weight: bold !important; margin-top: 25px !important; }
    
    /* 마스터 메시지 박스 */
    .master-dialogue { 
        background-color: #2D2D2D; padding: 18px; border-radius: 12px; 
        border-left: 5px solid #D4AF37; margin-top: 15px; font-size: 0.95em; line-height: 1.5;
    }
    .master-name { color: #D4AF37; font-weight: bold; margin-right: 8px; }
    
    /* 버튼 스타일 */
    .stButton>button { 
        background: linear-gradient(45deg, #D4AF37, #FF4B4B); 
        color: white; font-weight: bold; border: none; border-radius: 8px; width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# [CONNECTION: SUPABASE]
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# [LAYOUT: 50:50 SPLIT]
col_left, col_right = st.columns(2)

# --- LEFT PANEL: 원재료 보관소 ---
with col_left:
    st.markdown("<div class='left-panel'>", unsafe_allow_html=True)
    st.title("📓 무의식 원재료")
    
    if st.button("📂 지난 꿈 자산 불러오기"):
        try:
            res = supabase.table("dreams").select("*").order("created_at", desc=True).limit(3).execute()
            if res.data:
                for item in res.data:
                    with st.expander(f"📅 {item['created_at'][:10]} | {item['symbol'][:15]}..."):
                        st.write(f"**해석:** {item['meaning']}")
                        st.write(f"**의례:** {item['ritual_self']}")
            else: st.info("아직 기록된 자산이 없습니다.")
        except: st.error("데이터 저장소 연결을 확인하세요.")

    dream_raw = st.text_area("꿈의 내용을 날것 그대로 기록하세요", height=450, placeholder="이미지, 느낌, 대화 등 기억나는 모든 것...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- RIGHT PANEL: 마스터 컨설팅 룸 ---
with col_right:
    st.markdown("<div class='right-panel'>", unsafe_allow_html=True)
    st.title("🏛️ Master's Lab")
    
    with st.form("master_process"):
        # Stage 1: 이미지 연상 (Robert Johnson)
        st.subheader("🚀 Stage 1: 이미지 연상")
        st.markdown("<span class='stage-desc'>꿈의 파편에서 가장 강렬한 상징들을 추출하세요. 분석하려 하지 말고 보이는 대로 나열합니다.</span>", unsafe_allow_html=True)
        s1_images = st.text_input("상징의 원석", placeholder="예: 거대한 해일, 은색 동전, 붉은 꽃")

        # Stage 2: 역학관계 (Dynamics)
        st.subheader("🔍 Stage 2: 내적 역학")
        st.markdown("<span class='stage-desc'>이 이미지들이 현재 당신의 현실(경제적 결정, 관계, 심리적 갈등)과 어떤 에너지를 주고받나요?</span>", unsafe_allow_html=True)
        s2_dynamics = st.text_area("에너지 줄다리기", placeholder="예: 해일은 통제 불가능한 시장 상황을, 동전은 나의 위축된 투자 심리를 보여줌")

        # Stage 3: 통합 해석 (Master Dialogue)
        st.subheader("📝 Stage 3: 마스터 통합 해석")
        st.markdown("<span class='stage-desc'>융, 존슨, 고혜경 박사가 당신의 데이터를 바탕으로 심층 토론을 벌인 결과입니다.</span>", unsafe_allow_html=True)
        
        # 실제 AI 연결 전, 빌더님의 지침을 반영한 시뮬레이션 로직
        if s1_images and s2_dynamics:
            interpret_box = st.container()
            with interpret_box:
                st.markdown(f"""
                <div class='master-dialogue'>
                    <div><span class='master-name'>Carl Jung:</span> "{s1_images}은(는) 당신의 전체성을 향한 보상적 원형입니다. 현재의 현실을 정면으로 보라는 신호군요."</div>
                    <div><span class='master-name'>Robert Johnson:</span> "이 이미지는 살아있는 에너지입니다. 머리로 이해하지 말고 가슴으로 이 에너지의 흐름을 느끼세요."</div>
                    <div><span class='master-name'>Koh Hye-kyung:</span> "영혼이 당신에게 말을 걸고 있습니다. 이 역동을 통해 당신은 더 큰 풍요를 담을 그릇으로 거듭날 것입니다."</div>
                </div>
                """, unsafe_allow_html=True)
                final_insight = f"{s1_images}을 통한 자기 객관화와 에너지의 통합"
        else:
            final_insight = "1, 2단계를 입력하면 마스터들의 분석이 시작됩니다."

        # Stage 4: 현실 의례 (Ritual)
        st.subheader("🏃 Stage 4: 현실화 의례")
        st.markdown("<span class='stage-desc'>이 통찰을 현실의 부와 안정으로 고정하기 위해 오늘 당장 몸으로 실천할 구체적 행동을 제안합니다.</span>", unsafe_allow_html=True)
        
        auto_ritual = "이미지를 상징하는 작은 물건을 책상에 두고, 5분간 숨을 고르며 투자 원칙을 재정비하세요." if s1_images else ""
        st.info(f"💡 권장 의례: {auto_ritual}")
        
        s4_action = st.text_input("확정된 나의 행동", placeholder="예: 경제 지표 확인 후 명상 10분")
        s4_share = st.text_input("타인과 나눌 가치", placeholder="예: 오늘 깨달은 통찰을 커뮤니티에 공유")

        # 저장
        if st.form_submit_button("마스터의 지혜를 금고에 저장"):
            if s1_images and s4_action:
                data = {
                    "symbol": s1_images, "block": s2_dynamics, "context": dream_raw,
                    "meaning": final_insight, "ritual_self": s4_action, "ritual_share": s4_share
                }
                try:
                    supabase.table("dreams").insert(data).execute()
                    st.balloons()
                    st.success("빌더님, 당신의 내적 자산이 성공적으로 기록되었습니다.")
                except Exception as e:
                    st.error(f"저장 실패: {e}")
            else:
                st.warning("상징 추출과 행동 계획은 필수입니다.")

    st.markdown("</div>", unsafe_allow_html=True)
