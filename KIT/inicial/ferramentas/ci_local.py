"""Roda na sua máquina os passos `run:` do CI (.github/workflows/ci.yml), na mesma ordem.
CI é só isto: comandos que reprovam sozinhos, rodados sempre do mesmo jeito.

  python FERRAMENTAS/ci_local.py
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    wf = yaml.safe_load((RAIZ / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")) or {}
    for nome_job, job in (wf.get("jobs") or {}).items():
        print(f"== job {nome_job}")
        for passo in job.get("steps") or []:
            if "run" not in passo:
                print(f"   ⏭️  {passo.get('uses')} (só existe na nuvem)")
                continue
            cmd, nome = passo["run"].strip(), passo.get("name", passo["run"].strip())
            if cmd.startswith("pip install"):
                print(f"   ⏭️  {nome} (rode uma vez no setup)")
                continue
            if cmd.startswith("python "):
                cmd = f'"{sys.executable}" {cmd[len("python "):]}'
            print(f"   ▶️  {nome}", flush=True)
            r = subprocess.run(cmd, shell=True, cwd=RAIZ)
            if r.returncode != 0:
                print(f"   ❌ {nome} falhou (código {r.returncode}): na nuvem, o CI pararia aqui e o PR ficaria vermelho")
                return 1
            print(f"   ✅ {nome}")
    print("\nCI local: tudo verde ✅")
    return 0


if __name__ == "__main__":
    sys.exit(main())
