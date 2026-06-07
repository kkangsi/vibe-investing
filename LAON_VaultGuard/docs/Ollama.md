# Ollama 오프라인 모드 연동 — LAON VaultGuard

> 🇰🇷 Ollama를 이용해 인터넷 연결 없이 로컬 LLM으로 시크릿 탐지.
> 🇺🇸 Use Ollama for fully offline secret detection with a local LLM.
> 🇨🇳 使用 Ollama 在完全离线状态下进行本地 LLM 密钥检测。

## 1. Ollama 설치

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Windows (WSL)
```bash
# WSL 내에서 Linux와 동일하게 설치
curl -fsSL https://ollama.com/install.sh | sh
```

## 2. 모델 다운로드

```bash
ollama pull llama3.1    # 권장 (8B, 빠름, 한글 지원)
ollama pull mistral      # 대안 (7B, 가벼움)
ollama pull codellama    # 코드 특화 (7B)
```

## 3. .env 설정

```bash
# Ollama만 사용 (완전 오프라인)
LLM_PROVIDERS=ollama
LLM_MODE=sequential

# Ollama + 다른 LLM 혼합 (하이브리드)
LLM_PROVIDERS=ollama,deepseek
LLM_MODE=parallel

# Ollama 설정 (기본값이면 생략 가능)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=llama3.1
```

## 4. 장점

- **완전 오프라인** — 네트워크 불필요, API 키 불필요
- **무료** — 토큰 비용 $0
- **프라이버시** — 소스코드가 로컬을 벗어나지 않음 (기밀 레포에 필수)
- **오픈소스** — llama3, mistral, qwen 등 다양한 모델 선택 가능

## 5. 한계

- **속도** — API 기반 LLM보다 느림 (Mac M1: ~30 tok/s, CPU: ~10 tok/s)
- **정확도** — 작은 모델(7B~8B)은 API 모델보다 오탐/미탐 가능성 높음
- **리소스** — 최소 8GB RAM (llama3.1 8B 기준)

## 6. 권장 구성

| 환경 | LLM 구성 | 설명 |
|---|---|---|
| 개인 노트북 | `ollama` | 혼자 쓸 때 완전 오프라인 |
| 팀/회사 | `deepseek,ollama` | 평소 DeepSeek, 네트워크 장애 시 Ollama fallback |
| 기밀 레포 | `ollama` | 소스코드 외부 전송 금지 환경 |

## 7. 문제 해결

| 증상 | 해결 |
|---|---|
| `ollama` 명령어 없음 | 설치 후 터미널 재시작 또는 `ollama serve` 수동 실행 |
| 모델 응답 없음 | `ollama list`로 모델 확인, `ollama pull llama3.1` 재시도 |
| 느린 응답 | 더 작은 모델로 변경 (`ollama pull llama3.2:1b`) |
