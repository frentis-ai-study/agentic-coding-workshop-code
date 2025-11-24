# Part 2: AI-DLC 개발

AI-DLC(AI-Driven Development Life Cycle) 방법론과 spec-kit/OpenSpec 도구를 활용한 체계적인 AI 기반 개발 워크플로우를 학습합니다.

## 학습 목표

이 파트를 완료하면 다음 능력을 갖추게 됩니다:

- ✅ AI-DLC 방법론의 핵심 개념 및 전통적 SDLC와의 차이점 이해
- ✅ spec-kit의 5단계 워크플로우 실행 및 활용
- ✅ OpenSpec의 3단계 워크플로우 실행 및 활용
- ✅ Claude Code 슬래시 명령어를 활용한 효율적인 개발
- ✅ 프로젝트 특성에 맞는 도구 및 워크플로우 선택 역량

## 예상 소요 시간

- **전체**: 2시간
- **이론 학습**: 30분
- **도구 설정 및 실습**: 1시간 30분

## 학습 순서

### 1단계: AI-DLC 개념 이해 (15분)

AI-DLC 방법론의 핵심 개념을 학습합니다.

📚 [AI-DLC 개요](./concepts/ai-dlc-overview.md)
- AI-DLC 정의 및 배경
- 전통적 SDLC vs AI-DLC
- 핵심 원칙 및 용어

### 2단계: 도구 비교 (15분)

spec-kit과 OpenSpec의 차이점을 이해하고, 프로젝트에 적합한 도구를 선택하는 기준을 학습합니다.

📚 [도구 비교: spec-kit vs OpenSpec](./concepts/tools-comparison.md)
- 각 도구의 특징 및 워크플로우
- 사용 시나리오별 추천
- 장단점 비교

### 3단계: spec-kit 실습 (30분)

spec-kit을 활용하여 TODO 앱 기능을 명세하고 구현합니다.

📚 [spec-kit 설치 및 설정](./tools/spec-kit/)
📚 [spec-kit 워크플로우 가이드](./tools/spec-kit/workflow-guide.md)
💻 [실습 1: TODO 앱 명세 작성](./practice/spec-kit-todo-app/)

### 4단계: OpenSpec 실습 (30분)

OpenSpec을 활용하여 계산기 기능을 개선하는 변경 제안을 작성하고 구현합니다.

📚 [OpenSpec 설치 및 설정](./tools/openspec/)
📚 [OpenSpec 워크플로우 가이드](./tools/openspec/workflow-guide.md)
💻 [실습 2: 계산기 히스토리 기능 추가](./practice/openspec-calculator/)

### 5단계: AI 코딩 어시스턴트 통합 (10분)

Claude Code 및 Cursor에서 spec-kit/OpenSpec을 효과적으로 활용하는 방법을 학습합니다.

📚 [Claude Code 슬래시 명령어 활용](./tools/claude-code-integration.md)
📚 [Cursor 커스텀 명령어 활용](./tools/cursor-integration.md)

## 폴더 구조

```
02-ai-dlc-development/
├── README.md                           # 👈 현재 문서
│
├── concepts/                           # 이론 자료
│   ├── ai-dlc-overview.md             # AI-DLC 방법론 개요
│   └── tools-comparison.md            # spec-kit vs OpenSpec 비교
│
├── tools/                              # 도구별 가이드
│   ├── spec-kit/
│   │   ├── README.md                  # 설치 및 설정
│   │   └── workflow-guide.md          # 5단계 워크플로우
│   ├── openspec/
│   │   ├── README.md                  # 설치 및 설정
│   │   └── workflow-guide.md          # 3단계 워크플로우
│   ├── claude-code-integration.md     # Claude Code 통합
│   └── cursor-integration.md          # Cursor 통합
│
├── practice/                           # 실습 예제
│   ├── spec-kit-todo-app/             # spec-kit 실습
│   │   ├── README.md
│   │   ├── instructions.md
│   │   └── examples/                  # 예시 산출물
│   └── openspec-calculator/           # OpenSpec 실습
│       ├── README.md
│       ├── instructions.md
│       └── examples/                  # 예시 산출물
│
└── troubleshooting.md                  # FAQ 및 문제 해결
```

## 선수 지식

- **필수**: Part 1 (Agentic AI 기초) 완료 권장
- **필수**: Python 기초 지식
- **필수**: CLI(터미널) 사용 경험
- **선택**: Git 기본 명령어

## 필수 도구

- **spec-kit**: `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`
- **OpenSpec**: `npm install -g @fission-ai/openspec@latest`
- **AI 코딩 어시스턴트**: Claude Code 또는 Cursor

## 학습 경로 옵션

### 경로 A: 순차 학습 (권장)
모든 내용을 체계적으로 학습합니다.
```
AI-DLC 개념 → 도구 비교 → spec-kit 실습 → OpenSpec 실습 → 통합
```
- **대상**: 처음 접하는 학습자
- **소요 시간**: 2시간

### 경로 B: 도구 중심 학습
특정 도구만 집중적으로 학습합니다.
```
AI-DLC 개념 (간략) → spec-kit 또는 OpenSpec 선택 → 심화 학습
```
- **대상**: 특정 도구만 배우고 싶은 학습자
- **소요 시간**: 1시간

### 경로 C: 비교 중심 학습
두 도구를 비교하며 학습합니다.
```
AI-DLC 개념 → 도구 비교 → spec-kit 실습 → OpenSpec 실습 → 비교 정리
```
- **대상**: 도구 선택을 고민하는 학습자
- **소요 시간**: 2.5시간

## 문제 해결

설치 및 사용 중 문제가 발생하면 [troubleshooting.md](./troubleshooting.md)를 참조하세요.

자주 발생하는 문제:
- spec-kit 설치 오류
- OpenSpec 초기화 오류
- Claude Code 슬래시 명령어 인식 안 됨
- Node.js 버전 호환성 문제

## 참고 자료

### 공식 문서
- [AWS AI-DLC 블로그](https://aws.amazon.com/blogs/devops/ai-driven-development-life-cycle/)
- [spec-kit GitHub](https://github.com/github/spec-kit)
- [OpenSpec GitHub](https://github.com/Fission-AI/OpenSpec)
- [Claude Code 문서](https://code.claude.com/docs/en/slash-commands)

### 추가 학습 자료
- [spec-kit vs OpenSpec 비교 글 (Hashrocket)](https://hashrocket.com/blog/posts/openspec-vs-spec-kit-choosing-the-right-ai-driven-development-workflow-for-your-team)
- [Cursor를 활용한 Spec-Driven Development](https://maddevs.io/writeups/project-creation-using-spec-kit-and-cursor/)
- [OpenSpec Cursor 통합 (Forum)](https://forum.cursor.com/t/openspec-lightweight-portable-spec-driven-framework-for-ai-coding-assistants/134052)

## 다음 단계

Part 2를 완료하면 [Part 3: MCP 툴 구현](../03-mcp-tools/)으로 진행하세요.

---

**업데이트**: 2025-11-22 | **버전**: 1.0
