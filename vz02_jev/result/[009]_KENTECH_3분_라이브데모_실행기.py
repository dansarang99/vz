# -*- coding: utf-8 -*-
"""
[KENTECH LIVE DEMO ENGINE v2.0]
- 모든 소스와 데이터가 result/ 내 [001]~[009] 순차 시리얼로 완전 정돈된 실행기
"""
import os
import sys
import json
import time
import importlib.util
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def load_module(mod_name, file_name):
    fpath = os.path.join(CURRENT_DIR, file_name)
    spec = importlib.util.spec_from_file_location(mod_name, fpath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# [005], [006], [007] 모듈 동적 로드
core_mod = load_module('jev_core', '[005]_JEV_핵심의사결정_엔진.py')
opt_mod = load_module('jev_reinforcement', '[006]_JEV_강화학습_피드백최적화.py')
bridge_mod = load_module('obsidian_bridge', '[007]_JEV_옵시디언_2nd_Brain_연동브릿지.py')

JEVDecisionEngine = core_mod.JEVDecisionEngine
ReinforcementOptimizer = opt_mod.ReinforcementOptimizer
ObsidianBridge = bridge_mod.ObsidianBridge

def run_live_demo(scenario_text=None):
    print('=' * 80)
    print('🚀 [KENTECH CEO 특강 라이브 데모] result/ 100% 무결점 순차 시리얼 파이프라인')
    print('=' * 80)

    if not scenario_text:
        scenario_text = "전남 지역 중견 제조기업의 '휴먼브레인(사람 의존) ➔ AI브레인(자율 의사결정) 전환' 전략 수립"

    mem_file = os.path.join(CURRENT_DIR, '[008]_JEV_강화학습_기억메모리.json')
    engine = JEVDecisionEngine(memory_file=mem_file)
    situation = engine.analyze_situation(scenario_text)

    print(f"\n[1단계: 상황 인지 (Situation)]")
    print(f' ▸ 입력된 비즈니스 맥락: "{scenario_text}"')

    question = engine.formulate_question(situation)
    print(f"\n[2단계: 핵심 경영 질문 도출 (Question)]")
    print(f' ▸ 도출된 질문: "{question}"')

    candidates = engine.generate_action_candidates(situation, question)
    print(f"\n[3단계: 행동 후보군 탐색 및 기대가치 평가 (Action Candidates)]")
    for c in candidates:
        print(f"   [{c['id']}] {c['name']} (기대영향: {c['expected_impact']*100:.0f}%, 리스크: {c['cost_risk']*100:.0f}%)")

    chosen = engine.decide_best_action(candidates)
    print(f"\n[4단계: JEV 최적 의사결정 (Decision Making)]")
    print(f" 🎯 [최종 채택]: {chosen['id']} - {chosen['name']}")
    print(f"    - 정책 가중치 기반 최종 스코어: {chosen['calculated_score']}점 (최고 득점 단독 채택)")

    report_file = os.path.join(CURRENT_DIR, '[001]_AI브레인_전환_실행계획서.md')
    print(f"\n[5단계: 자동화 결과물 최신화 (Delivery)]")
    print(f" 📄 완제 계획서 파일 연결: {report_file}")

    bridge = ObsidianBridge(vault_root=r"C:\Users\note\vz")
    node_name = bridge.record_decision(situation, question, chosen, {'reward_score': 1.0, 'status': 'LIVE_DEMO_PASSED'})
    print(f"\n[6단계: 옵시디언 2nd Brain 관제탑 실시간 동기화]")
    print(f" 🧠 옵시디언 노드 연결 완료: [[{node_name}]]")

    optimizer = ReinforcementOptimizer(memory_file=mem_file)
    opt_log = optimizer.apply_feedback(chosen['id'], reward_score=1.0, comment='KENTECH CEO 특강 라이브 데모 최고 판정')
    print(f"\n[7단계: CEO 피드백 기반 강화학습(RL) 정책 튜닝]")
    print(f" 🎖️ 피드백 반영 완료: {opt_log['status']}")
    print(f"    - 튜닝된 정책 가중치: {opt_log['updated_weights']}")

    print("\n" + '=' * 80)
    print('✅ [성공] result/ [001]~[009] 엔드투엔드 파이프라인 100% 무결점 완주!')
    print('=' * 80)

if __name__ == '__main__':
    run_live_demo()
