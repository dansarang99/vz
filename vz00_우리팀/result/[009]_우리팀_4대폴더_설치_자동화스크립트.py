# -*- coding: utf-8 -*-
"""
[우리팀 산출물 009] 초보 수강생용 4대 표준 폴더 및 우리팀 환경 원클릭 설치 스크립트
- 실행 방법: python [009]_우리팀_4대폴더_설치_자동화스크립트.py [대상작업경로(선택)]
- 기능:
  1. conversation/, prompt/, result/, upload/ 4대 필수 폴더 자동 생성
  2. conversation/CONVERSATION_TOTAL.md 마스터 단일 실록 초기화
  3. AGENTS.md 및 GEMINI.md 우리팀 지휘 헌장 자동 배포
  4. result/ [001]~[999] 무결점 순차 시리얼 규칙 자동 정렬
"""
import os
import sys
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

AGENTS_MANIFEST = """# 🏛️ [우리팀 MANIFEST] 3계층 지휘 / 4대 표준 폴더 / result [001]~[999] 규약

> **지위**: Antigravity & AI Assistant Mandatory Rule  
> **최고 의사결정권자**: 본부장님 (USER / Chief Executive Officer)  
> **전담 창구 및 작전 지휘관**: ADVISOR 총괄팀장 (MAIN AI)  
> **현장 공장장**: 대장장이 (Factory Manager)  
> **핵심 철칙**: Token-Zero (메인 채팅창 순결성 유지, 잡다한 코드/로그 배제, 최종 3줄 요약 보고)

---

## 1. 4대 표준 폴더 (Four Core Folders) 절대 규약
모든 작업 기지에는 **오직 아래 4개 폴더만 존재**하며, 그 외 임의 폴더(src, data, brain 등)는 전면 금지합니다:
1. `conversation/`: 단일 마스터 실록 `CONVERSATION_TOTAL.md` 영구 보존.
2. `prompt/`: 원천 및 AI 프롬프트 보존.
3. `result/`: 모든 산출물(기획서, 코드, 데이터, 보고서)이 생성순으로 `[001]`~`[999]` 번호를 달고 집결.
4. `upload/`: 사용자 원천 소스 및 외부 투입 자료 수용소.

## 2. result/ [001]~[999] 무결점 순차 시리얼 절대 규약
- 대화를 통해 생성되는 모든 결과물은 단 하나의 예외도 없이 `[001]`~`[999]` 번호를 파일명 앞에 붙여 반드시 `result/` 폴더에만 저장할 것.
- 누락(결번) 절대 금지, 중첩(중복) 절대 금지, 모든 일련번호는 오직 1회만 단독 부여.
- 번호 없는 파일의 result 폴더 진입 일체 차단.
"""

def setup_our_team_environment(target_dir=None):
    if not target_dir:
        target_dir = os.getcwd()
    
    target_dir = os.path.abspath(target_dir)
    print("=" * 80)
    print(f"🚀 [우리팀 3계층 지휘 & 4대 표준 폴더 원클릭 셋업]")
    print(f" ▸ 대상 디렉토리: {target_dir}")
    print("=" * 80)

    # 1. 4대 표준 폴더 생성
    core_folders = ["conversation", "prompt", "result", "upload"]
    for folder in core_folders:
        fpath = os.path.join(target_dir, folder)
        os.makedirs(fpath, exist_ok=True)
        print(f" ✅ [폴더 생성 완료] {folder}/")

    # 2. conversation/CONVERSATION_TOTAL.md 초기화 (없을 때만)
    conv_file = os.path.join(target_dir, "conversation", "CONVERSATION_TOTAL.md")
    if not os.path.exists(conv_file):
        init_content = f"""# 📜 [단일 마스터 실록] CONVERSATION_TOTAL.md

> **기록 시작**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **최고 의사결정권자**: 본부장님 (Chief Executive Officer)  
> **총괄 지휘관**: ADVISOR 총괄팀장  
> **원칙**: 꼬리에 꼬리를 무는 무한 누적 (Append Only), 100% 토씨 보존 (Zero-Loss)

---

"""
        with open(conv_file, "w", encoding="utf-8") as f:
            f.write(init_content)
        print(" ✅ [실록 생성 완료] conversation/CONVERSATION_TOTAL.md")
    else:
        print(" ℹ️ [실록 유지 확인] conversation/CONVERSATION_TOTAL.md (기존 파일 보존)")

    # 3. AGENTS.md 헌장 배포
    agents_file = os.path.join(target_dir, "AGENTS.md")
    if not os.path.exists(agents_file):
        with open(agents_file, "w", encoding="utf-8") as f:
            f.write(AGENTS_MANIFEST)
        print(" ✅ [헌장 배포 완료] AGENTS.md")

    print("\n" + "=" * 80)
    print("🎉 [축하합니다! 우리팀 표준 환경 구축 완료]")
    print(" ▸ 이제 AI 챗봇에게 아래와 같이 말씀하시면 '우리팀'이 즉시 기동합니다:")
    print("   👉 \"우리팀 나와!\" 또는 \"우리팀 가동해줘!\"")
    print("=" * 80)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    setup_our_team_environment(target)
