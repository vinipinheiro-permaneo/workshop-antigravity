"""Valida todo LOOPS/*/loop.yaml: schema + referências cruzadas. Sem rede, sem LLM.

  python FERRAMENTAS/validar.py          relatório para pessoas
  python FERRAMENTAS/validar.py --json   relatório para máquinas (skills, CI)

Sai com código 0 quando tudo está válido e 1 quando existe algum problema.
"""
from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

RAIZ = Path(__file__).resolve().parents[1]
PILARES = {
    "verificadores": "pilar VERIFICAR: sem verificador, o agente não sabe se deu certo",
    "estado": "pilar ESTADO: onde fica o registro de cada execução",
    "parada": "pilar PARADA: quando o loop termina, bem ou mal",
}


def problema(codigo: str, mensagem: str, dica: str) -> dict:
    return {"codigo": codigo, "mensagem": mensagem, "dica": dica}


def ler_yaml(p: Path) -> dict:
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def traduzir(erro) -> dict:
    """Troca a mensagem do jsonschema por uma que um iniciante entende."""
    onde = "/".join(str(x) for x in erro.absolute_path) or "(raiz)"
    if erro.validator == "required":
        campo = erro.message.split("'")[1]
        return problema("SCHEMA-FALTA-CAMPO", f"falta o campo '{campo}' em {onde}",
                        PILARES.get(campo, "veja o campo no exemplo LOOPS/resumo-diario/loop.yaml"))
    if erro.validator == "enum":
        return problema("SCHEMA-VALOR", f"{onde}: valor {erro.instance!r} não é permitido",
                        f"use um destes: {', '.join(map(str, erro.validator_value))}")
    if erro.validator == "additionalProperties":
        return problema("SCHEMA-CAMPO-DESCONHECIDO", f"{onde}: {erro.message}",
                        "confira a grafia; campos novos precisam entrar no schema primeiro")
    return problema("SCHEMA", f"{onde}: {erro.message}", "compare com o schema em CONTRATO/SCHEMAS/loop.schema.json")


def validar_loop(p: Path, validador: Draft202012Validator, politicas: set[str]) -> list[dict]:
    try:
        d = ler_yaml(p)
    except yaml.YAMLError as e:
        return [problema("YAML-INVALIDO", f"o arquivo não é YAML válido: {e}".splitlines()[0],
                         "confira a indentação (2 espaços) e se não misturou tab com espaço")]
    probs = [traduzir(e) for e in sorted(validador.iter_errors(d), key=lambda e: list(e.absolute_path))]

    if d.get("id") and d["id"] != p.parent.name:
        probs.append(problema("ID-PASTA", f"id '{d['id']}' diferente da pasta '{p.parent.name}'",
                              "o id do loop precisa ser igual ao nome da pasta"))

    declarados = {v.get("id") for v in d.get("verificadores") or [] if isinstance(v, dict)}
    usados: dict[str, list[str]] = {}
    for e in d.get("etapas") or []:
        for v in (e or {}).get("verificadores") or []:
            usados.setdefault(v, []).append(str(e.get("id")))
    for v, etapas in sorted(usados.items()):
        if v not in declarados:
            probs.append(problema("REF-VERIFICADOR", f"{v} é usado na(s) etapa(s) {', '.join(etapas)} e não está declarado",
                                  "declare o verificador na lista `verificadores:` (id, tipo, bloqueante, comando)"))

    if d.get("verificadores") and not any(v.get("bloqueante") for v in d["verificadores"] if isinstance(v, dict)):
        probs.append(problema("SEM-BLOQUEANTE", "nenhum verificador bloqueante",
                              "pelo menos um verificador precisa poder reprovar (bloqueante: true)"))

    for pol in d.get("requer_aprovacao") or []:
        if pol not in politicas:
            parecido = difflib.get_close_matches(pol, sorted(politicas), n=1)
            dica = f"você quis dizer {parecido[0]}?" if parecido else "confira os ids em CONTRATO/politica.yaml"
            probs.append(problema("REF-POLITICA", f"requer_aprovacao cita {pol}, que não existe em CONTRATO/politica.yaml", dica))
    return probs


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    schema = json.loads((RAIZ / "CONTRATO" / "schemas" / "loop.schema.json").read_text(encoding="utf-8"))
    validador = Draft202012Validator(schema)
    politicas = {x["id"] for x in ler_yaml(RAIZ / "CONTRATO" / "politica.yaml").get("aprovacao_explicita") or []}

    LOOPS = []
    for p in sorted((RAIZ / "LOOPS").glob("*/loop.yaml")):
        probs = validar_loop(p, validador, politicas)
        LOOPS.append({"id": p.parent.name, "arquivo": p.relative_to(RAIZ).as_posix(), "valido": not probs, "problemas": probs})
    for pasta in sorted(x for x in (RAIZ / "LOOPS").iterdir() if x.is_dir() and not (x / "loop.yaml").exists()):
        LOOPS.append({"id": pasta.name, "arquivo": f"LOOPS/{pasta.name}/", "valido": False,
                      "problemas": [problema("SEM-LOOP-YAML", "pasta sem loop.yaml", "todo loop mora em LOOPS/<id>/loop.yaml")]})

    validos = sum(1 for x in LOOPS if x["valido"])
    resumo = {"validos": validos, "com_problema": len(LOOPS) - validos}
    if "--json" in argv:
        print(json.dumps({"LOOPS": LOOPS, "resumo": resumo}, ensure_ascii=False, indent=2))
    else:
        for x in LOOPS:
            print(f"{'✅' if x['valido'] else '❌'} {x['id']}  ({x['arquivo']})")
            for pr in x["problemas"]:
                print(f"   • {pr['mensagem']}\n     ↳ {pr['dica']}")
        print(f"\n{validos} válido(s) · {resumo['com_problema']} com problema")
    return 0 if resumo["com_problema"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
