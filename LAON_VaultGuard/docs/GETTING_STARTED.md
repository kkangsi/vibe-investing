# LAON VaultGuard — Getting Started

> 5분 만에 설치부터 첫 스캔까지.

## 1. 설치 (10초)

```bash
npx create-laon-vaultguard
```

대화형 마법사가 실행됩니다. 언어 선택 → 스토리지 엔진(SQLite 권장) → LLM 제공자(DeepSeek 추천) → API 키 입력.

## 2. 첫 스캔

```bash
npx laon-vaultguard scan .            # 현재 폴더 스캔
npx laon-vaultguard scan ~/my-project # 특정 프로젝트
```

## 3. Pre-commit Hook

```bash
npx laon-vaultguard hook install      # 커밋 전 자동 검사
```

이후 `git commit` 시 자동으로 시크릿과 CI/DI를 검사하고 차단합니다.

## 4. Git 히스토리 감사

```bash
npx laon-vaultguard audit-history     # 전체 커밋 히스토리에서 CI/DI 검색
npx laon-vaultguard audit-history ~/old-project
```

## 사용 예시

### 예시 1: 개인 개발자 (DeepSeek 단독)

```bash
# .env
DEEPSEEK_API_KEY=sk-xxxx
LLM_PROVIDERS=deepseek
LLM_MODE=sequential
STORAGE_ENGINE=sqlite

# 실행
npx laon-vaultguard hook install
npx laon-vaultguard scan .
```

### 예시 2: 팀 (Claude + DeepSeek 교차검증)

```bash
# .env
CLAUDE_API_KEY=sk-ant-xxxx
DEEPSEEK_API_KEY=sk-xxxx
LLM_PROVIDERS=claude,deepseek
LLM_MODE=parallel
STORAGE_ENGINE=sqlite
DASHBOARD_TOKEN=team-secret
HOST=0.0.0.0

# 서버 실행 → 팀원들이 http://<IP>:3101/dashboard 접속
npm run dev
```

### 예시 3: 오프라인 (Ollama only)

```bash
brew install ollama
ollama pull deepseek-r1:8b

# .env
LLM_PROVIDERS=ollama
LLM_MODE=sequential
STORAGE_ENGINE=sqlite

npx laon-vaultguard scan .
```

### 예시 4: CI/CD (GitHub Actions)

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: LAON Secret Scan
        run: npx laon-vaultguard scan . --mode secrets
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
```

### 예시 5: CI/DI 감사 리포트

```bash
# 전체 git 히스토리에서 개인정보 검색
npx laon-vaultguard audit-history . > audit-report.txt

# 심각한 항목만 필터
npx laon-vaultguard audit-history . | grep CRITICAL

# 특정 기간 커밋만 검사
git log --since="2026-01-01" --pretty=format:"%H" | \
  while read hash; do
    git show $hash | npx laon-vaultguard scan --no-llm --stdin
  done
```

### 예시 6: SARIF → GitHub Code Scanning

```bash
npx laon-vaultguard export-sarif --output results.sarif
gh code scanning upload-sarif --file results.sarif
```

### 예시 7: Semgrep + LAON 통합

```bash
# 시크릿 탐지
npx laon-vaultguard scan . --mode secrets

# XSS/SQLi 탐지 (Semgrep)
semgrep --config="p/owasp-top-ten" --sarif -o semgrep.sarif .

# GitHub에 업로드
gh code scanning upload-sarif --file semgrep.sarif
```

### 예시 8: PDF 리포트

```bash
npm run dev &                                   # 서버 실행
curl http://localhost:3101/api/report/pdf -o report.html
open report.html                                # 브라우저 → Cmd+P → PDF 저장
```

## 다음 단계

- [CLI 매뉴얼](./CLI.md) — 모든 명령어 레퍼런스
- [Semgrep 통합](./SEMGREP_INTEGRATION.md) — XSS/SQLi 동시 스캔
- [Ollama 가이드](./Ollama.md) — 오프라인 LLM 설정
- [API 문서](./API.md) — REST API
- [LLM Prompt](./LLM_Prompt.md) — 시크릿 탐지 프롬프트
- [CIChecker Prompt](./CICHECKER_PROMPT.md) — CI/DI 감사 프롬프트
