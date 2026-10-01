# lab-agy: workspace de treino do workshop Antigravity

Este é o **seu** workspace de treino. Você copiou esta pasta para um lugar seu e vai trabalhar nela durante os três encontros.

- Nada aqui acessa dado real da empresa, BigQuery ou internet.
- Tudo roda com Python 3.12 e as bibliotecas de `requirements.txt` (versões fixas).
- O agente lê as regras em `AGENTS.md` e as skills em `.agents/skills/`.

## O que tem aqui
```
AGENTS.md                 regras que o agente segue em toda conversa
.agents/skills/           skills: procedimentos que viram /comando
.agents/hooks/            scripts que o Antigravity roda em momentos do ciclo do agente
CONTRATO/politica.yaml    o que só acontece depois de pedir (custo, dados, web)
CONTRATO/SCHEMAS/         o formato que todo loop.yaml precisa seguir
LOOPS/                    um processo por pasta (spec em YAML)
pedidos/                  pedidos de exemplo para testar as skills
evals/                    casos de teste e respostas gravadas (teste A/B sem custo)
FERRAMENTAS/              validar · mapa · ab · auditar · ci_local
adk/                      o mesmo loop escrito como agente do ADK (para casa)
.github/                  CI, modelo de PR e donos de cada área
.githooks/                portão que roda antes de cada commit
```

## Comandos
```
python FERRAMENTAS/validar.py            os LOOPS estão válidos?
python FERRAMENTAS/mapa.py               gera mapa.html (JSONCrack) do workspace
python FERRAMENTAS/ab.py --detalhe       compara as variantes A e B do prompt
python FERRAMENTAS/auditar.py .          segurança básica (segredo, permissão curinga, versão sem pin)
python FERRAMENTAS/ci_local.py           roda o CI inteiro na sua máquina
```
