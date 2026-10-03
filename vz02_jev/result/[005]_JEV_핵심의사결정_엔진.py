# -*- coding: utf-8 -*-
"""
[JEV CORE ENGINE v1.0] SQAP 기반 의사결정 자율 자동화 코어
- 비즈니스 상황 인지 (Situation)
- 핵심 의사결정 질문 도출 (Question)
- 복수 행동 대안 도출 (Action Candidates)
- 확률 및 기대가치 판정 (Probability & Policy Selection)
- 보상 피드백(Reward) 및 자가 강화(Self-Reinforcement) 기록
"""
import os
import json
from datetime import datetime

class JEVDecisionEngine:
    def __init__(self, memory_file="data/jev_memory.json"):
        self.memory_file = memory_file
        self.memory = self._load_memory()

    def _load_memory(self):
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

    def _save_memory(self):
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def analyze_situation(self, raw_input):
        """1단계: 상황(Situation) 인지 및 핵심 특징 추출"""
        situation = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "raw_context": raw_input,
            "domain": "Enterprise AI Transformation & Business Strategy",
            "constraints": ["Token-Zero", "CEO-Level Clarity", "High ROI"]
        }
        return situation

    def formulate_question(self, situation):
        """2단계: 핵심 의사결정 질문(Question) 도출"""
        question = (
            f"상황 '{situation['raw_context'][:40]}...'에 대응하여, "
            f"인간의 개입을 최소화하면서 기업 가치를 극대화할 최적의 자동화 Action은 무엇인가?"
        )
        return question

    def generate_action_candidates(self, situation, question):
        """3단계: 행동(Action) 후보군 및 예상 시나리오 생성"""
        candidates = [
            {
                "id": "ACT_01",
                "name": "옵시디언 2nd Brain 지식 베이스 기반 자동 기획서 발행",
                "expected_impact": 0.85,
                "cost_risk": 0.15,
                "speed": 0.90
            },
            {
                "id": "ACT_02",
                "name": "외부 시장 트렌드 실시간 크롤링 및 EDA 통계 분석 파이프라인 가동",
                "expected_impact": 0.92,
                "cost_risk": 0.25,
                "speed": 0.75
            },
            {
                "id": "ACT_03",
                "name": "과거 성공 패턴(vf 기지) 자동 이식 및 즉각 실행 스크립트 빌드",
                "expected_impact": 0.95,
                "cost_risk": 0.10,
                "speed": 0.95
            }
        ]
        return candidates

    def decide_best_action(self, candidates):
        """4단계: 확률(Probability) 및 정책(Policy) 가중치 평가 후 최종 결정"""
        weights = self.memory.get("policy_weights", {})
        w_speed = weights.get("execution_speed", 1.0)
        w_cost = weights.get("cost_efficiency", 1.0)

        best_candidate = None
        best_score = -1.0

        for cand in candidates:
            # 점수 산출: (영향력 * 1.5 + 속도 * w_speed) / (리스크 * w_cost)
            score = (cand["expected_impact"] * 1.5 + cand["speed"] * w_speed) / (cand["cost_risk"] * w_cost + 0.1)
            cand["calculated_score"] = round(score, 2)
            if score > best_score:
                best_score = score
                best_candidate = cand

        return best_candidate

    def execute_and_reward(self, chosen_action, reward_feedback=1.0):
        """5단계: 실행 및 피드백(Reward)을 통한 강화학습 메모리 축적"""
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "chosen_action": chosen_action,
            "reward": reward_feedback
        }

        if reward_feedback > 0:
            self.memory["success_patterns"].append(log_entry)
        else:
            self.memory["failure_patterns"].append(log_entry)

        self._save_memory()
        return log_entry

if __name__ == "__main__":
    engine = JEVDecisionEngine()
    sit = engine.analyze_situation("10/22 KENTECH 최고위 과정 AI 브레인 전환 전략 강의 준비")
    q = engine.formulate_question(sit)
    cands = engine.generate_action_candidates(sit, q)
    decision = engine.decide_best_action(cands)
    log = engine.execute_and_reward(decision, reward_feedback=1.0)
    print("[JEV DECISION RESULT]")
    print(json.dumps(log, ensure_ascii=False, indent=2))
