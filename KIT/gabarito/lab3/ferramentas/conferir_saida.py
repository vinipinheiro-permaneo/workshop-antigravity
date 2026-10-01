"""Confere a saída do `agy -p ... --output-format json --json-schema <schema>` contra o schema.

  python FERRAMENTAS/conferir_saida.py saida.json CONTRATO/SCHEMAS/status.schema.json

O resultado estruturado vem no campo `structured_output` da saída JSON do agy.
Confiar sem conferir é o erro: o schema é o CONTRATO, este script é o fiscal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(argv) != 3:
        print(__doc__)
        return 2
    saida = json.loads(Path(argv[1]).read_text(encoding="utf-8-sig"))
    dado = saida.get("structured_output", saida) if isinstance(saida, dict) else saida
    erros = sorted(Draft202012Validator(json.loads(Path(argv[2]).read_text(encoding="utf-8"))).iter_errors(dado),
                   key=lambda e: list(e.absolute_path))
    for e in erros:
        print(f"❌ {'/'.join(map(str, e.absolute_path)) or '(raiz)'}: {e.message}")
    print("✅ saída segue o CONTRATO" if not erros else f"\n{len(erros)} desvio(s) do CONTRATO")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
