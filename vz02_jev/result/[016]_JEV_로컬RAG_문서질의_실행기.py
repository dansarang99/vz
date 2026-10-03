# -*- coding: utf-8 -*-
"""
[JEV 산출물 016] JEV 로컬 RAG 문서 질의 실행기
- 목적: upload/ 폴더의 문서를 읽어 로컬 LLM(gemma2:2b, hermes3:8b 등)을 통해 자율 RAG 질의응답 수행
- 규약: result/ [001]~[999] 무결점 순차 시리얼 절대 준수
"""
import os
import sys
import json
import subprocess
import argparse
from datetime import datetime

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "upload")
VAULT_DIR = r"C:\Users\note\vz"
OBSIDIAN_DECISION_DIR = os.path.join(VAULT_DIR, "00_Inbox_수신함", "JEV_의사결정노트")

def read_document(file_path):
    """지정된 문서 파일의 텍스트를 안전하게 로드"""
    if not os.path.isabs(file_path):
        file_path = os.path.join(PROJECT_ROOT, file_path)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"문서 파일을 찾을 수 없습니다: {file_path}")

    encodings = ['utf-8', 'cp949', 'euc-kr']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read(), os.path.basename(file_path)
        except UnicodeDecodeError:
            continue
    raise ValueError(f"지원하는 인코딩으로 파일을 읽을 수 없습니다: {file_path}")

def query_wsl_rag(model_name="gemma2:2b", context_text="", question=""):
    """WSL2 Ollama를 통해 RAG 프롬프트 추론 수행"""
    # 프롬프트 구성 (컨텍스트 + 질문)
    system_prompt = f"""당신은 제공된 참고 문서를 정밀하게 분석하여 답변하는 1인 AI 기업의 전문 RAG 인텔리전스 두뇌입니다.
반드시 아래 [참고 문서]의 내용만을 근거로 하여 질문에 정직하고 명쾌하게 답변하십시오.

[참고 문서]:
\"\"\"
{context_text[:3500]}
\"\"\"

[질문]:
{question}

[답변 가이드]:
1. 참고 문서에 명시된 핵심 사실을 바탕으로 답변할 것.
2. 3~5줄 내외로 절도 있고 명쾌하게 정리할 것."""

    python_script = f"""
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:11434/api/generate',
    data=json.dumps({{
        'model': '{model_name}',
        'prompt': '''{system_prompt}''',
        'stream': False,
        'options': {{
            'num_predict': 350,
            'temperature': 0.2
        }}
    }}).encode('utf-8'),
    headers={{'Content-Type': 'application/json'}}
)
try:
    res = urllib.request.urlopen(req, timeout=120)
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

def run_rag_qa(file_path, question, model="gemma2:2b"):
    print("=" * 80)
    print(f"📚 [JEV 로컬 RAG 파이프라인 가동] 모델: {model}")
    print("=" * 80)

    doc_text, doc_name = read_document(file_path)
    print(f"\n[1단계: upload/ 문서 로드 완료]")
    print(f" ▸ 대상 파일: {doc_name} (총 {len(doc_text):,}자)")
    print(f" ▸ 사용자 질문: \"{question}\"")

    print(f"\n[2단계: 로컬 RAG 실시간 지식 추론 중 (Token-Zero)...]")
    t_start = datetime.now()
    answer = query_wsl_rag(model_name=model, context_text=doc_text, question=question)
    elapsed = (datetime.now() - t_start).total_seconds()
    print(f" ▸ 추론 완결 (소요시간: {elapsed:.2f}초)")

    print(f"\n[3단계: RAG 답변 리포트]")
    print("-" * 60)
    print(answer)
    print("-" * 60)

    # 옵시디언 2nd Brain 자동 퍼블리싱
    os.makedirs(OBSIDIAN_DECISION_DIR, exist_ok=True)
    ts_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    obsidian_note_path = os.path.join(OBSIDIAN_DECISION_DIR, f"RAG_질의결과_{ts_slug}.md")
    note_content = f"""---
title: "RAG 질의: {doc_name}"
date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
document: "{doc_name}"
model: "{model}"
tags: [rag, jev, knowledge, {model}]
---

# 📚 JEV 로컬 RAG 질의응답 리포트

## 1. 질의 개요
- **참고 문서**: `{doc_name}`
- **질문 내용**: {question}
- **추론 모델**: `{model}` (WSL2 로컬 0-Token)
- **소요 시간**: {elapsed:.2f}초

## 2. RAG 도출 답변
{answer}
"""
    with open(obsidian_note_path, 'w', encoding='utf-8') as f:
        f.write(note_content)
    print(f"\n[4단계: 옵시디언 2nd Brain 실시간 퍼블리싱]")
    print(f" ▸ 볼트 노트 생성: {obsidian_note_path}")
    print("=" * 80)
    print("✅ [RAG 질의응답 무결점 완주 성공]")
    print("=" * 80)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JEV Local RAG Document QA Runner")
    parser.add_argument("--file", type=str, default="upload/curriculum_summary.txt", help="Document path in upload folder")
    parser.add_argument("--question", type=str, default="본 과정의 핵심 교육 목표를 3줄로 요약해줘.", help="Question to ask")
    parser.add_argument("--model", type=str, default="gemma2:2b", help="Model name (gemma2:2b, hermes3:8b, llama3.2:3b)")
    args = parser.parse_args()

    run_rag_qa(file_path=args.file, question=args.question, model=args.model)
