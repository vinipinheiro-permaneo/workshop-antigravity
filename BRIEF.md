# Workshop Antigravity: pedido e escopo

## 1. Pedido (verbatim, 2026-09-29)
> me faça um workshop de Antigravity para 3 dias:
> 1º dia - Explorar o maximo do Antigravity (slash commands, skills, agent plataform, ADK e etc);
> 2º dia - Aplicando conceitos de eng. de software (Arquitetura de diretorios, automatizações, yaml, jsoncrack e etc)
> 3º dia - Aplicando conceitos de DataOps e qualidade (Git, CI/CD, Develop, QA, Code Review PR, A/B test, sec e etc)
>
> baseado no trabalho que fizemos agora

(Uma primeira versão do pedido, interrompida, tinha "DevOps" no Dia 3 e não citava agent platform, ADK, jsoncrack nem sec.)

## 2. Respostas às perguntas de escopo (2026-09-29)
| Pergunta | Resposta do responsável |
|---|---|
| Quem faz o workshop? | Time misto (analistas + estagiários): trilha 🟢 guiada e desafio 🔴 em cada lab |
| Carga horária de cada dia? | "3 dias, sendo 1h ~ 1h30 cada" |
| Formato do material? | ".html, .md, kit labs" |
| Pode ler a doc oficial online? | Sim, só leitura (antigravity.google/docs e a doc do ADK) |

## 3. Premissas assumidas (ditas antes das perguntas, sem objeção)
- O material fica numa missão nova em `LOOP-ENGINEERING-CLAUDE`.
- Os labs rodam numa pasta sandbox que cada participante cria. Nunca em `MAIN_AG` nem nesta pasta.
- Custo zero por padrão. O que depende de modelo pago, conta ou GCP fica marcado como opcional (💲).

## 4. Estado das ferramentas na máquina (2026-09-29)
- Antigravity CLI `agy` 1.2.13, com a doc embutida (skills `antigravity-guide` e `agy-customizations`).
- `google-adk` 2.3.0. A doc oficial já está na 2.10.0: os labs seguem a versão instalada.
- `gh` (GitHub CLI) instalado; Python 3.12 com PyYAML 6.0.3 e jsonschema 4.26.0.
- A IDE Antigravity e o app Antigravity 2.0 não foram encontrados nesta máquina: os labs usam o CLI, e o app e a IDE entram como demonstração.
