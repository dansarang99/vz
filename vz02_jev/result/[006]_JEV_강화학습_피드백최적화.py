# -*- coding: utf-8 -*-
"""
[JEV REINFORCEMENT MODULE] 피드백 기반 강화학습(RL) 정책 업데이트 엔진
- Like (+1.0) / Dislike (-1.0) 또는 0.0~1.0 세부 스코어 피드백 수신
- 성공 패턴 및 실패 패턴 가중치 실시간 튜닝
- Policy Weights(정책 가중치: 속도, 비용효율성, 시장트렌드) 자가 최적화
"""
import os
import json
from datetime import datetime

class ReinforcementOptimizer:
    def __init__(self, memory_file="data/jev_memory.json"):
        self.memory_file = memory_file
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "success_patterns": [],
            "failure_patterns": [],
            "policy_weights": {
                "market_trend": 1.2,
                "cost_efficiency": 1.5,
                "execution_speed": 1.3
            }
        }

    def _save(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def apply_feedback(self, action_id, reward_score, comment=""):
        """CEO의 피드백을 수신하여 정책 가중치를 동적으로 튜닝"""
        weights = self.data.setdefault("policy_weights", {
            "market_trend": 1.2,
            "cost_efficiency": 1.5,
            "execution_speed": 1.3
        })

        # 보상 점수에 따른 정책 가중치 조정 (경사하강법/강화학습 원리 단순화)
        # reward_score > 0 (성공): 해당 행동의 특성 가중치를 강화
        learning_rate = 0.05
        if reward_score >= 0.5:
            delta = learning_rate * reward_score
            weights["execution_speed"] = round(weights["execution_speed"] + delta, 3)
            weights["cost_efficiency"] = round(weights["cost_efficiency"] + delta * 0.8, 3)
            status = "POLICY_REINFORCED (강화 성공)"
        else:
            delta = learning_rate * (1.0 - reward_score)
            weights["cost_efficiency"] = round(max(0.5, weights["cost_efficiency"] - delta), 3)
            status = "POLICY_PENALIZED (패널티 반영)"

        log_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action_id": action_id,
            "reward_score": reward_score,
            "comment": comment,
            "status": status,
            "updated_weights": dict(weights)
        }

        if reward_score >= 0.5:
            self.data.setdefault("success_patterns", []).append(log_record)
        else:
            self.data.setdefault("failure_patterns", []).append(log_record)

        self._save()
        return log_record

if __name__ == "__main__":
    opt = ReinforcementOptimizer()
    res = opt.apply_feedback("ACT_03", reward_score=1.0, comment="CEO 최고위 강의 실전 테스트 대성공")
    print("[REINFORCEMENT UPDATE RESULT]")
    print(json.dumps(res, ensure_ascii=False, indent=2))
