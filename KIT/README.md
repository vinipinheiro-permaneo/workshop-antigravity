# Kit de labs do workshop Antigravity

```
inicial/          o workspace de partida: cada dupla copia para uma pasta DELA (lab-agy)
gabarito/labN/    só os arquivos que o lab N muda (sobrescreva por cima de uma cópia)
gabarito/RELATORIO-lab6.md   o relatório esperado da caça ao risco
caca-ao-risco/    o workspace "de outro time" do Lab 6: só leia e audite, não rode nada
testar.py         autoteste: aplica cada gabarito numa cópia temporária e confere o resultado
```

## Labs
| Lab | Encontro | 🟢 trilha guiada | 🔴 desafio | Autoteste confere |
|---|---|---|---|---|
| 1 | Dia 1 | regras da dupla no `AGENTS.md` + skill `/reformular-pedido` | hook `PreToolUse` que barra `bq query` sem `--dry_run` | skill com frontmatter e recurso; `hooks.json` ligado; decisões do hook |
| 2 | Dia 2 | consertar `LOOPS/triagem-de-pedidos/loop.yaml` com o schema e o validador | skill `/validar-loops` + hook `Stop` que verifica antes de parar | validador verde; hook `Stop` bloqueia 3 vezes e libera na 4ª |
| 3 | Dia 2 | `mapa.py` (JSONCrack) do workspace e da saída do `agy -p` | CONTRATO de saída com `--json-schema` + `conferir_saida.py` | saída no CONTRATO passa; fora do CONTRATO reprova |
| 4 | Dia 3 | branch, pre-commit, `ci_local.py`, descrição do PR | repositório no GitHub, PR com Actions, passo novo no CI | CI local vermelho antes do Lab 2 e verde depois; skill sem verificação reprova |
| 5 | Dia 3 | ler a regra e decidir o A/B com `ab.py` | escrever o caso adversarial `adv-03` | B vence; com `adv-03`, A reprova 3/3 adversariais |
| 6 | Dia 3 (extensão) | `auditar.py ../caca-ao-risco` e a tabela de riscos | achar o que o scanner não pega; corrigir até 0 erro | 12 tipos de risco achados; 0 erro depois do gabarito |

## Antes de cada turma
```
python kit/testar.py
```
Precisa de Python 3.12 com `PyYAML` e `jsonschema`. Não usa rede, modelo nem nuvem. Se o `google-adk` estiver instalado, ele também confere a estrutura do agente ADK, sem chamar o modelo.

## Custo e segurança
- Tudo do kit roda local e sem custo. O que usa modelo (`agy -p`, SDK, `adk run` e `adk web`) está marcado com 💲 nos roteiros e consome a cota ou a conta de quem roda.
- `evals/respostas-*.jsonl` e `caca-ao-risco/` são **dados de treino inventados**: nenhuma chave, CPF ou e-mail é real.
- O `caca-ao-risco/` guarda o pacote suspeito fora de `.agents/` de propósito, para o Antigravity não carregar a skill maliciosa por engano.
