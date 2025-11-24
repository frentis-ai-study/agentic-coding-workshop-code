# CI/CD 파이프라인

GitHub Actions를 사용한 자동 테스트 및 빌드 파이프라인입니다.

## 개요

### 무엇을 하나요?

**코드를 푸시하면 자동으로 테스트, 린트, 빌드를 실행**하는 파이프라인을 만듭니다.

```mermaid
flowchart TD
    Start[개발자: git push] --> Trigger[GitHub Actions<br/>자동 트리거]

    Trigger --> Test[테스트 실행<br/>test.yml]
    Trigger --> Lint[코드 품질 검사<br/>lint.yml]
    Trigger --> Docker[Docker 빌드<br/>docker-build.yml]

    Test --> Check{모든 체크<br/>통과?}
    Lint --> Check
    Docker --> Check

    Check -->|✅ Yes| Deploy[배포 준비 완료<br/>PR 머지 가능]
    Check -->|❌ No| Block[머지 차단<br/>수정 필요]

    style Start fill:#e1f5ff
    style Trigger fill:#fff4e1
    style Test fill:#ccffcc
    style Lint fill:#ffffcc
    style Docker fill:#ffe1f5
    style Deploy fill:#ccffcc
    style Block fill:#ffcccc
```

### 왜 CI/CD가 필요한가요?

| 문제 (수동 작업) | 해결 (CI/CD 자동화) |
|------------------|---------------------|
| ❌ 테스트 깜빡하고 안 돌림 | ✅ 푸시할 때마다 자동 실행 |
| ❌ Python 버전별 테스트 번거로움 | ✅ 매트릭스로 3.12, 3.13 동시 테스트 |
| ❌ 코드 스타일 불일치 | ✅ ruff, mypy 자동 검사 |
| ❌ Docker 이미지 수동 빌드 | ✅ 자동 빌드 및 태깅 |
| ❌ 버그가 프로덕션에 배포됨 | ✅ 테스트 실패 시 머지 차단 |

### 만드는 것

**3개의 GitHub Actions 워크플로우**

```mermaid
graph LR
    Push[git push] --> Test[test.yml<br/>자동 테스트]
    Push --> Lint[lint.yml<br/>코드 품질]
    Push --> Docker[docker-build.yml<br/>이미지 빌드]

    Test --> Badge1[✅ Tests Passed]
    Lint --> Badge2[✅ Lint Passed]
    Docker --> Badge3[✅ Build Passed]

    Badge1 --> Merge{PR 머지 가능?}
    Badge2 --> Merge
    Badge3 --> Merge

    Merge -->|모두 통과| Deploy[배포 진행]
    Merge -->|하나라도 실패| Block[머지 차단]

    style Push fill:#e1f5ff
    style Test fill:#ccffcc
    style Lint fill:#ffffcc
    style Docker fill:#ffe1f5
    style Deploy fill:#ccffcc
    style Block fill:#ffcccc
```

### 워크플로우 구성

| 워크플로우 | 파일 | 실행 조건 | 역할 |
|-----------|------|----------|------|
| **테스트** | `.github/workflows/test.yml` | PR, push to main | pytest, 커버리지 |
| **린트** | `.github/workflows/lint.yml` | PR, push to main | ruff, mypy |
| **Docker 빌드** | `.github/workflows/docker-build.yml` | PR, push to main | 이미지 빌드 |

### 실행 흐름 예시

```
1. 개발자: git push origin feature/add-calculator
   ↓
2. GitHub Actions 트리거
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   병렬 실행 (3개 워크플로우)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   [test.yml]
   - Python 3.12 환경 설정
   - Python 3.13 환경 설정
   - uv sync 의존성 설치
   - pytest 실행
   - 커버리지 리포트 생성

   [lint.yml]
   - ruff check (린트)
   - ruff format --check (포맷)
   - mypy (타입 체크)

   [docker-build.yml]
   - Dockerfile.chat 빌드
   - docker-compose up --build
   - 헬스체크

   ↓
3. 결과 확인
   - ✅ 모든 체크 통과 → PR 머지 가능
   - ❌ 하나라도 실패 → PR 머지 차단
```

### GitHub Actions 뱃지

README에 추가할 수 있는 상태 뱃지:

```markdown
![Tests](https://github.com/사용자명/저장소명/workflows/test.yml/badge.svg)
![Lint](https://github.com/사용자명/저장소명/workflows/lint.yml/badge.svg)
![Docker](https://github.com/사용자명/저장소명/workflows/docker-build.yml/badge.svg)
```

---

## CI/CD 파이프라인 개요

### 전체 워크플로우

```mermaid
graph TB
    subgraph Developer["개발자 워크플로우"]
        Code["💻 코드 작성"]
        LocalTest["🧪 로컬 테스트<br/>uv run pytest"]
        Commit["📝 Git 커밋"]
        Push["⬆️ Git 푸시"]

        Code --> LocalTest
        LocalTest --> Commit
        Commit --> Push
    end

    subgraph GitHubActions["GitHub Actions (자동 실행)"]
        Trigger{이벤트 트리거}

        subgraph TestWorkflow["test.yml"]
            T1["Python 3.12, 3.13<br/>매트릭스 설정"]
            T2["의존성 설치<br/>(uv sync)"]
            T3["pytest 실행"]
            T4["커버리지 리포트"]

            T1 --> T2 --> T3 --> T4
        end

        subgraph LintWorkflow["lint.yml"]
            L1["ruff check<br/>(린트)"]
            L2["ruff format --check<br/>(포맷 검사)"]
            L3["mypy<br/>(타입 체크)"]

            L1 --> L2 --> L3
        end

        subgraph DockerWorkflow["docker-build.yml"]
            D1["MCP 서버<br/>이미지 빌드"]
            D2["채팅 앱<br/>이미지 빌드"]
            D3["Docker Compose<br/>스택 테스트"]

            D1 --> D3
            D2 --> D3
        end

        Trigger -->|PR 생성| TestWorkflow
        Trigger -->|PR 생성| LintWorkflow
        Trigger -->|main 푸시| DockerWorkflow
    end

    subgraph Results["결과 확인"]
        Success["✅ 모든 체크 통과"]
        Fail["❌ 실패<br/>PR 병합 차단"]
        Merge["🔀 PR 병합"]

        Success --> Merge
    end

    Push --> Trigger
    TestWorkflow --> Success
    LintWorkflow --> Success
    TestWorkflow -.실패.-> Fail
    LintWorkflow -.실패.-> Fail

    style Developer fill:#e1f5ff
    style GitHubActions fill:#f0f0f0
    style TestWorkflow fill:#ccffcc
    style LintWorkflow fill:#ffffcc
    style DockerWorkflow fill:#ffccff
    style Results fill:#ffe6cc
```

### 각 워크플로우 상세

```mermaid
sequenceDiagram
    actor Dev as 개발자
    participant GH as GitHub
    participant Actions as GitHub Actions
    participant Cache as 캐시 저장소

    Dev->>GH: git push origin feature-branch
    GH->>Actions: 워크플로우 트리거

    Note over Actions: test.yml 실행

    Actions->>Cache: uv 캐시 확인
    alt 캐시 있음
        Cache-->>Actions: 캐시된 의존성 복원
    else 캐시 없음
        Actions->>Actions: uv sync 실행
        Actions->>Cache: 캐시 저장
    end

    Actions->>Actions: pytest 실행 (Python 3.12)
    Actions->>Actions: pytest 실행 (Python 3.13)

    alt 테스트 통과
        Actions-->>GH: ✅ 체크 통과
    else 테스트 실패
        Actions-->>GH: ❌ 체크 실패
        GH-->>Dev: 🚨 실패 알림
    end

    Note over Actions: lint.yml 실행

    Actions->>Actions: ruff check
    Actions->>Actions: ruff format --check
    Actions->>Actions: mypy

    alt 린트 통과
        Actions-->>GH: ✅ 체크 통과
    else 린트 실패
        Actions-->>GH: ❌ 체크 실패
        GH-->>Dev: 🚨 실패 알림
    end

    Note over Dev,GH: 모든 체크 통과 시 PR 병합 가능
```

---

## 워크플로우

### 1. test.yml - 자동 테스트
```yaml
# PR 및 main push 시 자동 실행
- pytest 테스트
- Python 3.12, 3.13 매트릭스
- 커버리지 리포트
```

### 2. lint.yml - 코드 품질
```yaml
# PR 시 자동 실행
- ruff 린트
- ruff 포맷 검사
- mypy 타입 체크
```

### 3. docker-build.yml - Docker 이미지
```yaml
# main push 시 실행
- 채팅 앱 이미지 빌드
- 태그 생성
- (선택사항) 레지스트리 푸시
```

## 로컬 테스트

GitHub Actions 실행 전 로컬에서 테스트:

```bash
# pytest
uv run pytest 04-testing-deployment -v

# ruff
uv run ruff check .
uv run ruff format --check .

# mypy
uv run mypy 04-testing-deployment

# Docker 빌드
cd 04-testing-deployment/03-docker-deployment
docker-compose build
```

## 워크플로우 파일 위치

```
.github/workflows/
├── test.yml          # 자동 테스트
├── lint.yml          # 린트 및 타입 체크
└── docker-build.yml  # Docker 이미지 빌드
```

## 실행 결과 확인

GitHub 리포지토리의 "Actions" 탭에서 확인:
- https://github.com/your-username/your-repo/actions

## 참고

- [GitHub Actions 문서](https://docs.github.com/actions)
- [uv in CI](https://docs.astral.sh/uv/guides/integration/github/)
