# Semgrep Integration — LAON VaultGuard Scan Orchestrator

> LAON VaultGuard를 시크릿 탐지 + Semgrep(XSS/SQLi/OWASP) 통합 오케스트레이터로 확장.  
> 두 도구의 결과를 SARIF로 통합하여 단일 대시보드에서 확인.

## 개요

LAON은 시크릿 탐지(패턴 + 멀티 LLM)에 특화. XSS, SQL Injection 등 웹 취약점은 Semgrep이 담당.  
두 결과를 **SARIF v2.1.0**으로 통합해 하나의 파이프라인으로 운영.

```
                         ┌─ LAON VaultGuard ──→ findings.sarif
git push / PR / cron ────┤                        │
                         └─ Semgrep ──────────→ semgrep.sarif
                                                   │
                                    ┌──────────────┘
                                    ▼
                            sarif-merge (통합)
                                    │
                                    ▼
                          GitHub Code Scanning
                                   or
                            LAON Dashboard
```

## 1. Semgrep 설치

```bash
# macOS
brew install semgrep

# Linux
pip install semgrep

# Docker
docker run -v $(pwd):/src returntocorp/semgrep semgrep --config=auto /src
```

## 2. OWASP Top 10 스캔 규칙

```bash
# 기본 규칙셋 (XSS, SQLi, CVE 포함)
semgrep --config=auto .

# OWASP Top 10 전용
semgrep --config="p/owasp-top-ten" .

# 특정 규칙만
semgrep --config="p/xss" .
semgrep --config="p/sql-injection" .
semgrep --config="p/javascript" .

# SARIF 출력
semgrep --config=auto . --sarif -o semgrep-results.sarif
```

## 3. LAON + Semgrep 통합 파이프라인

### GitHub Actions 예시

```yaml
name: LAON Security Scan
on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # LAON VaultGuard — 시크릿 탐지
      - name: LAON Secret Scan
        run: |
          cd LAON_VaultGuard && npm ci --omit=dev
          npx tsx src/sarif-export.ts --output ../laon-results.sarif
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}

      # Semgrep — XSS, SQLi, OWASP
      - name: Semgrep SAST Scan
        run: |
          pip install semgrep
          semgrep --config="p/owasp-top-ten" --sarif -o semgrep-results.sarif .

      # 통합 SARIF → GitHub Code Scanning
      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: laon-results.sarif
          category: laon-secrets

      - name: Upload Semgrep SARIF
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: semgrep-results.sarif
          category: semgrep-sast
```

### 로컬 통합 스크립트

```bash
#!/bin/bash
# run-all-scans.sh — LAON + Semgrep 통합 스캔

REPO_PATH=${1:-.}
OUTPUT_DIR="./scan-results"
mkdir -p "$OUTPUT_DIR"

echo "🔍 LAON VaultGuard — 시크릿 탐지..."
npx laon-vaultguard scan "$REPO_PATH"

echo "🔍 Semgrep — XSS/SQLi/OWASP 스캔..."
semgrep --config="p/owasp-top-ten" --config="p/xss" \
  --sarif -o "$OUTPUT_DIR/semgrep.sarif" "$REPO_PATH"

echo "📊 LAON SARIF export..."
npx laon-vaultguard export-sarif --output "$OUTPUT_DIR/laon.sarif"

echo "✅ 완료. 결과: $OUTPUT_DIR/"
echo "   GitHub에 업로드: gh code scanning upload-sarif --file $OUTPUT_DIR/laon.sarif"
```

## 4. SARIF 통합 결과 보기

```bash
# GitHub Code Scanning에서 확인
gh code scanning list

# 로컬에서 JSON 확인
cat laon-results.sarif | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d[\"runs\"][0][\"results\"])} findings')"
cat semgrep-results.sarif | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d[\"runs\"][0][\"results\"])} findings')"
```

## 5. Semgrep 규칙 커스터마이징

`.semgrep.yml` (레포 루트):

```yaml
rules:
  - id: detect-xss-innerhtml
    pattern: $X.innerHTML = $Y
    message: "Potential XSS via innerHTML. Use textContent or sanitize."
    languages: [javascript, typescript]
    severity: WARNING

  - id: detect-eval
    pattern: eval($X)
    message: "eval() with dynamic input may cause code injection."
    languages: [javascript, typescript]
    severity: ERROR
```

## 6. 범위 분담

| 취약점 유형 | 담당 도구 | 이유 |
|-------------|-----------|------|
| AWS/GCP/Azure 키 | **LAON** | 멀티 LLM 문맥 분석으로 정확도 높음 |
| GitHub/Slack 토큰 | **LAON** | 패턴 + LLM 교차검증 |
| DB 연결 문자열 | **LAON** | 비밀번호 포함 탐지 |
| JWT/세션 토큰 | **LAON** | 인코딩된 시크릿 탐지 |
| XSS (innerHTML 등) | **Semgrep** | AST 기반 패턴 매칭 |
| SQL Injection | **Semgrep** | 문자열 연결 패턴 감지 |
| Command Injection | **Semgrep** | `exec()` 위험 패턴 |
| Path Traversal | **Semgrep** | `fs.readFile()` 검증 누락 |
| Hardcoded Secrets (이중 확인) | **LAON + Semgrep** | 교차 검증으로 오탐 제거 |

Semgrep의 `generic` 모드로 시크릿 탐지도 가능하지만, LAON의 멀티 LLM 교차검증이 정확도 측면에서 우수합니다.
