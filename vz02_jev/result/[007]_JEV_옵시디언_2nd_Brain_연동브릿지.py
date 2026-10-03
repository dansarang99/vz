# -*- coding: utf-8 -*-
r"""
[OBSIDIAN 2ND BRAIN BRIDGE] JEV 엔진과 옵시디언 관제탑 간의 실시간 동기화 브릿지
- JEV의 의사결정 결과를 옵시디언 볼트(C:\Users\note\vz)에 마크다운으로 즉시 기록
- 000_관제탑 및 02_Projects/vz02_...md 상태(진척도, 최신 의사결정) 실시간 갱신
- 옵시디언 그래프 뷰에 새로운 노드가 반짝이며 연결되도록 링크([[ ]]) 생성
"""
import os
from datetime import datetime

class ObsidianBridge:
    def __init__(self, vault_root=r"C:\Users\note\vz"):
        self.vault_root = vault_root

    def record_decision(self, situation, question, decision, reward_info=None):
        """JEV 의사결정 결과를 옵시디언 2nd Brain에 영구 자산화"""
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        date_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. 신규 실행 결과 노트 생성 (03_Knowledge/ 또는 02_Projects/ 하위)
        note_name = f"JEV_의사결정실행_{date_id}.md"
        note_path = os.path.join(self.vault_root, "03_Knowledge", note_name)

        action_name = decision.get("name", "미상 행동")
        action_id = decision.get("id", "ACT_XX")
        score = decision.get("calculated_score", 0.0)

        content = f"""---
title: JEV 자율 의사결정 실행 보고서 ({date_id})
created: {now_str}
action_id: {action_id}
score: {score}
tags: [JEV, Decision, Automation, ReinforcementLearning]
---

# 🤖 [JEV 실행] {action_name}

상위 프로젝트: [[vz02_jev_강화학습_자동화]]  
통합 관제탑: [[000_vz_통합_시스템_관제탑]]

---

## 1. 상황 인지 (Situation)
- **일시**: {now_str}
- **맥락**: {situation.get('raw_context', '')}
- **도메인**: {situation.get('domain', '')}

## 2. 핵심 의사결정 질문 (Question)
> {question}

## 3. 최종 선택된 행동 (Chosen Action)
- **행동 코드**: `{action_id}`
- **과업명**: **{action_name}**
- **기대가치 평가 점수**: **{score}점** (최고 득점)

## 4. 강화학습 피드백 상태 (Reward)
- **보상 수치**: `{reward_info.get('reward_score', 1.0) if reward_info else '대기'}`
- **상태**: `{reward_info.get('status', '정상 반영') if reward_info else '정상'}`
"""
        os.makedirs(os.path.dirname(note_path), exist_ok=True)
        with open(note_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

        # 2. vz02 프로젝트 카드의 진행 현황 업데이트
        proj_card = os.path.join(self.vault_root, "02_Projects", "vz02_jev_강화학습_자동화.md")
        if os.path.exists(proj_card):
            try:
                with open(proj_card, "r", encoding="utf-8") as pf:
                    lines = pf.readlines()

                new_lines = []
                for line in lines:
                    if line.startswith("progress:"):
                        new_lines.append("progress: 60%\n")
                    elif line.startswith("status:"):
                        new_lines.append("status: 가동중\n")
                    elif line.startswith("updated:"):
                        new_lines.append(f"updated: {datetime.now().strftime('%Y-%m-%d')}\n")
                    else:
                        new_lines.append(line)

                # 맨 아래에 최신 실행 링크 꼬리물기
                new_lines.append(f"\n- ⚡ **최신 자율 실행 기록**: [[{note_name[:-3]}]] ({now_str})\n")

                with open(proj_card, "w", encoding="utf-8") as pf:
                    pf.writelines(new_lines)
            except Exception:
                pass

        print(f"[OBSIDIAN BRIDGE] Successfully recorded to: {note_path}")
        return note_name[:-3]

if __name__ == "__main__":
    bridge = ObsidianBridge()
    dummy_sit = {"raw_context": "KENTECH CEO 특강 실전 시연", "domain": "Enterprise AX"}
    dummy_q = "최적의 시연 행동은?"
    dummy_dec = {"id": "ACT_03", "name": "과거 성공 자산 이식 및 자율 기획서 빌드", "calculated_score": 10.64}
    link = bridge.record_decision(dummy_sit, dummy_q, dummy_dec, {"reward_score": 1.0, "status": "REINFORCED"})
    print("Created Obsidian Node:", link)
