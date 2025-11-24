# AI-DLC 테스트 방법론 개요

## AI-DLC vs 전통적 SDLC 테스트 비교

### 테스트 접근법 차이

```mermaid
flowchart TD
    subgraph Traditional["전통적 SDLC 테스트"]
        T1[개발자가 코드 작성]
        T2[개발자가 테스트 작성 수동<br/>• 예상 입력 정의<br/>• 예상 출력 정의<br/>• assert expected == actual]
        T3[테스트 실행]
        T4[통과 → 배포]
        T5[실패 → 수정]

        T1 --> T2 --> T3
        T3 -->|Pass| T4
        T3 -->|Fail| T5
        T5 --> T1

        Problems["❌ 문제점:<br/>• 엣지 케이스 수작업 작성<br/>• 유지보수 비용 높음<br/>• LLM 비결정성 대응 불가"]
    end

    subgraph AIDLC["AI-DLC 테스트"]
        A1[AI가 코드 생성]
        A2["AI + 개발자가 테스트 작성<br/>• Property-Based Testing<br/>• Metamorphic Testing<br/>• LLM-as-Judge<br/>• Self-Healing Tests"]
        A3["자동화된 검증<br/>• 수천 개 케이스 자동 테스트<br/>• 반례 자동 축소<br/>• 지속적 개선"]
        A4[배포]

        A1 --> A2 --> A3 --> A4

        Benefits["✅ 장점:<br/>• 자동 엣지 케이스 발견<br/>• LLM 비결정성 해결<br/>• 유지보수 비용 감소"]
    end

    style Traditional fill:#ffcccc
    style AIDLC fill:#ccffcc
    style Problems fill:#fff0f0
    style Benefits fill:#f0fff0
```

---

## AI-DLC 테스트 기법 상세 비교

### 1. TDD/BDD with AI

#### 전통적 TDD

```mermaid
flowchart LR
    Red[🔴 Red<br/>테스트 작성<br/>실패] --> Green[🟢 Green<br/>코드 구현<br/>통과]
    Green --> Refactor[♻️ Refactor<br/>리팩토링<br/>개선]
    Refactor --> Red

    style Red fill:#ffcccc
    style Green fill:#ccffcc
    style Refactor fill:#ccffff
```

#### AI-Powered TDD

```mermaid
flowchart LR
    AIRed["🤖🔴 Red<br/>AI: 테스트 초안 생성<br/>Dev: 검토 & 승인"] --> AIGreen["🤖🟢 Green<br/>AI: 구현 제안<br/>Dev: 승인 & 조정"]
    AIGreen --> AIRefactor["🤖♻️ Refactor<br/>AI: 최적화 제안<br/>Dev: 승인 & 검증"]
    AIRefactor --> AIRed

    Metrics["⚡ 속도: 2-3배 향상<br/>✅ 품질: 더 많은 테스트<br/>📊 커버리지: 엣지 케이스 자동 포함"]

    style AIRed fill:#ffd9cc
    style AIGreen fill:#d9ffcc
    style AIRefactor fill:#d9f0ff
    style Metrics fill:#fff9cc
```

---

### 2. Metamorphic Testing

#### 핵심 아이디어
정확한 출력을 예측할 수 없어도, **입력 변환 시 출력 간 관계**는 검증 가능!

##### 1. 순열 불변성 (Permutation Invariance)

```mermaid
graph LR
    subgraph Input1["입력 1"]
        I1["'1+2+3'"]
    end

    subgraph Input2["입력 2 (순서 변경)"]
        I2["'3+2+1'"]
    end

    subgraph Process["처리"]
        F1["function(x)"]
        F2["function(permute(x))"]
    end

    subgraph Output["출력"]
        O1["6"]
        O2["6"]
    end

    I1 --> F1 --> O1
    I2 --> F2 --> O2
    O1 -.동일.-> O2

    Property["Property:<br/>f(x) == f(permute(x))<br/>(덧셈은 순서 무관)"]

    style Input1 fill:#e1f5ff
    style Input2 fill:#e1f5ff
    style Output fill:#ccffcc
    style Property fill:#fff9cc
```

##### 2. 가산 단조성 (Additive Monotonicity)

```mermaid
graph TB
    subgraph Short["짧은 질문"]
        Q1["'What is Python?'"]
        A1["'Python is a<br/>programming language.'<br/><br/>len = 50"]
    end

    subgraph Long["긴 질문 (컨텍스트 추가)"]
        Q2["'What is Python?<br/>Explain in detail<br/>with history'"]
        A2["'Python is a programming<br/>language created by<br/>Guido van Rossum in 1991.<br/>It emphasizes...'<br/><br/>len = 200"]
    end

    Q1 -->|LLM with q| A1
    Q2 -->|LLM with q+context| A2

    A1 -.더 긴 응답.-> A2

    Property["Property:<br/>len(f(x + context)) > len(f(x))"]

    style Short fill:#ffe6cc
    style Long fill:#ccffff
    style Property fill:#fff9cc
```

##### 3. 부정 반전 (Negation Inversion)

```mermaid
graph LR
    subgraph Q1["질문 1"]
        Question1["'Is 5 even?'"]
        Answer1["False"]
    end

    subgraph Q2["질문 2 (부정)"]
        Question2["'Is 5 odd?'"]
        Answer2["True"]
    end

    Question1 -->|is_even 5| Answer1
    Question2 -->|is_odd 5| Answer2

    Answer1 -.반대.-> Answer2

    Property["Property:<br/>f(x) != f(negate(x))"]

    style Q1 fill:#ffcccc
    style Q2 fill:#ccffcc
    style Property fill:#fff9cc
```

#### 실전 적용: LLM 테스트

**시나리오**: AI 번역기 테스트
**문제**: 번역 결과가 매번 다를 수 있어 정확한 예상 출력 불가
**해결**: Metamorphic Relations 사용!

##### Relation 1: 역번역 일관성 (Back-translation Consistency)

```mermaid
graph TB
    Original["한글 원문:<br/>'안녕하세요'"]
    English["영어 번역:<br/>'Hello'"]
    BackToKorean["역번역 한글:<br/>'안녕하세요'<br/>(원문과 유사)"]

    Original -->|translate ko to en| English
    English -->|translate en to ko| BackToKorean

    BackToKorean -.의미 유사도 > 0.8.-> Original

    Property["Property:<br/>semantic_similarity(original, back_translated) > 0.8"]

    style Original fill:#e1f5ff
    style English fill:#ffe6cc
    style BackToKorean fill:#ccffcc
    style Property fill:#fff9cc
```

##### Relation 2: 패러프레이즈 일관성 (Paraphrase Consistency)

```mermaid
graph TB
    subgraph Inputs["유사한 의미의 입력"]
        In1["'How are you?'"]
        In2["'How's it going?'"]
    end

    subgraph Outputs["번역 출력"]
        Out1["'어떻게 지내세요?'"]
        Out2["'어떻게 지내?'"]
    end

    In1 -->|translate en to ko| Out1
    In2 -->|translate en to ko| Out2

    Out1 -.의미 유사도 > 0.7.-> Out2

    Property["Property:<br/>semantic_similarity(out1, out2) > 0.7"]

    style Inputs fill:#e1f5ff
    style Outputs fill:#ccffcc
    style Property fill:#fff9cc
```

---

### 3. Property-Based Testing (Hypothesis)

#### 작동 원리

```mermaid
graph TB
    subgraph Traditional["전통적 예제 기반 테스트"]
        T_Code["def test_add():<br/>  assert add(2, 3) == 5<br/>  assert add(0, 0) == 0<br/>  assert add(-1, 1) == 0"]
        T_Count["총 3개 케이스<br/>(개발자가 수작업)"]
        T_Problem["❌ 문제점:<br/>• 놓친 케이스?<br/>• 큰 숫자는?<br/>• 오버플로우는?"]

        T_Code --> T_Count --> T_Problem
    end

    subgraph PropertyBased["Property-Based 테스트 (Hypothesis)"]
        P_Code["@given(st.integers(), st.integers())<br/>def test_add_commutative(a, b):<br/>  assert add(a, b) == add(b, a)"]
        P_Property["교환법칙 (속성 정의)"]
        P_Auto["Hypothesis가 자동으로:<br/>• 100개+ (a,b) 조합 생성<br/>• 엣지 케이스 포함<br/>  (0, 음수, 큰 수, 경계값)<br/>• 실패 시 최소 반례 찾기<br/>• 이전 실패 재테스트"]
        P_Result["✅ 결과:<br/>• 3개 → 100개+ 자동<br/>• 속성만 정의,<br/>  입력은 AI 생성"]

        P_Code --> P_Property --> P_Auto --> P_Result
    end

    T_Problem -.해결.-> P_Code

    style Traditional fill:#ffcccc
    style PropertyBased fill:#ccffcc
    style T_Problem fill:#fff0f0
    style P_Result fill:#f0fff0
```

#### Hypothesis 실행 흐름

```mermaid
graph TB
    Step1["1️⃣ 속성 정의<br/><br/>@given(st.integers())<br/>def test_abs_non_negative(n):<br/>    assert abs(n) >= 0"]

    Step2["2️⃣ Hypothesis가 입력 생성 (자동)<br/><br/>Round 1: n = 0<br/>Round 2: n = 1<br/>Round 3: n = -1<br/>Round 4: n = 2147483647 (경계값)<br/>Round 5: n = -2147483648 (경계값)<br/>...<br/>Round 100: n = 42"]

    Step3["3️⃣ 실패 발견 시 자동 축소 (Shrinking)<br/><br/>실패: n = -2147483648<br/>↓<br/>Shrink 1: n = -1073741824<br/>↓<br/>Shrink 2: n = -536870912<br/>↓<br/>...<br/>↓<br/>최소 반례: n = -1"]

    Step4["4️⃣ 개발자에게 리포트<br/><br/>'Your property fails for n = -1'<br/><br/>→ 코드 수정 또는 속성 조정"]

    Step1 --> Step2 --> Step3 --> Step4

    Step4 -.수정 후 재실행.-> Step1

    style Step1 fill:#e1f5ff
    style Step2 fill:#ccffcc
    style Step3 fill:#ffe6cc
    style Step4 fill:#ffcccc
```

---

### 4. Self-Healing Tests

#### 문제: UI 변화로 인한 테스트 깨짐

```mermaid
graph TB
    subgraph Traditional["전통적 UI 테스트"]
        T_Code["button = driver.find_element<br/>(By.ID, 'submit-btn')<br/>button.click()"]
        T_Change["UI 변경:<br/>ID: 'submit-btn' → 'submit-button'"]
        T_Fail["❌ 테스트 실패<br/>❌ 수작업 수정 필요"]

        T_Code --> T_Change --> T_Fail
    end

    subgraph SelfHealing["Self-Healing 테스트 with AI"]
        S_Code["button = ai_find_element(<br/>  description='submit button',<br/>  fallback_locators=[<br/>    By.ID('submit-btn'),<br/>    By.CLASS('btn-primary'),<br/>    By.XPATH('//button[...]')<br/>  ])"]
        S_Process["AI가 자동으로:<br/>1. 첫 번째 locator 시도<br/>2. 실패 시 두 번째 시도<br/>3. 실패 시 세 번째 시도<br/>4. 모두 실패 시 화면 분석<br/>   (Vision AI)<br/>5. 'Submit' 텍스트 버튼 찾기"]
        S_Success["✅ ID 변경해도 통과<br/>✅ 유지보수 비용 감소"]

        S_Code --> S_Process --> S_Success
    end

    T_Fail -.해결.-> S_Code

    style Traditional fill:#ffcccc
    style SelfHealing fill:#ccffcc
    style T_Fail fill:#fff0f0
    style S_Success fill:#f0fff0
```

---

### 5. LLM-as-Judge

#### LLM으로 코드/테스트 품질 평가

```mermaid
graph TB
    Code["1️⃣ 코드 생성<br/><br/>def calculate_tax(income):<br/>  if income < 10000:<br/>    return income * 0.1<br/>  else:<br/>    return income * 0.2"]

    Prompt["2️⃣ LLM에게 평가 요청<br/><br/>Prompt: '다음 코드를 평가하세요:<br/>[코드 첨부]<br/><br/>평가 기준:<br/>1. 정확성<br/>2. 가독성<br/>3. 효율성<br/>4. 엣지 케이스<br/><br/>1-10점으로 평가하고 개선 제안'"]

    Response["3️⃣ LLM 응답<br/><br/>{<br/>  accuracy: 7,<br/>  readability: 8,<br/>  efficiency: 9,<br/>  edge_cases: 5,<br/>  overall: 7.25,<br/>  suggestions: [<br/>    '음수 income 처리 필요',<br/>    '경계값(10000) 명확화',<br/>    '상수를 변수로 추출'<br/>  ]<br/>}"]

    Decision{"4️⃣ 자동화된<br/>의사결정<br/><br/>overall_score?"}

    Reject["❌ Reject<br/>(score < 7.0)"]
    Improve["⚠️ Request<br/>Improvements<br/>(7.0 ≤ score < 8.5)"]
    Approve["✅ Approve<br/>(score ≥ 8.5)"]

    Code --> Prompt --> Response --> Decision
    Decision -->|"< 7.0"| Reject
    Decision -->|"7.0-8.5"| Improve
    Decision -->|">= 8.5"| Approve

    Reject -.재작성.-> Code
    Improve -.수정.-> Code

    style Code fill:#e1f5ff
    style Prompt fill:#ffe6cc
    style Response fill:#ccffff
    style Decision fill:#fff9cc
    style Reject fill:#ffcccc
    style Improve fill:#ffffcc
    style Approve fill:#ccffcc
```

---

## AI-DLC 테스트 실전 적용 가이드

### 단계별 도입 로드맵

```mermaid
graph TB
    Start([AI-DLC 테스트<br/>도입 시작])

    Phase1["📦 Phase 1: Property-Based 추가<br/>(1주)<br/><br/>• Hypothesis 설치<br/>• 주요 함수에 @given 테스트 추가<br/>• 기존 예제 기반 테스트 유지"]

    Phase2["🔄 Phase 2: Metamorphic Relations<br/>(2주)<br/><br/>• LLM 관련 기능에 적용<br/>• 5가지 핵심 Relations 구현<br/>• CI/CD 파이프라인 통합"]

    Phase3["⚖️ Phase 3: LLM-as-Judge<br/>(1주)<br/><br/>• 코드 리뷰 자동화<br/>• 테스트 품질 평가 자동화<br/>• 개발자 피드백 루프 구축"]

    Phase4["🔧 Phase 4: Self-Healing Tests<br/>(선택사항)<br/><br/>• UI 테스트에 AI locator 도입<br/>• Playwright/Selenium 통합<br/>• 유지보수 비용 감소 측정"]

    Complete([AI-DLC 테스트<br/>완전 도입])

    Start --> Phase1 --> Phase2 --> Phase3
    Phase3 --> Phase4 --> Complete
    Phase3 -.Phase 4 생략 가능.-> Complete

    style Start fill:#fff9cc
    style Phase1 fill:#e1f5ff
    style Phase2 fill:#ccffcc
    style Phase3 fill:#ffe6cc
    style Phase4 fill:#f0f0f0
    style Complete fill:#ccffcc
```

---

**다음 단계**: 각 테스트 기법의 실습 예제를 `examples/` 디렉토리에서 확인하세요!
