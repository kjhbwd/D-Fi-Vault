with st.form("self_prosperity_form"):
    # Stage 1: 내 안의 잠재 자원 발견 ( Associations )
    st.subheader("🚀 Stage 1: 내면의 원석 발견 (Associations)")
    st.info("이 상징은 현재 '나'에게 어떤 유익한 정보를 주고 있나요?")
    symbol = st.text_input("꿈의 상징", placeholder="예: 끊이지 않는 샘물")

    # Stage 2: 에너지 누수 진단 ( Inner Dynamics )
    st.subheader("🔍 Stage 2: 내면의 에너지 정렬 (Inner Dynamics)")
    st.write("경제적/심리적 안정을 가로막는 내 안의 방해 요소를 찾습니다.")
    inner_block = st.selectbox("현재 나의 흐름을 막는 인격은?", 
                               ["결핍을 두려워하는 나", "성공을 회피하는 나", "과거에 머무는 나", "완벽주의자"])
    context = st.text_input("이것이 해결되면 좋아질 나의 현실 영역", placeholder="예: 자금 흐름, 업무 집중도")

    # Stage 3: 나를 위한 가치 제언 ( Interpretation )
    st.subheader("📝 Stage 3: 1호 수혜자를 위한 해석 (Interpretation)")
    meaning = st.text_area("이 꿈이 '나의 경제적 자립'을 위해 던지는 직구", 
                           placeholder="예: '불안해서 투자하지 말고, 확신이 생길 때까지 에너지를 응축하라'")

    # Stage 4: 부의 선순환 의례 ( Ritual for Prosperity )
    st.subheader("🏃 Stage 4: 나를 살리고 이웃을 돕는 의례 (Ritual)")
    st.write("먼저 나를 채우는 행동을 정하고, 그 결과로 타인에게 줄 수 있는 가치를 적습니다.")
    ritual_self = st.text_input("나를 위한 작은 행동 (경제적 이득과 연결)", placeholder="예: 관련 경제 지표 30분 공부하기")
    ritual_share = st.text_input("내가 여유로워졌을 때 이웃에게 줄 도움", placeholder="예: 오늘 얻은 통찰을 커뮤니티에 공유하기")

    submit_button = st.form_submit_button("나의 자산 금고에 저장")

if submit_button:
    # (구글 시트 저장 로직은 동일하게 유지)
    st.success("빌더님, 오늘의 작업으로 내면 자산이 한 층 더 견고해졌습니다!")
    st.balloons()
