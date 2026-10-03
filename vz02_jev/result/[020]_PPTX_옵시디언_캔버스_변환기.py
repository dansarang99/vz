# -*- coding: utf-8 -*-
"""
[JEV 산출물 020] PPTX ➔ 옵시디언 캔버스(Canvas) 자동 변환 파이프라인
- 입력: upload/ 폴더 내 PPTX 파일
- 변환:
  1. PowerPoint COM 엔진을 통해 1280x720 고화질 슬라이드 이미지 일괄 추출 (upload/ 폴더 저장)
  2. python-pptx를 통해 슬라이드별 텍스트 및 스크립트 추출
  3. 옵시디언 네이티브 .canvas JSON 파일 자동 빌드 (이미지 노드 + 텍스트 노드 + 시각적 연결선)
- 출력: result/[021]_광주_2차_휴먼브레인_전환전략_캔버스.canvas
- 규약: result/ [001]~[999] 무결점 순차 시리얼 절대 준수
"""
import os
import sys
import json
import uuid
import win32com.client
import pptx

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
VAULT_ROOT = r"C:\Users\note\vz"
UPLOAD_DIR = os.path.join(PROJECT_ROOT, "upload")
RESULT_DIR = os.path.join(PROJECT_ROOT, "result")

def convert_pptx_to_canvas(pptx_filename="광주_2차_003.pptx", canvas_filename="[021]_광주_2차_휴먼브레인_전환전략_캔버스.canvas"):
    pptx_path = os.path.join(UPLOAD_DIR, pptx_filename)
    if not os.path.exists(pptx_path):
        raise FileNotFoundError(f"PPTX 파일을 찾을 수 없습니다: {pptx_path}")

    print("=" * 80)
    print(f"🎨 [PPTX ➔ 옵시디언 캔버스 변환기 가동]")
    print(f" ▸ 원본 파일: {pptx_path}")
    print("=" * 80)

    # 1. PowerPoint COM으로 슬라이드 이미지 추출
    print("\n[1단계: 슬라이드 고해상도 이미지 일괄 렌더링 중...]")
    ppt_app = win32com.client.Dispatch("PowerPoint.Application")
    prs_com = ppt_app.Presentations.Open(os.path.abspath(pptx_path), WithWindow=False)
    total_slides = prs_com.Slides.Count
    print(f" ▸ 총 슬라이드 수: {total_slides}장")

    image_rel_paths = []
    prefix = os.path.splitext(pptx_filename)[0]

    for i in range(1, total_slides + 1):
        img_name = f"{prefix}_slide_{i:03d}.png"
        img_full_path = os.path.join(UPLOAD_DIR, img_name)
        # Vault 기준 상대 경로 계산
        vault_rel_path = os.path.relpath(img_full_path, VAULT_ROOT).replace("\\", "/")
        image_rel_paths.append((img_full_path, vault_rel_path))
        prs_com.Slides(i).Export(os.path.abspath(img_full_path), "PNG", 1280, 720)

    prs_com.Close()
    ppt_app.Quit()
    print(f" ▸ {total_slides}장 이미지 추출 완료 (upload/ 폴더 저장)")

    # 2. python-pptx로 텍스트 추출
    print("\n[2단계: 슬라이드별 텍스트 및 개체 정보 분석 중...]")
    prs_pptx = pptx.Presentation(pptx_path)
    slide_texts = []
    for idx, slide in enumerate(prs_pptx.slides):
        texts = []
        for shape in slide.shapes:
            if shape.has_text_frame:
                txt = shape.text.strip()
                if txt:
                    texts.append(txt)
        slide_texts.append(texts)

    # 3. 옵시디언 캔버스 JSON 구조체 생성
    print("\n[3단계: 옵시디언 캔버스(.canvas) 노드 및 엣지 빌드 중...]")
    nodes = []
    edges = []

    # 레이아웃 상수 (가로 6열 그리드)
    COLS = 6
    NODE_WIDTH = 560
    NODE_HEIGHT = 315  # 16:9 비율
    TEXT_HEIGHT = 160
    GAP_X = 140
    GAP_Y = 160
    COL_PITCH = NODE_WIDTH + GAP_X
    ROW_PITCH = NODE_HEIGHT + TEXT_HEIGHT + GAP_Y

    prev_img_node_id = None

    for i in range(total_slides):
        col = i % COLS
        row = i // COLS
        x = col * COL_PITCH
        y = row * ROW_PITCH

        slide_num = i + 1
        img_node_id = f"slide_{slide_num:03d}"
        text_node_id = f"text_{slide_num:03d}"
        _, vault_rel_path = image_rel_paths[i]

        # 3-1. 슬라이드 이미지 노드
        nodes.append({
            "id": img_node_id,
            "type": "file",
            "file": vault_rel_path,
            "x": x,
            "y": y,
            "width": NODE_WIDTH,
            "height": NODE_HEIGHT
        })

        # 3-2. 슬라이드 텍스트/해설 노드
        raw_texts = slide_texts[i] if i < len(slide_texts) else []
        if raw_texts:
            title = raw_texts[0].split('\n')[0]
            body_lines = []
            for t in raw_texts[1:4]:
                for line in t.split('\n')[:2]:
                    if line.strip():
                        body_lines.append(f"- {line.strip()}")
            content_md = f"### [{slide_num:02d}장] {title}\n" + "\n".join(body_lines)
        else:
            content_md = f"### [{slide_num:02d}장] 시각 비주얼 / 다이어그램 슬라이드\n*(도형 및 이미지 중심 슬라이드)*"

        # 색상 구분: 10장 단위로 카드 색상 변화 (1~6)
        color_code = str(((slide_num - 1) // 8) % 6 + 1)
        nodes.append({
            "id": text_node_id,
            "type": "text",
            "text": content_md,
            "x": x,
            "y": y + NODE_HEIGHT + 15,
            "width": NODE_WIDTH,
            "height": TEXT_HEIGHT,
            "color": color_code
        })

        # 3-3. 슬라이드 간 순차 연결선 (Edge)
        if prev_img_node_id:
            # 같은 행이면 오른쪽 ➔ 왼쪽 연결
            if col > 0:
                edges.append({
                    "id": f"edge_{slide_num-1}_{slide_num}",
                    "fromNode": prev_img_node_id,
                    "fromSide": "right",
                    "toNode": img_node_id,
                    "toSide": "left"
                })
            else:
                # 다음 행으로 넘어갈 때는 아래 ➔ 위 연결
                edges.append({
                    "id": f"edge_{slide_num-1}_{slide_num}",
                    "fromNode": prev_img_node_id,
                    "fromSide": "bottom",
                    "toNode": img_node_id,
                    "toSide": "top"
                })
        prev_img_node_id = img_node_id

    canvas_data = {
        "nodes": nodes,
        "edges": edges
    }

    canvas_out_path = os.path.join(RESULT_DIR, canvas_filename)
    with open(canvas_out_path, "w", encoding="utf-8") as f:
        json.dump(canvas_data, f, ensure_ascii=False, indent=2)

    print(f"\n[4단계: 옵시디언 캔버스 저장 완료]")
    print(f" ▸ 생성 파일: {canvas_out_path}")
    print(f" ▸ 총 노드 수: {len(nodes)}개 (이미지 {total_slides}개 + 텍스트 {total_slides}개)")
    print(f" ▸ 총 연결선: {len(edges)}개")
    print("=" * 80)
    print("✅ [옵시디언 캔버스 변환 무결점 완주 성공]")
    print("=" * 80)
    return canvas_out_path

if __name__ == "__main__":
    convert_pptx_to_canvas()
