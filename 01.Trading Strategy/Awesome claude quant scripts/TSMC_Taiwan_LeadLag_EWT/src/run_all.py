"""run_all.py — 전체 파이프라인 실행 (데이터 -> 선행지표 -> 백테스트)."""
import subprocess, sys, pathlib
here = pathlib.Path(__file__).resolve().parent
for script in ["leadlag.py", "backtest.py"]:
    print(f"\n{'='*60}\n  RUN {script}\n{'='*60}")
    subprocess.run([sys.executable, str(here / script)], check=True)
print("\n완료. results/ 폴더에서 json/csv/png 확인.")
