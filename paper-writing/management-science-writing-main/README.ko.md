# 경영과학 학술 논문 작성 스킬

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

OpenCode / Claude Code / Codex 등 AI 코딩 에이전트를 위한 경영과학(MS&E) 학술 논문 작성 스킬입니다. 주제 선정부터 모델링, 도출, 수치 실험, 완전한 초고까지 전 과정을 다룹니다.

UTD-24 최상위 저널 **MS, OR, MSOM, POM**을 비롯해 **TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE**까지 총 13개 저널을 지원합니다.

## 기능

AI 에이전트가 MS&E 논문의 **0→초고 5단계 파이프라인**을 수행하도록 안내합니다:

| 단계 | 산출물 | 주요 결과물 |
|------|--------|-----------|
| **1단계**: 주제 선정 | Gap table, 저널 추천, 기여陈述 | 어느 저널 + 무엇이 새로운가 |
| **2단계**: 모델 구축 | 표기 체계, 가정 프레임워크, 수식 | §3 모델 섹션 초고 |
| **3단계**: 도출 및 분석 | Lemma→Theorem→Corollary 증명 체인 | §4 분석 섹션 초고 |
| **4단계**: 수치 실험 | 파라미터 보정, 민감도 분석, 반사실 | §5-6 실험 섹션 초고 |
| **5단계**: 집필 및 조립 | Introduction, 문헌 검토, 경영적 시사점, Abstract | 완전한 초고 |

**도메인 특화**: 일반写作 스킬이 다루지 않는 MS&E 저널 고유의 관행(모델 제시 구조, 증명 위계, SAR 형식의 경영적 시사점, 심사자 기대치 등)을 내장하고 있습니다.

---

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/liyuanbo1024/management-science-writing.git
```

### 2. AI 에이전트에 설치

| 에이전트 | 설치 명령어 |
|---------|-----------|
| **OpenCode** | `cp -r management-science-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r management-science-writing ~/.claude/skills/` |
| **Codex** | `cp -r management-science-writing ~/.agents/skills/` |
| **Cursor** | `cp -r management-science-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r management-science-writing ~/.windsurf/skills/` |

설치 후 자연어로 스킬을 호출할 수 있습니다:
- `MSOM에 동적 가격 책정 논문을 쓰고 싶습니다. 포지셔닝을 도와주세요`
- `모델이 완성되었습니다. 구조적 성질을 도출해 주세요`
- `경영과학 논문 작성 파이프라인 전체를 실행해 주세요`

---

## 사용법

### 파이프라인 모드

```
"MS&E 논문 작성 파이프라인을 실행해 주세요. 제 주제는…"
```

에이전트가 현재 단계를 평가하고 1단계부터 5단계까지 순차적으로 실행하며, 각 단계마다 확인을 요청합니다.

### 단계 건너뛰기

| 트리거 문구 | 이동 단계 |
|-----------|---------|
| "연구 아이디어가 있습니다…" | 1단계: 주제 선정 |
| "수리 모델을 설계해 주세요" | 2단계: 모델 구축 |
| "도출/증명해 주세요…" | 3단계: 도출 및 분석 |
| "수치 실험을 설계해 주세요" | 4단계: 수치 실험 |
| "완전한 논문을 작성해 주세요" | 5단계: 집필 및 조립 |

### 참조 모드

```
"MS 저널의 증명 완전성 심사 기준은 무엇인가요?"
"EJOR의 경영적 시사점은 어떻게 구성해야 하나요?"
```

---

## 지원 저널

### Tier 1 (UTD-24)
**Management Science (MS)**, **Operations Research (OR)**, **M&SOM (MSOM)**, **Production & Oper. Mgmt (POM)**

### Tier 2 (분야 저널)
**TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE**

---

## 파일 구조

```
management-science-writing/
├── SKILL.md                              메인 스킬 파일
├── references/                           8개 참조 파일
├── assets/                               정리 구조 참조
├── examples/                             LaTeX 템플릿 + Python 실험
├── README.md / README.zh-CN.md / .ja.md / .ko.md
└── LICENSE
```

---

## 라이선스

MIT License — [LICENSE](LICENSE) 참조.

---

## 감사의 글

[agentskills.io](https://agentskills.io) 명세와 [OpenCode](https://github.com/anomalyco/opencode)의 스킬 작성 방법론을 기반으로 합니다. MS&E 도메인 지식은 INFORMS 저널 편집 성명과 OR 커뮤니티의 출판 스타일 가이드에 의존합니다.
