"""Checa toda skill em .agents/skills/: frontmatter, descrição útil, verificação e links.

  python FERRAMENTAS/checar_skills.py

Regras (da doc do Antigravity e da casa):
  - `description` diz O QUE a skill faz e QUANDO usar: é o que o agente lê para decidir ativar;
  - `name`, se existir, é kebab-case e igual ao nome da pasta;
  - o corpo tem uma seção "## Verificação" (a skill diz como provar que deu certo);
  - todo link relativo aponta para um arquivo que existe.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]


def checar(p: Path) -> list[str]:
    texto = p.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", texto, re.S)
    if not m:
        return ["sem frontmatter YAML (bloco entre --- no topo)"]
    fm, corpo, probs = yaml.safe_load(m.group(1)) or {}, m.group(2), []
    desc = str(fm.get("description") or "").strip()
    if len(desc) < 40:
        probs.append("description curta demais: diga o que faz e quando usar")
    if not re.search(r"\b(use|usar)\b", desc, re.I):
        probs.append("description não diz quando usar (ex.: 'Use quando...')")
    nome = fm.get("name")
    if nome is not None and (nome != p.parent.name or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", str(nome))):
        probs.append(f"name '{nome}' precisa ser kebab-case e igual à pasta '{p.parent.name}'")
    if not re.search(r"^##\s+Verifica[çc][ãa]o", corpo, re.M | re.I):
        probs.append("falta a seção '## Verificação'")
    for alvo in re.findall(r"\]\(([^)#\s]+)\)", corpo):
        if "://" not in alvo and not (p.parent / alvo).exists():
            probs.append(f"link quebrado: {alvo}")
    return probs


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    total = 0
    for p in sorted((RAIZ / ".agents" / "skills").glob("*/SKILL.md")):
        probs = checar(p)
        total += len(probs)
        print(f"{'✅' if not probs else '❌'} {p.parent.name}")
        for pr in probs:
            print(f"   • {pr}")
    print(f"\n{total} problema(s) nas skills")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
