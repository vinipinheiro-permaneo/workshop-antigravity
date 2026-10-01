"""Gera mapa.html: o workspace (ou qualquer JSON) como grafo navegável no JSONCrack.

  python FERRAMENTAS/mapa.py                      mapa do workspace (LOOPS, skills, hooks, política)
  python FERRAMENTAS/mapa.py --arquivo saida.json mapa de um JSON qualquer (ex.: a saída do agy -p)

O arquivo gerado abre direto no navegador. Precisa de internet só para baixar o JSONCrack
(versões fixas no código: fixar versão é defesa de cadeia de suprimentos, veja o Dia 3).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
CDN = {
    "css": "https://esm.sh/jsoncrack-react@1.0.5/dist/index.css",
    "react": "https://esm.sh/react@18.3.1",
    "dom": "https://esm.sh/react-dom@18.3.1/client",
    "jc": "https://esm.sh/jsoncrack-react@1.0.5?deps=react@18.3.1,react-dom@18.3.1",
}
HTML = """<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- GERADO por FERRAMENTAS/mapa.py: NÃO EDITAR À MÃO -->
<link rel="stylesheet" href="{css}">
<style>html,body,#mapa{{margin:0;height:100%;background:#1e1e2e;color:#cdd6f4;font:14px system-ui,sans-serif}}
#topo{{position:fixed;top:8px;left:12px;z-index:5;background:#181825cc;padding:6px 12px;border-radius:8px}}</style>
</head><body><div id="topo">🗺️ {titulo}</div><div id="mapa">carregando o JSONCrack…</div>
<script type="module">
const dados = {dados};
try {{
  const [R, D, J] = await Promise.all([import("{react}"), import("{dom}"), import("{jc}")]);
  const React = R.default || R;
  document.getElementById("mapa").textContent = "";
  D.createRoot(document.getElementById("mapa")).render(
    React.createElement(J.JSONCrack, {{json: dados, theme: "dark", layoutDirection: "RIGHT", showControls: true, showGrid: true}}));
}} catch (e) {{
  document.getElementById("mapa").textContent = "Não consegui carregar o JSONCrack (precisa de internet). Os dados estão no código desta página.";
}}
</script></body></html>
"""


def frontmatter(p: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---", p.read_text(encoding="utf-8"), re.S)
    return yaml.safe_load(m.group(1)) if m else {}


def workspace() -> dict:
    LOOPS = {}
    for p in sorted((RAIZ / "LOOPS").glob("*/loop.yaml")):
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        LOOPS[p.parent.name] = {
            "titulo": d.get("titulo"),
            "gatilho": (d.get("gatilho") or {}).get("tipo"),
            "etapas": [f"{e.get('id')}. {e.get('nome')}" for e in d.get("etapas") or []],
            "verificadores": [v.get("id") for v in d.get("verificadores") or []] or "⚠️ nenhum",
            "estado": (d.get("estado") or {}).get("onde", "⚠️ sem estado"),
            "parada": (d.get("parada") or {}).get("sucesso", "⚠️ sem parada"),
        }
    skills = {p.parent.name: (frontmatter(p).get("description") or "").strip()
              for p in sorted((RAIZ / ".agents" / "skills").glob("*/SKILL.md"))}
    hooks_p = RAIZ / ".agents" / "hooks.json"
    hooks = json.loads(hooks_p.read_text(encoding="utf-8")) if hooks_p.exists() else "ainda não existe (Lab 1 🔴)"
    pol = yaml.safe_load((RAIZ / "CONTRATO" / "politica.yaml").read_text(encoding="utf-8")) or {}
    return {
        "workspace": RAIZ.name,
        "regras (AGENTS.md)": "carregadas sempre, em toda conversa",
        "skills (.agents/skills)": skills or "nenhuma",
        "hooks (.agents/hooks.json)": hooks,
        "politica": {x["id"]: x["escopo"] for x in pol.get("aprovacao_explicita") or []},
        "LOOPS": LOOPS,
    }


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--arquivo" in argv:
        origem = Path(argv[argv.index("--arquivo") + 1])
        dados, titulo = json.loads(origem.read_text(encoding="utf-8-sig")), f"JSON: {origem.name}"
    else:
        dados, titulo = workspace(), f"Workspace {RAIZ.name}"
    js = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")
    (RAIZ / "mapa.html").write_text(HTML.format(titulo=titulo, dados=js, **CDN), encoding="utf-8")
    print(f"mapa.html gerado ({titulo}). Abra no navegador.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
