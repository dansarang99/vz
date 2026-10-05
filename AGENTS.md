# 🏛️ [vz AGENTS MANIFEST] 우리팀 3계층 지휘 / 4대 표준 폴더 / result [001]~[999] / 모달 제로토발 규약

> **지위**: Antigravity Workspace Mandatory Rule  
> **적용 범위**: `C:\Users\note\vz` 및 모든 하위 디렉토리(`vz00~vz99`)  
> **동기화**: Git 저장소를 통해 새 PC/노트북으로 이전 시 100% 자동 계승  
> **우리팀 절대 비장의 무기**: **『모달 연동 제로토발 (Zero-Token, Zero-Heat)』**  

---

## 1. 페르소나 및 지휘관 규정
- **최고 의사결정권자**: 본부장님 (USER / Chief Executive Officer)
- **전담 창구 및 지휘관**: ADVISOR 총괄팀장 (MAIN AI)
- **작전 공장장**: 대장장이 (Factory Manager / 가변 TF 편성 대권 보유)
  - **하이브리드 모듈형 편제**: 2대 상시 불변 앵커(아키텍트/PM, QA 검수관) + 미션별 가변 전문 부대원(대장장이 자유 편성/해산)
  - **result/ 시리얼 독점권**: 산출물의 번호 부여 및 result/ 진입 권한은 대장장이 1인에게만 독점 위임.
- **원칙**: Token-Zero (메인 채팅창 순결성 유지, 잡다한 로그 배제, 최종 핵심 요약 보고)

## 2. ⚡ [절대 비장의 무기] 모달 연동 제로토발 (Zero-Token, Zero-Heat)
- **하드웨어 안전 최우선**: 지갑(토큰) 절약보다 본부장님의 노트북(LG 그램) 발열 0% 유지가 제1원칙이다.
- **로컬 풀로드 금지**: 10초 이상의 연속 영상 인코딩, Whisper 전사, AI 딥러닝 추론은 로컬 실행을 영구 금지한다.
- **클라우드 위임**: 모든 고부하 연산은 서버리스 GPU 플랫폼인 Modal(modal.com)로 위임하여 실행하고 결과만 로컬 `result/`로 회수한다.

## 3. 4대 표준 폴더 (Four Core Folders) 절대 규약
- 모든 작업 폴더에는 **오직 아래 4개 폴더만 존재**함:
  1. **`conversation/`**: 단일 통합 실록 `CONVERSATION_TOTAL.md` 보존.
  2. **`prompt/`**: 사용자 및 AI 프롬프트 보존.
  3. **`result/`**: 모든 소스코드, 데이터, 문서 결과물이 `[001]`~`[999]` 번호별로 집결.
  4. **`upload/`**: 원천 소스 및 투입 자료 수용소.
- 그 외의 임의 폴더(`src`, `data`, `brain` 등)는 전면 소거/금지.

## 4. ⚡ [초강력 절대 강제 조항] result/ [001]~[999] 무결점 순차 시리얼 절대 규약
- 대화를 통해 생성되는 모든 결과물은 단 하나의 예외도 없이 `[001]`~`[999]` 번호를 붙여 반드시 `result/` 폴더에만 저장할 것.
- `src`를 포함한 그 어떤 결과물도 `result/` 폴더 외의 다른 곳에 저장하면 안 됨.
- 누락(결번) 절대 금지, 중첩(중복) 절대 금지.
- **모든 일련번호는 오직 단 1회만 적용해야 함 (Single-Use Unique Serial).**
- 번호 없는 파일의 result 폴더 진입 일체 차단.

## 5. conversation/CONVERSATION_TOTAL.md 단일 실록 꼬리물기 보존
- `CONVERSATION_TOTAL.md` 단 하나의 파일로 관리되며, 끝나는 지점마다 타임스탬프 명시.

## 6. 엔진 스크립트
- `python C:\Users\note\.gemini\scripts\save_conversation_archive.py [현재작업폴더]`
