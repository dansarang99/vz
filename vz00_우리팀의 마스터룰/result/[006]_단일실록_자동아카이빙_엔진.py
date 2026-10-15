# -*- coding: utf-8 -*-
"""
[GLOBAL ENGINE] 우리팀 단일 무손실 실록 통합 엔진 (save_conversation_archive.py)
- 개별 파일 분할 없이 `conversation/CONVERSATION_TOTAL.md` 단 하나의 파일로 일원화
- 꼬리에 꼬리를 물고(Append) 대화가 무한 누적 기록됨
- 세션/턴이 끝나는 지점마다 정확한 일자와 시간(Timestamp) 구분선 기록
- 원본 JSONL은 `conversation/prompt/CONVERSATION_RAW.jsonl`에 정돈 보존
"""
import os
import sys
import json
import glob
import shutil
from datetime import datetime

def find_latest_transcript(app_data_dir=r"C:\Users\note\.gemini\antigravity-cli"):
    """가장 최근에 수정된 transcript_full.jsonl 탐색"""
    pattern = os.path.join(app_data_dir, "brain", "*", ".system_generated", "logs", "transcript_full.jsonl")
    files = glob.glob(pattern)
    if not files:
        pattern2 = os.path.join(app_data_dir, "brain", "*", ".system_generated", "logs", "transcript.jsonl")
        files = glob.glob(pattern2)
    if not files:
        return None
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return files[0]

def archive_conversation(target_workspace=None, current_conv_id=None):
    if not target_workspace:
        target_workspace = os.getcwd()
    
    conv_dir = os.path.join(target_workspace, "conversation")
    os.makedirs(conv_dir, exist_ok=True)
    
    prompt_dir = os.path.join(conv_dir, "prompt")
    os.makedirs(prompt_dir, exist_ok=True)
    
    transcript_path = find_latest_transcript()
    if not transcript_path or not os.path.exists(transcript_path):
        print(f"[WARN] No transcript found for {target_workspace}")
        return None

    detected_conv_id = transcript_path.split(os.sep)[-4]
    active_conv_id = current_conv_id if current_conv_id else detected_conv_id
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 1. 단일 마스터 파일 및 RAW 파일 경로 지정
    single_md_path = os.path.join(conv_dir, "CONVERSATION_TOTAL.md")
    single_raw_path = os.path.join(prompt_dir, "CONVERSATION_RAW.jsonl")

    # 2. RAW 파일 최신화 복사 (prompt 폴더에 보존)
    shutil.copy2(transcript_path, single_raw_path)

    # 3. JSONL 파싱
    records = []
    with open(transcript_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass

    # 4. 단일 파일 내용 렌더링
    existing_content = ""
    if os.path.exists(single_md_path):
        try:
            with open(single_md_path, "r", encoding="utf-8") as ef:
                existing_content = ef.read()
        except Exception:
            existing_content = ""

    header_tag = f"<!-- SESSION_ID: {active_conv_id} -->"

    session_body = [
        header_tag,
        f"# 🎖️ 본부장님 ↔ ADVISOR 총괄팀장 대화 무손실 통합 실록 (CONVERSATION_TOTAL)",
        "",
        "> **지위**: 100% 무손실 최고 사령부 단일 통합 실록 (Single Master Verbatim)",
        f"> **기록 시작 일시**: {now_str}",
        f"> **작업 사령부 (Workspace)**: `{target_workspace}`",
        f"> **대화 고유 ID (Conversation ID)**: `{active_conv_id}`",
        f"> **총 기록 단계 수 (Total Steps)**: {len(records)} Steps",
        "> **불변 원칙**: 단 하나의 파일로 꼬리에 꼬리를 물고 누적되며, 끝나는 지점마다 일자와 시간을 명시함",
        "",
        "---",
        ""
    ]

    for rec in records:
        step_idx = rec.get("step_index", 0)
        source = rec.get("source", "UNKNOWN")
        stype = rec.get("type", "")
        created_at = rec.get("created_at", "")
        content = rec.get("content", "")

        # 본부장님(USER) 하명
        if source == "USER_EXPLICIT" or stype == "USER_INPUT":
            session_body.append(f"## 👑 [Step {step_idx}] 본부장님 하명 ({created_at})")
            session_body.append("")
            session_body.append("```text")
            session_body.append(str(content).strip())
            session_body.append("```")
            session_body.append("")
            session_body.append("---")
            session_body.append("")

        # 총괄팀장(MODEL) 브리핑
        elif source == "MODEL" or stype == "PLANNER_RESPONSE":
            if content and str(content).strip():
                session_body.append(f"### 🗣️ [Step {step_idx}] ADVISOR 총괄팀장 보고 ({created_at})")
                session_body.append("")
                session_body.append(str(content).strip())
                session_body.append("")
                session_body.append("---")
                session_body.append("")

    # 세션 끝나는 지점 타임스탬프 블록 명시 (본부장님 핵심 요구사항)
    session_body.append("")
    session_body.append("```")
    session_body.append(f"========================================================================================")
    session_body.append(f"⏰ [대화 기록 일시]: {now_str}")
    session_body.append(f"📌 [기록 완료 지점]: Conversation ID [{active_conv_id}] - Total {len(records)} Steps 완료")
    session_body.append(f"========================================================================================")
    session_body.append("```")
    session_body.append("")

    new_session_text = "\n".join(session_body)

    # 기존 파일 처리: 동일 세션이면 덮어쓰고, 이전 세션이 있다면 뒤에 꼬리물기
    if header_tag in existing_content:
        parts = existing_content.split(header_tag)
        final_text = parts[0] + new_session_text
    elif existing_content.strip():
        final_text = existing_content.rstrip() + "\n\n\n---\n\n\n" + new_session_text
    else:
        final_text = new_session_text

    with open(single_md_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    # 이전 분할 파일들([001], [002]...)이 있다면 자동 정리
    for old_file in os.listdir(conv_dir):
        if old_file.startswith("[") and (old_file.endswith(".md") or old_file.endswith(".jsonl")):
            try:
                os.remove(os.path.join(conv_dir, old_file))
            except Exception:
                pass

    print(f"[SUCCESS] Appended conversation to: {single_md_path}")
    return single_md_path

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else None
    conv_id = sys.argv[2] if len(sys.argv) > 2 else None
    archive_conversation(target, conv_id)
