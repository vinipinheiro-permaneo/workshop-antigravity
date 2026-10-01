"""Hook Stop do Antigravity: o agente só encerra quando os loops passam no validador.

É o pilar VERIFICAR virando regra da ferramenta: "terminei" deixa de ser opinião do agente.
Para não prender o agente num ciclo, existe um limite de tentativas por conversa (pilar PARADA).
Responder `continue` bloqueia a parada; qualquer outro valor deixa o agente parar.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]          # .agents/hooks/este.py → raiz do workspace
ESTADO = Path(__file__).with_name("tentativas.json")
LIMITE = 3


def main() -> int:
    try:
        entrada = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        entrada = {}
    conversa = str(entrada.get("conversationId") or "sem-id")
    r = subprocess.run([sys.executable, str(RAIZ / "ferramentas" / "validar.py")], cwd=RAIZ,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        print(json.dumps({"decision": "stop"}))
        return 0
    tentativas = json.loads(ESTADO.read_text(encoding="utf-8")) if ESTADO.exists() else {}
    tentativas[conversa] = tentativas.get(conversa, 0) + 1
    ESTADO.write_text(json.dumps(tentativas), encoding="utf-8")
    if tentativas[conversa] > LIMITE:
        print(json.dumps({"decision": "stop",
                          "reason": f"o validador ainda falha depois de {LIMITE} tentativas: peça ajuda a uma pessoa"},
                         ensure_ascii=False))
        return 0
    print(json.dumps({"decision": "continue",
                      "reason": "Ainda não terminou: os loops não passam no validador.\n" + r.stdout[-1500:] +
                                "\nCorrija e rode `python ferramentas/validar.py` antes de encerrar."},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
