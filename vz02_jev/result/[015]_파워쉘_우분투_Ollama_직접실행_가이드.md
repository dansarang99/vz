# 📘 [JEV 산출물 015] 파워쉘 및 우분투 Ollama 직접 실행 매뉴얼

> **작성일자**: 2026-10-03  
> **총괄책임**: ADVISOR 총괄팀장  
> **수신**: 본부장님 (Chief Executive Officer)  
> **적용 환경**: Windows PowerShell & Ubuntu WSL2  
> **결과물 위치**: `result/[015]_파워쉘_우분투_Ollama_직접실행_가이드.md`

---

## 1. 개요
본부장님 PC의 우분투(WSL2)에는 이미 세계 최고 수준의 AI 모델(`gemma2:2b`, `hermes3:8b`, `llama3.2:3b`)이 완벽히 설치·상주해 있습니다.  
따라서 파워쉘과 우분투 양쪽 어디에서나 단 한 줄의 명령어로 즉시 대화형 AI를 직접 기동할 수 있습니다.

---

## 2. 방법 1: 윈도우 파워쉘(PowerShell)에서 직접 실행 (가장 추천)
윈도우 터미널(PowerShell) 창을 열고 아래 명령어를 입력하시면 우분투에 설치된 모델과 즉시 실시간 대화가 시작됩니다.

### ① Gemma 2 2B (초경량/고속 대화)
```powershell
wsl ollama run gemma2:2b
```

### ② Hermes 3 8B (심층 추론/전략 의사결정)
```powershell
wsl ollama run hermes3:8b
```

### ③ Llama 3.2 3B (최신 메타 경량 모델)
```powershell
wsl ollama run llama3.2:3b
```

### ④ 현재 보유 중인 모델 목록 확인
```powershell
wsl ollama list
```

---

## 3. 방법 2: 우분투(Ubuntu WSL) 내부에서 직접 실행
우분투 터미널 창을 직접 열었을 때는 앞의 `wsl` 접두사 없이 바로 실행하시면 됩니다.

### ① 모델 실행 명령어
```bash
ollama run gemma2:2b
```
또는
```bash
ollama run hermes3:8b
```

### ② 실행 상태 및 메모리 확인
```bash
ollama ps
```

---

## 4. 핵심 단축키 및 대화 종료 방법
대화창(`>>>` 프롬프트)이 떴을 때:
- **대화 종료 및 터미널 복귀**: `/bye` 입력 후 엔터 (또는 `Ctrl + D`)
- **도움말 보기**: `/?`
- **단축키 강제 종료**: `Ctrl + C`
