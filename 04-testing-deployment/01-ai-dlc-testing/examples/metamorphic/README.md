# Metamorphic Testing for LLM Applications

**Metamorphic Testing**은 LLM이 생성한 코드와 출력의 일관성을 검증하는 테스트 기법입니다. 전통적인 테스트처럼 정확한 예상 출력을 지정하는 대신, **입력 변환 시 출력 간의 관계(Metamorphic Relation)**를 검증합니다.

## 왜 Metamorphic Testing인가?

LLM 생성 코드는 다음과 같은 특성 때문에 전통적인 테스트가 어렵습니다:

1. **비결정적 출력**: 같은 입력도 매번 다른 출력 생성
2. **정확한 출력 예측 불가**: 창의적인 답변, 요약, 번역 등
3. **테스트 오라클 부재**: 무엇이 "정답"인지 정의하기 어려움

Metamorphic Testing은 이러한 문제를 해결하기 위해 **불변 속성(invariant properties)**을 검증합니다.

## 핵심 개념

### Metamorphic Relation (MR)

입력을 변환했을 때, 원본 출력과 변환된 출력 간에 성립해야 하는 관계입니다.

**예시:**
- **순열 불변성**: "1 + 2 + 3" → "3 + 2 + 1" (덧셈은 순서 무관)
- **패러프레이즈 일관성**: "날씨 어때?" ≈ "오늘 날씨는?" (의미 유사)
- **가산 단조성**: "파이썬이란?" → "파이썬이란? 자세히 설명해줘" (출력이 더 상세)

## 구현된 Metamorphic Relations

### 1. PermutationInvariance (순열 불변성)

**정의**: 입력 순서를 바꿔도 결과가 동일해야 합니다.

**적용 예시:**
- 교환법칙이 성립하는 연산 (덧셈, 곱셈)
- 정렬된 리스트 (순서 무관)
- 집합 연산 (합집합, 교집합)

```python
from metamorphic_relations import PermutationInvariance

relation = PermutationInvariance()

# 입력 변환
original = "1 + 2 + 3"
transformed = "3 + 2 + 1"

# 출력 검증
assert calculator(original) == calculator(transformed)  # 둘 다 6
```

**실전 활용:**
- API 파라미터 순서 변경 시 동일한 결과 확인
- 데이터베이스 쿼리 조건 순서 변경 테스트

---

### 2. ParaphraseConsistency (패러프레이즈 일관성)

**정의**: 의미가 같은 입력은 유사한 출력을 생성해야 합니다.

**적용 예시:**
- 자연어 질의응답 시스템
- 명령어 인식 (음성 비서)
- 텍스트 분류 (감정 분석)

```python
from metamorphic_relations import ParaphraseConsistency

relation = ParaphraseConsistency()

original = "계산해줘: 5 + 5"
paraphrased = "계산하세요: 5 + 5"

# 출력이 유사해야 함 (완전 동일하거나 의미적으로 유사)
assert relation.verify_outputs(
    calculator(original),
    calculator(paraphrased)
)
```

**실전 활용:**
- LLM 기반 챗봇의 답변 일관성 검증
- 다국어 번역 결과 비교

---

### 3. AdditiveMonotonicity (가산 단조성)

**정의**: 추가 정보를 제공하면 출력이 더 상세해져야 합니다.

**적용 예시:**
- RAG 시스템 (컨텍스트 추가 시 답변 개선)
- 검색 엔진 (쿼리에 필터 추가)
- 요약 시스템 (길이 제약 완화)

```python
from metamorphic_relations import AdditiveMonotonicity

relation = AdditiveMonotonicity(additional_context="더 자세히 설명해줘")

original_input = "파이썬이란?"
detailed_input = relation.transform_input(original_input)

original_output = llm_query(original_input)
detailed_output = llm_query(detailed_input)

# 상세한 답변이 더 길어야 함
assert len(detailed_output) > len(original_output)
```

**실전 활용:**
- 프롬프트 엔지니어링 효과 측정
- 컨텍스트 윈도우 최적화

---

### 4. NegationInversion (부정 반전)

**정의**: 질문을 부정형으로 바꾸면 답변도 반대가 되어야 합니다.

**적용 예시:**
- 불린 질의응답 (예/아니오)
- 분류 모델 (긍정/부정)
- 논리 추론 시스템

```python
from metamorphic_relations import NegationInversion

relation = NegationInversion()

original = "5는 짝수인가?"
negated = relation.transform_input(original)  # "5는 홀수인가?"

assert is_even_checker(original) != is_even_checker(negated)  # False vs True
```

**실전 활용:**
- 감정 분석 모델 검증 (긍정 ↔ 부정)
- 팩트 체킹 시스템

---

### 5. EquivalenceRelation (동등성 관계)

**정의**: 동일한 의미의 입력은 동일한 출력을 생성해야 합니다.

**적용 예시:**
- 수학 연산 (교환법칙, 결합법칙)
- 동의어 처리
- 정규화된 입력

```python
from metamorphic_relations import EquivalenceRelation

relation = EquivalenceRelation(equivalent_input="3 * 5")

original_output = calculator("5 * 3")
equivalent_output = calculator("3 * 5")

assert relation.verify_outputs(original_output, equivalent_output)  # 둘 다 15
```

**실전 활용:**
- MCP 도구의 교환법칙 검증
- API 호출 순서 독립성 확인

---

## 실행 방법

### 1. 전체 테스트 실행

```bash
cd 04-testing-deployment/01-ai-dlc-testing/examples/metamorphic
uv run pytest test_llm_output.py -v
```

**예상 출력:**
```
test_llm_output.py::test_permutation_invariance_addition PASSED
test_llm_output.py::test_paraphrase_consistency PASSED
test_llm_output.py::test_additive_monotonicity PASSED
test_llm_output.py::test_negation_inversion_even_odd PASSED
test_llm_output.py::test_equivalence_relation_commutativity PASSED
test_llm_output.py::test_permutation_invariance_with_lists PASSED
test_llm_output.py::test_mcp_tool_metamorphic_consistency PASSED
```

### 2. 개별 테스트 실행

```bash
# 순열 불변성 테스트만
uv run pytest test_llm_output.py::test_permutation_invariance_addition -v

# 부정 반전 테스트만
uv run pytest test_llm_output.py::test_negation_inversion_even_odd -v
```

### 3. 스크립트로 실행

```bash
uv run python test_llm_output.py
```

---

## 실전 적용: MCP 서버 테스트

### Part 3 MCP 계산기 도구 검증

```python
import pytest
from fastmcp import FastMCP

# MCP 서버 초기화
mcp = FastMCP("calculator")

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """두 숫자를 곱합니다."""
    return a * b

def test_mcp_calculator_commutativity():
    """교환법칙 검증: a * b == b * a"""
    from metamorphic_relations import EquivalenceRelation

    relation = EquivalenceRelation(equivalent_input=(5, 3))

    result1 = multiply(3, 5)
    result2 = multiply(5, 3)

    assert relation.verify_outputs(result1, result2)
```

### LLM 기반 MCP 도구 검증

```python
@mcp.tool()
async def summarize_text(text: str, max_length: int = 100) -> str:
    """텍스트를 요약합니다."""
    # LLM 호출 (예: OpenAI API)
    response = await llm.summarize(text, max_length)
    return response

def test_summarize_additive_monotonicity():
    """가산 단조성: max_length가 클수록 요약이 더 상세함"""
    from metamorphic_relations import AdditiveMonotonicity

    text = "긴 문서 내용..."

    short_summary = await summarize_text(text, max_length=50)
    long_summary = await summarize_text(text, max_length=200)

    # 더 긴 max_length는 더 상세한 요약 생성
    assert len(long_summary) >= len(short_summary)
```

---

## 고급 기법

### 1. 의미적 유사도 검증

단순 문자열 비교 대신 임베딩 기반 유사도를 사용할 수 있습니다:

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(text1: str, text2: str) -> float:
    """두 텍스트의 의미적 유사도 계산 (0~1)."""
    embeddings = model.encode([text1, text2])
    similarity = util.cos_sim(embeddings[0], embeddings[1])
    return float(similarity[0][0])

# ParaphraseConsistency 검증 시 사용
assert semantic_similarity(original_output, paraphrased_output) > 0.8
```

### 2. LLM-as-Judge 결합

Metamorphic Relation을 LLM으로 검증:

```python
async def llm_verify_consistency(output1: str, output2: str) -> bool:
    """LLM에게 두 출력이 일관성 있는지 판단 요청."""
    prompt = f"""
    다음 두 답변이 의미적으로 일관성이 있는지 판단하세요:

    답변 1: {output1}
    답변 2: {output2}

    일관성이 있으면 'YES', 없으면 'NO'로만 답변하세요.
    """
    response = await llm.query(prompt)
    return "YES" in response.upper()
```

---

## 모범 사례

### ✅ DO

- **복수의 MR 적용**: 하나의 함수에 여러 Metamorphic Relation 테스트
- **자동화**: CI/CD 파이프라인에 통합
- **MR 문서화**: 각 테스트가 검증하는 속성을 명확히 기록
- **실패 원인 분석**: MR 위배 시 코드 로직 재검토

### ❌ DON'T

- **과도한 제약**: 너무 엄격한 MR은 합법적인 변동을 막음
- **MR 남용**: 모든 테스트를 MR로 대체하지 말 것 (단위 테스트도 필요)
- **무의미한 변환**: 출력에 영향을 주지 않는 입력 변환은 의미 없음

---

## 참고 자료

### 학술 논문
- [Metamorphic Testing for LLMs (2024)](https://arxiv.org/abs/2406.06864)
- [Testing Machine Learning Systems (Google Research)](https://research.google/pubs/pub49555/)

### 실전 가이드
- [LLM Testing Methods (Confident AI)](https://www.confident-ai.com/blog/llm-testing-in-2024-top-methods-and-strategies)
- [AI-Powered Testing (AWS)](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)

---

## 다음 단계

Metamorphic Testing을 마스터했다면:

1. **Property-Based Testing**: Hypothesis로 자동 입력 생성
2. **Self-Healing Tests**: UI 변화에 자동 적응
3. **LLM-as-Judge**: AI로 테스트 결과 평가

📁 **[Property-Based Testing 예제 →](../property-based/)**
