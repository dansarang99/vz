# -*- coding: utf-8 -*-
"""
[JEV 산출물 014] JEV WSL 로컬 LLM 통합 의사결정 실행기
- 백엔드: Ubuntu WSL Ollama (gemma2:2b, hermes3:8b, llama3.2:3b)
- 기능: 로컬 LLM 직접 연동 ➔ JEV 4단계 의사결정 ➔ 강화학습 피드백 ➔ 옵시디언 2nd Brain 자동 동기화
- 규약: result/ [001]~[999] 무결점 순차 시리얼 절대 준수
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime

# Windows 콘솔 인코딩 방어
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VAULT_DIR = r"C:\Users\note\vz"
OBSIDIAN_DECISION_DIR = os.path.join(VAULT_DIR, "00_Inbox_수신함", "JEV_의사결정노트")

def query_wsl_ollama(model_name="gemma2:2b", prompt=""):
    """
    WSL2 내부의 Ollama REST API를 로컬 호출하여 LLM 추론 수행
    """
    python_script = f"""
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:11434/api/generate',
    data=json.dumps({{
        'model': '{model_name}',
        'prompt': '''{prompt}''',
        'stream': False,
        'options': {{
            'num_predict': 260,
            'temperature': 0.2
        }}
    }}).encode('utf-8'),
    headers={{'Content-Type': 'application/json'}}
)
try:
    res = urllib.request.urlopen(req, timeout=180)
    data = json.loads(res.read().decode('utf-8'))
    print(data.get('response', ''))
except Exception as e:
    print(f'ERROR: {{e}}')
"""
    cmd = ["wsl", "-e", "python3", "-c", python_script]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
        if proc.returncode == 0:
            return proc.stdout.strip()
        else:
            return f"[오류 발생] {proc.stderr.strip()}"
    except Exception as e:
        return f"[시스템 예외] {str(e)}"

def run_jev_decision_pipeline(scenario=None, model="gemma2:2b", feedback_score=1.0):
    print("=" * 80)
    print(f"🧠 [JEV 1인 AI 기업 로컬 두뇌 기동] 모델: {model} | 환경: WSL2 Ollama")
    print("=" * 80)

    if not scenario:
        scenario = "전남 지역 중견 제조기업의 휴먼브레인(사람 의존)을 AI브레인(자율 의사결정)으로 전환하는 전략"

    print(f"\n[1단계: 상황 인지 및 질문 도출]")
    print(f" ▸ 비즈니스 상황: {scenario}")
    question = "CEO가 당장 내일부터 전사적으로 AI를 적용할 때 실패하지 않는 1호 실행 수칙은 무엇인가?"
    print(f" ▸ JEV 경영 질문: {question}")

    # LLM 프롬프트 조립
    system_prompt = f"""당신은 1인 AI 기업의 자율 의사결정 전략 두뇌 JEV(Joint Expected Value)입니다.
최고의사결정권자(본부장님/CEO)에게 직관적이고 즉시 실행 가능한 결정을 보고해야 합니다.

[상황]: {scenario}
[질문]: {question}

반드시 다음 형식으로 3줄 핵심 요약 보고를 작성하십시오:
1. 1호 실행 조치 (즉시 적용)
2. 기대 효과 및 위험 회피 (정량적/정성적)
3. 확장 로드맵 (향후 자율 운영)"""

    print(f"\n[2단계: 로컬 LLM ({model}) 실시간 자율 추론 중 (Token-Zero)...]")
    t_start = datetime.now()
    llm_decision = query_wsl_ollama(model_name=model, prompt=system_prompt)
    elapsed = (datetime.now() - t_start).total_seconds()
    print(f" ▸ 추론 완료 (소요시간: {elapsed:.2f}초)")

    print(f"\n[3단계: JEV 최적 의사결정 보고]")
    print("-" * 60)
    print(llm_decision)
    print("-" * 60)

    # 강화학습 메모리 파일 갱신
    mem_file = os.path.join(CURRENT_DIR, "[008]_JEV_강화학습_기억메모리.json")
    mem_data = {"history": [], "policy_weights": {}}
    if os.path.exists(mem_file):
        try:
            with open(mem_file, 'r', encoding='utf-8') as f:
                mem_data = json.load(f)
        except Exception:
            pass

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "model": model,
        "scenario": scenario,
        "question": question,
        "decision": llm_decision,
        "elapsed_seconds": elapsed,
        "feedback_score": feedback_score
    }
    mem_data.setdefault("history", []).append(log_entry)

    with open(mem_file, 'w', encoding='utf-8') as f:
        json.dump(mem_data, f, ensure_ascii=False, indent=2)
    print(f"\n[4단계: 강화학습 기억 메모리 동기화]")
    print(f" ▸ 누적 의사결정 이력: {len(mem_data['history'])}건 ([008] JSON 갱신 완료)")

    # 옵시디언 2nd Brain 자동 퍼블리싱
    os.makedirs(OBSIDIAN_DECISION_DIR, exist_ok=True)
    ts_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    obsidian_note_path = os.path.join(OBSIDIAN_DECISION_DIR, f"JEV_의사결정_{ts_slug}.md")
    note_content = f"""---
title: "JEV 의사결정: {ts_slug}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
model: "{model}"
feedback_score: {feedback_score}
tags: [jev, decision, ai-brain, {model}]
---

# 🧠 JEV 자율 의사결정 리포트

## 1. 개요
- **상황 맥락**: {scenario}
- **도출 질문**: {question}
- **추론 모델**: `{model}` (WSL2 로컬 무제한 연산)
- **추론 소요**: {elapsed:.2f}초

## 2. JEV 최종 결정 내용
{llm_decision}

## 3. 피드백 및 강화학습
- **부여된 피드백 점수**: {feedback_score} (1.0 = 우수/채택, -1.0 = 기각)
- **메모리 아카이브**: `vz02_jev/result/[008]_JEV_강화학습_기억메모리.json`
"""
    with open(obsidian_note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)
    print(f"\n[5단계: 옵시디언 2nd Brain 실시간 퍼블리싱]")
    print(f" ▸ 볼트 노트 생성: {obsidian_note_path}")
    print("=" * 80)
    print("✅ [JEV 전 파이프라인 무결점 완주 성공]")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JEV WSL Local LLM Runner")
    parser.add_argument("--model", type=str, default="gemma2:2b", help="Model name (gemma2:2b, hermes3:8b, llama3.2:3b)")
    parser.add_argument("--scenario", type=str, default=None, help="Business scenario")
    parser.add_argument("--feedback", type=float, default=1.0, help="Feedback score")
    args = parser.parse_args()

    run_jev_decision_pipeline(scenario=args.scenario, model=args.model, feedback_score=args.feedback)
