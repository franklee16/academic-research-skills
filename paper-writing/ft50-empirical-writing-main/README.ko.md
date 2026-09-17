# FT50 실증 논문 학술 작성 스킬

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

OpenCode / Claude Code / Codex 등 AI 코딩 에이전트를 위한 FT50 실증 논문 작성 스킬입니다. 연구 질문 설정부터 이론 구축, 식별 전략, 실증 결과, 강건성 검증, 메커니즘 분석, 완전한 초고까지 전 과정을 다룹니다.

회계학, 재무학, 경영학, 마케팅, 운영·정보시스템, 경제학의 6개 분야에 걸친 FT50 전 50개 저널을 지원합니다.

## 기능

AI 에이전트가 FT50 실증 논문의 **0→초고 5단계 파이프라인**을 수행하도록 안내합니다:

| 단계 | 산출물 | 주요 결과물 |
|------|--------|------------|
| **1단계**: 연구 질문과 포지셔닝 | Gap table, 저널 추천, 기여陈述 | 어느 저널 + 무엇이 새로운가 |
| **2단계**: 이론과 가설 | 이론 프레임워크, 개념 모델, 검증 가능 가설 | §2 이론·가설 초고 |
| **3단계**: 식별 전략과 연구 설계 | DID/RDD/IV/RCT/Synthetic Control, 데이터 기술 | §3-4 연구 설계 초고 |
| **4단계**: 결과와 강건성 | 주요 결과, 강건성 피라미드, Oster bounds, 메커니즘 분석 | §5-6 결과·강건성 초고 |
| **5단계**: 집필과 조립 | Introduction, 문헌 검토, 논의, 시사점, Abstract | 완전한 초고 |

**도메인 특화**: 일반 작성 스킬이 다루지 않는 FT50 실증 연구 고유의 방법론 규범(식별 전략 설계, 강건성 피라미드, Oster bounds를 통한 관측 불가능 선택 편의 처리, 메커니즘 분석 프레임워크, 6개 분야별 심사자 기대치 등)을 내장하고 있습니다.

### 주요 기능

- **식별 전략**: DID(스태거드, 연속), RDD(샤프, 퍼지), IV(2SLS, Bartik, 시프트셰어), RCT, Synthetic Control, 이벤트 스터디
- **강건성 피라미드**: 계수 안정성 플롯, Oster bounds, 대체 모형 설정, 반증 검정, 표본 제한
- **메커니즘 분석**: 매개효과 vs. 조절효과, 횡단면 이질성, 구조적 추정
- **분야별 가이드**: 회계학(TAR, JAE, JAR, CAR, RAST), 재무학(JF, JFE, RFS, JFQA, RF), 경영학(AMJ, AMR, ASQ, OS, SMJ, JOM, JMS, JIBS), 마케팅(MktSci, JMR, JM, JCR), 운영·정보시스템(MS, OR, MSOM, ISR), 경제학(AER, ECMA, JPE, QJE, REStud)

---

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/liyuanbo1024/ft50-empirical-writing.git
```

### 2. AI 에이전트에 설치

| 에이전트 | 설치 명령어 |
|---------|------------|
| **OpenCode** | `cp -r ft50-empirical-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r ft50-empirical-writing ~/.claude/skills/` |
| **Codex** | `cp -r ft50-empirical-writing ~/.agents/skills/` |
| **Cursor** | `cp -r ft50-empirical-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r ft50-empirical-writing ~/.windsurf/skills/` |

설치 후 자연어로 스킬을 호출할 수 있습니다:

- `DID로 최저임금 고용 효과를 분석하는 논문을 쓰고 싶습니다. 포지셔닝을 도와주세요`
- `이론 프레임워크가 완성되었습니다. 스태거드 DID 식별 전략을 설계하고 Bacon 분해를 처리해 주세요`
- `FT50 실증 논문 작성 파이프라인 전체를 실행해 주세요`

---

## 사용법

### 파이프라인 모드

```
"FT50 실증 논문 작성 파이프라인을 실행해 주세요. 제 주제는…"
```

에이전트가 현재 단계를 평가하고 1단계부터 5단계까지 순차적으로 실행하며, 각 단계마다 확인을 요청합니다.

### 단계 건너뛰기

| 트리거 문구 | 이동 단계 |
|------------|----------|
| "연구 아이디어가 있습니다…" | 1단계: 포지셔닝 |
| "이론 프레임워크를 구축해 주세요" | 2단계: 이론과 가설 |
| "식별 전략을 설계해 주세요" | 3단계: 식별 전략 |
| "결과를 분석해 주세요 / 강건성 체크를 구축해 주세요" | 4단계: 결과와 강건성 |
| "완전한 논문을 작성해 주세요" | 5단계: 집필과 조립 |

### 참조 모드

```
"JF의 인과 식별에 대한 심사 기준은 무엇인가요?"
"Oster bounds를 어떻게 구현하여 관측 불가능 선택 편의를 처리하나요?"
"경영학 최상위 저널의 표준 메커니즘 분석 프레임워크는 무엇인가요?"
```

---

## 파일 구조

```
ft50-empirical-writing/
├── SKILL.md                              메인 스킬 파일
├── references/
│   ├── journal-characteristics.md        50개 FT50 저널 상세 프로필(분야별)
│   ├── identification-strategies.md      DID/RDD/IV/RCT/Synthetic Control/이벤트 스터디
│   ├── theory-hypothesis-guide.md        이론 프레임워크, 가설 구축, 개념 모델
│   ├── robustness-oster-guide.md         강건성 피라미드, Oster bounds, 반증 검정
│   ├── mechanism-analysis.md            매개, 조절, 이질성, 구조적 분석
│   ├── data-results-presentation.md      기술 통계, 결과 테이블, 시각화
│   ├── reviewer-expectations.md          분야별 FT50 심사자 기대치
│   └── writing-patterns.md              기출판 FT50 논문의 재사용 가능한 작성 패턴
├── assets/
│   └── regression-table-template.md      표준 회귀 테이블 규약
├── examples/
│   ├── manuscript_template.tex           저널 형식 LaTeX 템플릿
│   └── empirical_analysis.py            DID + Oster bounds 분석 템플릿
├── README.md / README.zh-CN.md / .ja.md / .ko.md
└── LICENSE
```

---

## 지원 저널

### 회계학

**TAR**, **JAE**, **JAR**, **CAR**, **RAST**

### 재무학

**JF**, **JFE**, **RFS**, **JFQA**, **RF**

### 경영학

**AMJ**, **AMR**, **ASQ**, **OS**, **SMJ**, **JOM**, **JMS**, **JIBS**

### 마케팅

**MktSci**, **JMR**, **JM**, **JCR**

### 운영·정보시스템

**MS**, **OR**, **MSOM**, **ISR**

### 경제학

**AER**, **ECMA**, **JPE**, **QJE**, **REStud**

---

## 사용자 정의

### 저널 추가

`references/journal-characteristics.md`를 편집하고 템플릿에 따라 새 저널 항목을 추가합니다.

### 실증 분석 기본값 조정

`examples/empirical_analysis.py`의 설정 매개변수를 수정합니다:

```python
@dataclass
class EmpiricalConfig:
    cluster_se: str = "state"   # 클러스터 표준 오차 수준
    fe_absorb: str = "firm"     # 고정 효과 흡수 변수
    oster_delta: float = 1.0    # Oster delta 매개변수
    # ...
```

---

## 라이선스

MIT License — [LICENSE](LICENSE) 참조.

---

## 감사의 글

[agentskills.io](https://agentskills.io) 명세와 [OpenCode](https://github.com/anomalyco/opencode)의 스킬 작성 방법론을 기반으로 합니다. FT50 도메인 지식은 Financial Times Top 50 저널의 편집 성명과 실증 경영 연구 커뮤니티의 방법론 가이드에 의존합니다.
