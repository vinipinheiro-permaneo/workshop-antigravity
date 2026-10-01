"""Hook PreToolUse do Antigravity: guarda de custo (POL-CUSTO) como código.

O Antigravity manda o JSON da chamada no stdin e lê a decisão no stdout.
Regra de ouro: hook de segurança só RESTRINGE. Quando não tem opinião, responde `ask`,
que devolve a decisão para o fluxo normal de permissão (nunca libera por conta própria).
Cada decisão vai para decisoes.jsonl (append-only), que serve de trilha de auditoria.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

LOG = Path(__file__).with_name("decisoes.jsonl")


def decidir(cmd: str) -> tuple[str, str]:
    if re.search(r"\bbq\b", cmd) and re.search(r"\bquery\b", cmd):
        if "--dry_run" in cmd or "--dry-run" in cmd:
            return "ask", "estimativa (dry-run) não cobra; confira os bytes antes da consulta real"
        return "deny", ("POL-CUSTO: rode primeiro `bq query --dry_run ...`, mostre os bytes estimados "
                        "e peça aprovação antes da consulta real")
    if re.search(r"\b(bq|gcloud)\b", cmd):
        return "force_ask", "comando de nuvem (POL-CUSTO): confirme com a pessoa antes"
    if re.search(r"\brm\s+-rf\b|\bRemove-Item\b.*-Recurse", cmd, re.I):
        return "force_ask", "apagar em massa: confirme o caminho antes"
    return "ask", ""


def main() -> int:
    try:
        entrada = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        entrada = {}
    args = (entrada.get("toolCall") or {}).get("args") or {}
    cmd = str(args.get("CommandLine") or args.get("commandLine") or "")
    decisao, motivo = decidir(cmd)
    saida = {"decision": decisao, **({"reason": motivo} if motivo else {})}
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"quando": dt.datetime.now().isoformat(timespec="seconds"), "comando": cmd[:200],
                                "decisao": decisao}, ensure_ascii=False) + "\n")
    except OSError:
        pass  # o log nunca derruba o agente
    print(json.dumps(saida, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
