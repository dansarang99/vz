# 🏛️ [vz00] 우리팀(AX-TWIN) 운영 체계 마스터 가이드

> **"혼자 일하지 말고, AI 군단을 지휘하라."**  
> 본 저장소는 1인 창업가, AX 창업지도사, 실무 기획자가 AI를 단순 챗봇이 아닌 **'자립형 3계층 전문 조직'**으로 편제하여 대규모 프로젝트를 완전 무결하게 완수하도록 돕는 마스터 오케스트레이션 시스템입니다.

---

## 📌 목차 (Table of Contents)

1. [시스템 개요 (Overview)](#시스템-개요)
2. [3계층 지휘 구조도 (Three-Tier Hierarchy)](#3계층-지휘-구조도)
3. [토큰 제로(Token-Zero) 운영 원칙](#토큰-제로-운영-원칙)
4. [수강생 전수 가이드 (Curriculum)](#수강생-전수-가이드)
5. [폴더 및 참조 문서 안내](#폴더-및-참조-문서-안내)
6. [원클릭 스킬 등록 및 사용법](#원클릭-스킬-등록-및-사용법)

---

## 1. 시스템 개요

일반적인 사용자는 AI에게 질문하고 답변을 받는 **"1:1 대화식(Ping-Pong)"**으로 작업합니다.  
이 방식은 기획서가 커지거나, 코드가 길어지거나, 영상 대본처럼 다차원적인 산출물이 필요할 때 다음 세 가지 문제로 반드시 붕괴합니다:

- **컨텍스트 오염 (Context Pollution):** 메인 창이 지저분해지며 AI가 이전 지시를 잊어버림.
- **토큰 과다 소모 (Token Exhaustion):** 불필요한 로그와 대화로 API 비용 및 토큰 한도가 급속 소모됨.
- **결과물 파편화:** 매번 결과 양식이 달라지고 검수가 불가능함.

**[vz00 우리팀 시스템]**은 이 문제를 군대식 지휘 계통과 공장 분업화(Factory Line) 모델로 완벽히 해결합니다.

---

## 2. 3계층 지휘 구조도

```
👑 [Tier 1] 본부장 (사용자 / CEO)
       │  "전략 목표 하명 & 최종 승인"
       ▼
🗣️ [Tier 2] ADVISOR 총괄팀장 (메인 에이전트)
       │  "지휘 통제 & 본부장 전담 3줄 브리핑"
       ▼
🔨 [Tier 3-A] 대장장이 (공장장 / Factory Manager)
       │  "토큰 제로 무한 연마 & 공정 총괄"
       ▼
🏭 [Tier 3-B] AX-TWIN 전문 부대원 (Specialized Agents)
       ├─ PM (공정 관리)
       ├─ 아키텍트 (구조 설계)
       ├─ 프로그래머 (스크립트/코드 빌드)
       ├─ DB 엔지니어 (데이터 정제/무결성)
       ├─ 카피라이터 (5대 마스터 대본 집필)
       ├─ 리딩/풀링 AGENT (기획안 무손실 해독)
       ├─ 수학/기하학 연산자 (시간축·초단위 정밀 캘리브레이션)
       └─ QA 검수관 (0-Error 품질 통과 검증)
```

---

## 3. 토큰 제로(Token-Zero) 운영 원칙

- **대화창에서는 지시와 브리핑만:** 본부장의 메인 화면은 항상 깨끗해야 합니다.
- **실무는 방을 따로 파서 수행:** 대장장이와 부대원들은 백그라운드(`invoke_subagent` 또는 로컬 스크립트)에서 동작합니다.
- **데이터 전달은 채팅이 아닌 파일로:** 에이전트끼리 대화로 텍스트를 주고받지 않고, `result/` 폴더 내 JSON, Markdown, HTML 파일을 직접 읽고 씁니다.
- **영구 보존:** 모든 산출물은 `result/[001]_파일명` 형식으로 시리얼 번호를 매겨 영구 보존됩니다.

---

## 4. 수강생 전수 가이드 (Curriculum)

AX 창업지도사 과정 수강생들에게 전수할 때는 다음 5단계 실습을 진행합니다:

1. **[마인드셋 전환]** "나는 코딩하는 사람이 아니라, AI 팀을 지휘하는 사장이다."
2. **[팀 세팅]** `.gemini/config/skills/`에 `vz00-our-team` 스킬 등록하기
3. **[첫 소집]** 채팅창에 `"우리팀 모두 나와."` 입력 후 전 부대원 도열 확인하기
4. **[작전 하달]** 기획안 1장을 던지고 `"5단 시나리오 5대 대본 작성해."` 명령하기
5. **[최종 검수]** 총괄팀장의 3줄 보고를 받고 `result/`에 생성된 파일 검수 및 승인하기

---

## 5. 폴더 및 참조 문서 안내

- 📄 [`SKILL.md`](./SKILL.md) : Antigravity 및 AI 시스템에 직접 탑재되는 실행 스킬 명세
- 📚 [`references/01_THREE_TIER_ARCHITECTURE.md`](./references/01_THREE_TIER_ARCHITECTURE.md) : 3계층 지휘 체계 심층 해설
- 📚 [`references/02_TOKEN_ZERO_PROTOCOL.md`](./references/02_TOKEN_ZERO_PROTOCOL.md) : 토큰 제로 원리와 파일 기반 파이프라인
- 📚 [`references/03_AX_TWIN_SUBAGENTS_ROSTER.md`](./references/03_AX_TWIN_SUBAGENTS_ROSTER.md) : 각 서브에이전트별 R&R 및 시스템 프롬프트
- 📚 [`references/04_STUDENT_TRAINING_WORKBOOK.md`](./references/04_STUDENT_TRAINING_WORKBOOK.md) : 수강생 실습 교재 (핸즈온 워크북)
- 📚 [`references/05_COMMAND_CHEATSHEET.md`](./references/05_COMMAND_CHEATSHEET.md) : 사장님 전용 10대 지휘 명령어 모음
- 📋 [`templates/skill_template_our_team.md`](./templates/skill_template_our_team.md) : 수강생 프로젝트 복제용 빈 스킬 템플릿
- 📁 `result/` : 작전 수행 결과물 영구 보존 디렉토리
- 📁 `upload/` : 기획안, 레퍼런스 원천 데이터 적재 디렉토리
