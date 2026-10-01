"""Teste A/B de prompt SEM gastar: compara respostas já gravadas de duas variantes.

  python FERRAMENTAS/ab.py                  compara evals/respostas-A.jsonl × evals/respostas-B.jsonl
  python FERRAMENTAS/ab.py --detalhe        mostra o motivo de cada reprovação
  python FERRAMENTAS/ab.py --json           relatório para máquinas
  python FERRAMENTAS/ab.py --falhar-se-pior sai com 1 se a candidata perder pela regra (portão de CI)

A regra de decisão fica em evals/regra.yaml e é escrita ANTES de olhar o resultado.
As respostas gravadas são dados de treino inventados para o workshop.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parents[1]
EVALS = RAIZ / "evals"
Z = 1.96  # intervalo de 95%


def jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def wilson(x: int, n: int) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = x / n
    base = 1 + Z * Z / n
    centro = (p + Z * Z / (2 * n)) / base
    meia = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / base
    return max(0.0, centro - meia), min(1.0, centro + meia)


def avaliar(caso: dict, saida: str) -> list[str]:
    """Checagens determinísticas: nada de LLM julgando LLM neste lab."""
    c, motivos = caso.get("criterios") or {}, []
    for campo in c.get("campos") or []:
        if not re.search(rf"^\s*\**{re.escape(campo)}\**\s*:", saida, re.I | re.M):
            motivos.append(f"falta o campo '{campo}'")
    for rx in c.get("proibido") or []:
        if re.search(rx, saida, re.I):
            motivos.append(f"contém o proibido /{rx}/")
    for rx in c.get("exigido") or []:
        if not re.search(rx, saida, re.I):
            motivos.append(f"não contém o exigido /{rx}/")
    limite = c.get("max_palavras")
    if limite and len(saida.split()) > limite:
        motivos.append(f"{len(saida.split())} palavras (limite {limite})")
    return motivos


def resumo_variante(nome: str, casos: dict, respostas: list[dict]) -> dict:
    linhas, ignoradas = [], []
    for r in respostas:
        caso = casos.get(r["caso"])
        if caso is None:
            ignoradas.append(r["caso"])
            continue
        motivos = avaliar(caso, r["saida"])
        linhas.append({"caso": r["caso"], "tipo": caso.get("tipo", "normal"), "aprovada": not motivos, "motivos": motivos,
                       "tokens": int(r.get("tokens_entrada", 0)) + int(r.get("tokens_saida", 0))})
    n = len(linhas)
    aprov = sum(1 for x in linhas if x["aprovada"])
    adv = [x for x in linhas if x["tipo"] == "adversarial"]
    tokens = sum(x["tokens"] for x in linhas)
    lo, hi = wilson(aprov, n)
    return {"variante": nome, "n": n, "aprovadas": aprov, "taxa": aprov / n if n else 0.0, "ic95": [lo, hi],
            "tokens_por_resposta": tokens / n if n else 0.0,
            "tokens_por_aprovada": tokens / aprov if aprov else math.inf,
            "adversariais": {"total": len(adv), "aprovadas": sum(1 for x in adv if x["aprovada"])},
            "linhas": linhas, "ignoradas": ignoradas}


def decidir(regra: dict, ctl: dict, cand: dict) -> tuple[bool, list[str]]:
    motivos = []
    g = regra.get("guarda_corpos") or {}
    if g.get("adversariais_aprovados") == "todos" and cand["adversariais"]["aprovadas"] < cand["adversariais"]["total"]:
        motivos.append("candidata reprovou em caso adversarial (guarda-corpo de segurança)")
    teto = g.get("custo_por_aprovada_max_vs_controle")
    if teto and cand["tokens_por_aprovada"] > teto * ctl["tokens_por_aprovada"]:
        motivos.append(f"custo por resposta aprovada acima de {teto}× o controle")
    if cand["taxa"] < ctl["taxa"]:
        motivos.append("taxa de aprovação menor que a do controle")
    return not motivos, motivos


def pct(x: float) -> str:
    return f"{x * 100:.0f}%"


def milhar(x: float) -> str:
    return "∞" if math.isinf(x) else f"{x:,.0f}".replace(",", ".")


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    regra = yaml.safe_load((EVALS / "regra.yaml").read_text(encoding="utf-8")) or {}
    casos = {c["id"]: c for c in jsonl(EVALS / "casos.jsonl")}
    ctl_nome, cand_nome = regra.get("controle", "A"), regra.get("candidata", "B")
    ctl = resumo_variante(ctl_nome, casos, jsonl(EVALS / f"respostas-{ctl_nome}.jsonl"))
    cand = resumo_variante(cand_nome, casos, jsonl(EVALS / f"respostas-{cand_nome}.jsonl"))
    vence, motivos = decidir(regra, ctl, cand)
    minimo = int(regra.get("amostra_minima_por_variante") or 30)
    avisos = []
    if min(ctl["n"], cand["n"]) < minimo:
        avisos.append(f"amostra pequena ({min(ctl['n'], cand['n'])} < {minimo} por variante): trate como indício, não como prova")
    if ctl["ic95"][1] >= cand["ic95"][0] and cand["ic95"][1] >= ctl["ic95"][0]:
        avisos.append("os intervalos de 95% se sobrepõem: a diferença pode ser acaso")
    for v in (ctl, cand):
        if v["ignoradas"]:
            avisos.append(f"respostas da variante {v['variante']} sem caso em casos.jsonl (ignoradas): {', '.join(v['ignoradas'])}")

    if "--json" in argv:
        print(json.dumps({"controle": ctl, "candidata": cand, "candidata_vence": vence, "motivos": motivos, "avisos": avisos},
                         ensure_ascii=False, indent=2, default=str))
    else:
        print(f"{'variante':<9}{'n':>4}{'aprov.':>8}{'taxa':>7}{'IC 95%':>13}{'tokens/resp':>13}{'tokens/aprov.':>15}{'adversariais':>14}")
        for v in (ctl, cand):
            ic = f"{pct(v['ic95'][0])}–{pct(v['ic95'][1])}"
            adv = f"{v['adversariais']['aprovadas']}/{v['adversariais']['total']}"
            print(f"{v['variante']:<9}{v['n']:>4}{v['aprovadas']:>8}{pct(v['taxa']):>7}{ic:>13}"
                  f"{milhar(v['tokens_por_resposta']):>13}{milhar(v['tokens_por_aprovada']):>15}{adv:>14}")
        print(f"\ndiferença ({cand_nome} − {ctl_nome}): {(cand['taxa'] - ctl['taxa']) * 100:+.0f} pontos percentuais")
        print(f"decisão pela regra de evals/regra.yaml: {'✅ ' + cand_nome + ' vence' if vence else '❌ ' + cand_nome + ' não vence'}")
        for m in motivos:
            print(f"   • {m}")
        for a in avisos:
            print(f"⚠️  {a}")
        if "--detalhe" in argv:
            for v in (ctl, cand):
                print(f"\nreprovações da variante {v['variante']}:")
                for x in v["linhas"]:
                    if not x["aprovada"]:
                        print(f"   {x['caso']} ({x['tipo']}): {'; '.join(x['motivos'])}")
    if "--falhar-se-pior" in argv and not vence:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
