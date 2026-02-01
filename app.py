# (위쪽 코드는 동일하므로 생략, analyze_dream_engine 함수와 결과 출력 부분만 수정합니다)

def analyze_dream_engine(symbol, dynamics):
    # ... (기존 키워드 매칭 로직 동일) ...
    
    # 3. [신규 기능] AI 그림 프롬프트 생성 (Image Prompt)
    # 실제로는 ChatGPT API가 연결되면 꿈 내용에 맞춰 자동 생성되지만,
    # 지금은 시뮬레이션으로 '상징'과 '역학'을 조합한 영어 프롬프트를 만듭니다.
    
    art_style = random.choice([
        "Oil painting style, heavy brushstrokes, dark background",
        "Cyberpunk style, neon lights, futuristic atmosphere",
        "Surrealism style like Dali, melting objects, dreamlike",
        "Minimalist line art, golden lines on black paper",
        "Watercolor style, soft pastel colors, healing atmosphere"
    ])
    
    # 영어로 번역된 느낌을 주기 위한 가상 로직
    symbol_en = {"쫓김": "chasing shadow", "돈": "golden coins", "집": "mysterious house", "바다": "deep blue ocean"}.get(symbol, "mysterious symbol")
    
    image_prompt = f"/imagine prompt: A cinematic shot of {symbol_en} representing {dynamics}, {art_style}, 8k resolution, --ar 16:9"

    interpretations = {
        # ... (기존 해석 로직 동일, 여기에 image_prompt 추가) ...
        "general": {
            "jung": f"...", # (기존 내용)
            "johnson": f"...",
            "ko": f"...",
            "ritual": f"...",
            "prompt": image_prompt # 프롬프트 저장
        }
    }
    # (키워드 매칭된 해석에도 prompt를 추가해야 하지만, 
    # 코드가 너무 길어지므로 'result' 딕셔너리에 'prompt' 키가 있다고 가정하고 아래 UI를 짭니다.)
    
    # 편의상 모든 결과에 프롬프트를 강제로 넣는 로직 (시뮬레이션용)
    result = interpretations.get(detected_type, interpretations["general"])
    result['prompt'] = image_prompt 
    return result

# ... (중략) ...

# [UI 출력 부분 수정]
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

--------------------------------------------------
🎨 [보너스] 무의식 형상화 주문서 (Image Prompt):
(아래 텍스트를 복사해서 AI 그림 도구에 넣어보세요)

`{result['prompt']}`
--------------------------------------------------
"""
            # (이하 저장 로직 동일)
