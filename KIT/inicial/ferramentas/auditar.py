"""Auditoria de segurança básica do workspace (sem rede). Pega PADRÃO, não intenção:
revisão humana continua obrigatória.

  python FERRAMENTAS/auditar.py .          audita a pasta atual
  python FERRAMENTAS/auditar.py <pasta>    audita outra pasta (ex.: o Lab 6)
  python FERRAMENTAS/auditar.py . --json   relatório para máquinas

Sai com 1 se houver algum ERRO. Exceções intencionais vão em `.auditar-ignorar`,
uma por linha, no formato `caminho:REGRA  # motivo` (sem motivo, a exceção não vale).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PULAR_PASTAS = {".git", "__pycache__", "node_modules", ".venv", "venv"}
TEXTO = {".py", ".md", ".json", ".jsonl", ".yaml", ".yml", ".html", ".js", ".sh", ".ps1", ".txt", ".csv", ".toml", ".env", ""}
INSTRUCAO = re.compile(r"(^|/)(AGENTS|GEMINI|SKILL|agent)\.md$|(^|/)\.agents/.*\.md$")

REGRAS = [
    # id, severidade, padrão, onde aplicar (None = todo arquivo de texto), mensagem, como corrigir
    ("SEC-01", "ERRO", re.compile(r"(api[_-]?key|secret|token|senha|password)\b[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-\.]{12,}", re.I),
     None, "parece um segredo escrito no arquivo", "tire o valor do arquivo; use variável de ambiente ou cofre de segredos"),
    ("SEC-03", "ERRO", None, None, "biblioteca carregada de CDN sem versão fixa",
     "fixe a versão exata (ex.: pacote@1.2.3); sem versão, o código muda sem você saber"),
    ("SEC-04", "AVISO", re.compile(r"uses:\s*[\w.-]+/[\w.-]+@(v?\d[\w.]*)\s*(#.*)?$", re.M),
     None, "GitHub Action fixada por tag, não por SHA", "troque a tag pelo SHA do commit do release"),
    ("SEC-04", "ERRO", re.compile(r"uses:\s*[\w.-]+/[\w.-]+@(main|master|latest)\b"),
     None, "GitHub Action apontando para um branch", "fixe pelo SHA do release; branch muda a qualquer momento"),
    ("SEC-05", "ERRO", re.compile(r"\b(command|read_file|write_file|read_url|execute_url|mcp|unsandboxed)\(\*\)"),
     None, "permissão curinga (*)", "libere prefixos específicos, ex.: command(python FERRAMENTAS/validar.py)"),
    # o literal da flag é partido em dois para esta regra não acusar o próprio arquivo
    ("SEC-06", "ERRO", re.compile(r"[\"']?dangerouslySkipPermissions[\"']?\s*:\s*true|--dangerously-skip-" r"permissions", re.I),
     None, "agente configurado para não pedir permissão", "volte para o modo com aprovação; só troque depois de homologar o projeto"),
    ("SEC-06", "AVISO", re.compile(r"[\"']?toolPermission[\"']?\s*:\s*[\"']always-proceed", re.I),
     None, "execução de ferramenta sem revisão", "prefira request-review ou proceed-in-sandbox"),
    ("SEC-07", "ERRO", re.compile(r"ignore\s+(as|todas\s+as|all|previous|the)\s+(regras|instru[cç][oõ]es|instructions|rules)|"
                                  r"desconsidere\s+(as\s+)?(regras|instru[cç][oõ]es)|n[aã]o\s+(conte|avise|mostre)\s+(ao|para\s+o)\s+usu[aá]rio|"
                                  r"do\s+not\s+tell\s+the\s+user", re.I),
     INSTRUCAO, "instrução para o agente tenta desligar as regras (injeção de prompt)",
     "não use esta skill/regra; se veio de fora, reporte e apague"),
    ("SEC-08", "ERRO", re.compile(r"\b(curl|wget|iwr|Invoke-WebRequest)\b[^\n|]*\|\s*(sh|bash|iex|python)\b", re.I),
     None, "baixa e executa código da internet sem revisão", "baixe, leia, fixe a versão e só então execute"),
    ("SEC-09", "AVISO", re.compile(r"roles/(editor|owner)\b"),
     None, "papel amplo demais no GCP", "crie uma conta de serviço com o papel mínimo para a tarefa"),
    ("SEC-10", "AVISO", re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"),
     None, "parece CPF (dado pessoal)", "dado real de cliente não entra no workspace (POL-DADOS); use dado fictício mascarado"),
    ("SEC-11", "ERRO", re.compile(r"^\s*permissions:\s*write-all\b", re.M),
     None, "CI com permissão de escrita em tudo", "use `permissions: contents: read` e libere só o necessário por job"),
    ("SEC-12", "AVISO", re.compile(r"[\"']decision[\"']\s*:\s*[\"']allow[\"']"),
     re.compile(r"(^|/)hooks/[^/]+\.(py|sh|ps1|js)$"), "hook de segurança que libera por conta própria",
     "hook só restringe: responda ask e deixe a permissão normal decidir"),
]
CDN = re.compile(r"https://(esm\.sh|unpkg\.com|cdn\.jsdelivr\.net/npm)/((?:@[\w.-]+/)?[\w.-]+)(@[\w.^~*-]+)?")


def ignoradas(raiz: Path) -> tuple[set[tuple[str, str]], list[str]]:
    p, ok, sem_motivo = raiz / ".auditar-ignorar", set(), []
    if p.exists():
        for linha in p.read_text(encoding="utf-8").splitlines():
            if not linha.strip() or linha.lstrip().startswith("#"):
                continue
            alvo, _, motivo = linha.partition("#")
            if not motivo.strip():
                sem_motivo.append(alvo.strip())
                continue
            caminho, _, regra = alvo.strip().rpartition(":")
            ok.add((caminho, regra))
    return ok, sem_motivo


def arquivos(raiz: Path):
    for p in sorted(raiz.rglob("*")):
        if p.is_file() and not (PULAR_PASTAS & set(p.relative_to(raiz).parts)) and p.suffix.lower() in TEXTO:
            yield p


def auditar(raiz: Path) -> list[dict]:
    achados = []
    ok, sem_motivo = ignoradas(raiz)
    for s in sem_motivo:
        achados.append({"regra": "SEC-00", "sev": "AVISO", "arquivo": ".auditar-ignorar", "linha": 0,
                        "msg": f"exceção sem motivo não vale: {s}", "dica": "escreva `# motivo` no fim da linha"})

    def add(regra, sev, rel, n, msg, dica):
        if (rel, regra) not in ok:
            achados.append({"regra": regra, "sev": sev, "arquivo": rel, "linha": n, "msg": msg, "dica": dica})

    for p in arquivos(raiz):
        rel = p.relative_to(raiz).as_posix()
        try:
            texto = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if p.name == ".env":
            gi = raiz / ".gitignore"
            if not (gi.exists() and re.search(r"^\.env\b", gi.read_text(encoding="utf-8"), re.M)):
                add("SEC-02", "ERRO", rel, 1, ".env fora do .gitignore (vai parar no git)", "adicione `.env` ao .gitignore")
        for regra, sev, rx, onde, msg, dica in REGRAS:
            if onde is not None and not onde.search(rel):
                continue
            if regra == "SEC-03":
                for m in CDN.finditer(texto):
                    versao = m.group(3) or ""
                    if not versao or any(c in versao for c in "^~*") or "latest" in versao:
                        add(regra, sev, rel, texto.count("\n", 0, m.start()) + 1, f"{msg}: {m.group(0)}", dica)
                continue
            for m in rx.finditer(texto):
                add(regra, sev, rel, texto.count("\n", 0, m.start()) + 1, msg, dica)
    return achados


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in argv[1:] if not a.startswith("--")]
    raiz = Path(args[0] if args else ".").resolve()
    achados = auditar(raiz)
    erros = sum(1 for a in achados if a["sev"] == "ERRO")
    if "--json" in argv:
        print(json.dumps({"achados": achados, "erros": erros, "avisos": len(achados) - erros}, ensure_ascii=False, indent=2))
    else:
        for a in sorted(achados, key=lambda a: (a["sev"] != "ERRO", a["arquivo"], a["linha"])):
            print(f"{'🔴 ERRO ' if a['sev'] == 'ERRO' else '🟡 AVISO'} {a['regra']}  {a['arquivo']}:{a['linha']}  {a['msg']}\n"
                  f"         ↳ {a['dica']}")
        print(f"\n{erros} erro(s) · {len(achados) - erros} aviso(s) em {raiz.name}")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
