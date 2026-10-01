---
titulo: "Glossário"
---
# Glossário

Cada termo tem duas leituras. A 🟢 **Simples** é para quem está começando, e a 🔴 **Técnica** é para quem já programa. A linha 🧭 diz onde o termo aparece no workshop.

## Agentes e Antigravity

### Agente
🟢 **Simples:** um programa que recebe um pedido em português e faz o trabalho: lê e escreve arquivos e roda comandos, pedindo licença no que é arriscado.
🔴 **Técnico:** um LLM rodando em loop com ferramentas (arquivos, terminal, MCP). A cada volta, ele decide o próximo passo a partir do contexto [SRC-02].
🧭 **No workshop:** [Dia 1 · Abertura](dia-1.md#d1-abertura)

### LLM
🟢 **Simples:** o "cérebro" que escreve as respostas. É um modelo que aprendeu, com muito texto, a continuar textos.
🔴 **Técnico:** Large Language Model, que prevê o próximo token. No Antigravity, você escolhe o modelo com `/model` [SRC-06].
🧭 **No workshop:** [Dia 1 · Demo](dia-1.md#d1-demo)

### Prompt
🟢 **Simples:** o pedido que você escreve para o agente.
🔴 **Técnico:** o texto que entra no modelo: o seu pedido, as rules carregadas, as descrições das skills e o histórico da conversa [SRC-03].
🧭 **No workshop:** [Dia 3 · Lab 5](dia-3.md#d3-lab5)

### Contexto
🟢 **Simples:** tudo o que o agente "tem na cabeça" naquele momento. Tem tamanho máximo.
🔴 **Técnico:** a janela de tokens enviada ao modelo a cada chamada. `/context` mostra quanto está ocupado [SRC-06].
🧭 **No workshop:** [Dia 2 · Abertura](dia-2.md#d2-abertura)

### Token
🟢 **Simples:** um pedaço de palavra que o modelo conta. É a unidade de tamanho e de custo.
🔴 **Técnico:** a unidade de tokenização do modelo. Limites e consumo são medidos em tokens; as rules sempre ativas, por exemplo, dividem um orçamento de 20.000 tokens [SRC-03].
🧭 **No workshop:** [Dia 2 · Abertura](dia-2.md#d2-abertura)

### CLI
🟢 **Simples:** um programa que você usa digitando comandos no terminal, sem janelas nem botões.
🔴 **Técnico:** Command-Line Interface. O CLI do Antigravity é o `agy` [SRC-01].
🧭 **No workshop:** [Dia 1 · Demo](dia-1.md#d1-demo)

### Slash command
🟢 **Simples:** um atalho que começa com barra, como `/help`, para pedir uma ação específica.
🔴 **Técnico:** um comando interno do agy. Toda skill do workspace vira um slash command `/nome` [SRC-06] [SRC-08].
🧭 **No workshop:** [Dia 1 · Demo](dia-1.md#d1-demo)

### Rule
🟢 **Simples:** uma regra da casa, escrita num arquivo de texto, que o agente segue sempre.
🔴 **Técnico:** `AGENTS.md` ou `GEMINI.md` (sempre ativos), ou `.agents/rules/*.md` com gatilho `always_on`, `model_decision`, `glob` ou `manual`. O limite é 24 KB por arquivo [SRC-03] [SRC-08].
🧭 **No workshop:** [Dia 1 · Lab 1](dia-1.md#d1-lab1)

### Skill
🟢 **Simples:** um manual de procedimento que o agente abre quando precisa, como "reformular um pedido".
🔴 **Técnico:** a pasta `.agents/skills/<nome>/` com um `SKILL.md` (frontmatter com name e description, e os passos no corpo). Até ativar, só a descrição fica no contexto [SRC-03].
🧭 **No workshop:** [Dia 1 · Lab 1](dia-1.md#d1-lab1)

### Hook
🟢 **Simples:** um porteiro automático. É um script que roda em momentos do trabalho do agente e pode barrar uma ação.
🔴 **Técnico:** um comando registrado em `.agents/hooks.json` para `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation` ou `Stop`, que conversa por JSON no stdin e no stdout [SRC-03].
🧭 **No workshop:** [Dia 1 · Lab 1](dia-1.md#d1-lab1) · [Dia 2 · Lab 2](dia-2.md#d2-lab2)

### Plugin
🟢 **Simples:** um pacote que junta várias customizações para instalar de uma vez.
🔴 **Técnico:** uma pasta com `plugin.json` e as subpastas `skills/`, `rules/`, `hooks.json` e `mcp_config.json`, gerenciada por `agy plugin` [SRC-01] [SRC-03].
🧭 **No workshop:** [Dia 2 · Automações](dia-2.md#d2-automacao)

### MCP
🟢 **Simples:** um "adaptador de tomada" que liga o agente a outros sistemas: banco, Jira, navegador.
🔴 **Técnico:** Model Context Protocol. Os servidores ficam em `mcp_config.json`, rodando local (`command`/`args`) ou remoto (`serverUrl`) [SRC-03] [SRC-08].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### Subagente
🟢 **Simples:** um ajudante que o agente principal chama para cuidar de uma parte do trabalho.
🔴 **Técnico:** um agente com contexto próprio: nativo (`research`, `browser`, `self`) ou customizado em `.agents/agents/<nome>.md` [SRC-08].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### Sandbox
🟢 **Simples:** uma "caixa de areia" onde o agente trabalha sem conseguir estragar o resto do computador.
🔴 **Técnico:** execução com terminal restrito, sem rede por padrão e sem acesso a `.env` e `~/.ssh`. Liga com `agy --sandbox`; no Windows, a doc do CLI ainda não confirma que funciona [SRC-01] [SRC-07].
🧭 **No workshop:** [Comece aqui](README.md)

### Permissão
🟢 **Simples:** a autorização que o agente pede antes de fazer algo arriscado.
🔴 **Técnico:** o nível em `toolPermission` (`request-review`, `proceed-in-sandbox`, `strict` ou `always-proceed`) mais as regras `allow`, `ask` e `deny`. Quando elas conflitam, `deny` vence [SRC-06] [SRC-07].
🧭 **No workshop:** [Dia 1 · Demo](dia-1.md#d1-demo)

### Workspace
🟢 **Simples:** a pasta do projeto onde o agente trabalha.
🔴 **Técnico:** a raiz de trabalho da sessão. O agente procura `.agents/` e `AGENTS.md` subindo da pasta atual até a raiz do repositório [SRC-03].
🧭 **No workshop:** [Comece aqui](README.md)

### Artifact
🟢 **Simples:** um documento que o agente produz para você revisar: um plano, um diff, uma captura de tela.
🔴 **Técnico:** Implementation Plan, diffs, diagramas e gravações. No CLI, `Ctrl+R` abre o painel, e `y` ou `n` aprova ou rejeita [SRC-08].
🧭 **No workshop:** [Dia 1 · Demo](dia-1.md#d1-demo)

### Print mode
🟢 **Simples:** um jeito de usar o agente sem conversa. Um pedido, uma resposta, pronto para usar em scripts.
🔴 **Técnico:** `agy -p "..." --output-format json`. Com `--json-schema`, o resultado vem no campo `structured_output` [SRC-01] [SRC-08].
🧭 **No workshop:** [Dia 2 · Lab 3](dia-2.md#d2-lab3)

### SDK
🟢 **Simples:** uma caixa de peças para usar uma ferramenta de dentro do seu próprio programa.
🔴 **Técnico:** Software Development Kit. O do Antigravity é o pacote Python `google-antigravity`, com a classe `Agent`, que só lê por padrão [SRC-02].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### ADK
🟢 **Simples:** o kit do Google para construir o seu próprio agente em código.
🔴 **Técnico:** Agent Development Kit, com `LlmAgent`, `LoopAgent`, `SequentialAgent`, `ParallelAgent` e grafos (`Workflow`). A CLI tem `adk create`, `run`, `web`, `eval` e `deploy` [SRC-05] [SRC-10].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### LoopAgent
🟢 **Simples:** um agente que repete um ciclo (escrever, revisar) até dar certo ou chegar a um limite.
🔴 **Técnico:** um agente de workflow do ADK. Ele roda os `sub_agents` em sequência até alguém chamar `exit_loop` (que dispara um *escalate*) ou até completar `max_iterations` [SRC-05] [SRC-10].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### Agent Platform
🟢 **Simples:** o lugar no Google Cloud onde agentes ficam no ar para outras pessoas usarem.
🔴 **Técnico:** Google Cloud Agent Platform. O runtime gerenciado se chama Agent Runtime (antes, Agent Engine) e é um serviço pago; o deploy é feito com `adk deploy agent_engine` [SRC-10].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### Cloud Run
🟢 **Simples:** um serviço do Google que deixa um programa no ar sem você cuidar de servidor.
🔴 **Técnico:** a plataforma serverless de contêineres do Google Cloud. O ADK publica nela com `adk deploy cloud_run` [SRC-05].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

### IAP
🟢 **Simples:** um porteiro de login. Só entra quem tem conta da empresa e foi liberado.
🔴 **Técnico:** Identity-Aware Proxy, que autentica e autoriza na frente do serviço, com a conta da empresa.
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)

## Formatos e engenharia de software

### YAML
🟢 **Simples:** um formato de texto para listas e fichas, fácil de ler para gente e para máquina.
🔴 **Técnico:** serialização por indentação. No kit, todo `loop.yaml` é validado por JSON Schema. Cuidado: no YAML 1.1, `on` vira `true`.
🧭 **No workshop:** [Dia 2 · Lab 2](dia-2.md#d2-lab2)

### JSON
🟢 **Simples:** um formato de texto com chaves e valores, o jeito mais comum de sistemas trocarem dados.
🔴 **Técnico:** JavaScript Object Notation: objetos `{}`, listas `[]`, texto, número, booleano e `null`.
🧭 **No workshop:** [Dia 2 · Lab 3](dia-2.md#d2-lab3)

### JSON Schema
🟢 **Simples:** a "ficha de regras" que diz como um arquivo precisa ser: campos obrigatórios, tipos e valores permitidos.
🔴 **Técnico:** a especificação que valida JSON e YAML. O VS Code usa a linha `# yaml-language-server: $schema=...` para dar autocomplete e mostrar erros.
🧭 **No workshop:** [Dia 2 · Lab 2](dia-2.md#d2-lab2)

### JSONL
🟢 **Simples:** um arquivo em que cada linha é um registro separado, e só se acrescenta linha no fim.
🔴 **Técnico:** JSON Lines: append-only e sem conflito de merge. É usado em evals e trilhas de auditoria.
🧭 **No workshop:** [Dia 2 · Conceitos](dia-2.md#d2-conceitos)

### Markdown
🟢 **Simples:** texto simples com marcações leves (`#` para título, `-` para lista) que vira página formatada.
🔴 **Técnico:** a linguagem de marcação que é a fonte deste workshop: o `montar.py` transforma os `.md` no site.
🧭 **No workshop:** [Dia 2 · Conceitos](dia-2.md#d2-conceitos)

### Frontmatter
🟢 **Simples:** um cabeçalho de ficha no topo de um texto, entre duas linhas de `---`.
🔴 **Técnico:** um bloco YAML no início de um `.md`. No `SKILL.md`, `name` e `description` decidem quando a skill é ativada [SRC-03].
🧭 **No workshop:** [Dia 1 · Lab 1](dia-1.md#d1-lab1)

### JSONCrack
🟢 **Simples:** uma ferramenta que desenha um JSON como um mapa de caixinhas ligadas.
🔴 **Técnico:** uma biblioteca que mostra JSON como grafo. Aqui ela entra como `jsoncrack-react@1.0.5`, com a versão fixa.
🧭 **No workshop:** [Dia 2 · Lab 3](dia-2.md#d2-lab3)

### Mermaid
🟢 **Simples:** diagramas escritos como texto, que viram desenho.
🔴 **Técnico:** uma linguagem de diagramas (`flowchart`, `sequenceDiagram`, `gitGraph`). O GitHub e este site desenham os blocos `mermaid`.
🧭 **No workshop:** [Dia 3 · Git](dia-3.md#d3-git)

### Loop
🟢 **Simples:** um processo que o agente repete: faz, confere, registra e decide se continua.
🔴 **Técnico:** uma spec com etapas, verificadores (VERIFICAR), estado (ESTADO) e parada (PARADA). Sem os três pilares, o schema reprova.
🧭 **No workshop:** [Dia 2 · Lab 2](dia-2.md#d2-lab2)

### Verificador
🟢 **Simples:** quem confere, sem opinião, se o trabalho ficou certo: passou ou não passou.
🔴 **Técnico:** uma checagem bloqueante (schema, teste ou revisão). O `validar.py` do kit é um verificador.
🧭 **No workshop:** [Dia 2 · Lab 2](dia-2.md#d2-lab2)

## DataOps e qualidade

### Git
🟢 **Simples:** o histórico do projeto, com máquina do tempo: guarda cada versão e quem mudou o quê.
🔴 **Técnico:** um controle de versão distribuído, com commits, branches e merges.
🧭 **No workshop:** [Dia 3 · Git](dia-3.md#d3-git)

### Commit
🟢 **Simples:** uma foto do projeto num momento, com uma frase dizendo o que mudou.
🔴 **Técnico:** um snapshot identificado por hash, com autor e mensagem. O pre-commit roda antes de gravar.
🧭 **No workshop:** [Dia 3 · Lab 4](dia-3.md#d3-lab4)

### Branch
🟢 **Simples:** uma linha de trabalho paralela, para mexer sem atrapalhar a versão principal.
🔴 **Técnico:** um ponteiro móvel para um commit. `git switch -c` cria a branch e já troca para ela [SRC-14].
🧭 **No workshop:** [Dia 3 · Git](dia-3.md#d3-git)

### Pull request
🟢 **Simples:** o pedido para juntar o seu trabalho na versão principal, com a revisão de outra pessoa.
🔴 **Técnico:** PR, uma proposta de merge com diff, discussão, CI e aprovação. Abre com `gh pr create` [SRC-14].
🧭 **No workshop:** [Dia 3 · Lab 4](dia-3.md#d3-lab4)

### Code review
🟢 **Simples:** outra pessoa lê a sua mudança antes de ela entrar. Quem escreveu não aprova.
🔴 **Técnico:** a revisão do diff com checklist (o modelo de PR) e com donos por pasta (`CODEOWNERS`). Um agente revisor ajuda, mas quem decide é a pessoa.
🧭 **No workshop:** [Dia 3 · Git](dia-3.md#d3-git)

### CI/CD
🟢 **Simples:** robôs que testam sozinhos cada mudança (CI) e publicam o que passou (CD).
🔴 **Técnico:** integração e entrega contínuas: uma pipeline de checagens a cada PR. No kit é o `.github/workflows/ci.yml`, que roda igual na sua máquina com o `ci_local.py`.
🧭 **No workshop:** [Dia 3 · Lab 4](dia-3.md#d3-lab4)

### Esteira
🟢 **Simples:** o caminho que todo pedido percorre: desenvolver, testar, homologar, publicar.
🔴 **Técnico:** a pipeline de entrega. Numa esteira de agentes: pedido, dev, teste, homologação e deploy.
🧭 **No workshop:** [Dia 3 · Abertura](dia-3.md#d3-abertura)

### Ambiente
🟢 **Simples:** uma "cópia de trabalho" separada: dev para mexer, homologação para testar, produção para valer.
🔴 **Técnico:** projetos, bases e credenciais isolados por estágio. Nada de teste em produção.
🧭 **No workshop:** [Dia 3 · Abertura](dia-3.md#d3-abertura)

### Homologação
🟢 **Simples:** a etapa em que quem pediu testa e diz "é isso".
🔴 **Técnico:** o aceite da área solicitante, num ambiente separado, antes do deploy em produção.
🧭 **No workshop:** [Dia 3 · Abertura](dia-3.md#d3-abertura)

### A/B test
🟢 **Simples:** comparar duas versões com a mesma régua para ver qual é melhor.
🔴 **Técnico:** a mesma bateria de casos para controle e candidata, com regra de decisão escrita antes, guarda-corpos e intervalo de confiança. No kit, é o `ab.py`.
🧭 **No workshop:** [Dia 3 · Lab 5](dia-3.md#d3-lab5)

### Eval
🟢 **Simples:** uma prova com gabarito para o agente.
🔴 **Técnico:** uma avaliação automática contra casos esperados. No ADK, é o `adk eval`, com um evalset e critérios como `response_match_score` [SRC-10].
🧭 **No workshop:** [Dia 3 · Lab 5](dia-3.md#d3-lab5)

### Dry-run
🟢 **Simples:** um ensaio que mostra o que aconteceria e quanto custaria, sem fazer de verdade.
🔴 **Técnico:** uma execução simulada. No BigQuery, `bq query --dry_run` estima os bytes antes da consulta real; é a regra da casa, e o hook de custo do kit cobra.
🧭 **No workshop:** [Dia 1 · Lab 1](dia-1.md#d1-lab1)

### Prompt injection
🟢 **Simples:** um texto escondido num arquivo ou numa página que tenta dar ordens ao agente.
🔴 **Técnico:** uma instrução maliciosa dentro de conteúdo não confiável. A defesa é tratar conteúdo como dado, usar guarda-corpos (hooks, callbacks e plugins de segurança do ADK) e revisar [SRC-10].
🧭 **No workshop:** [Dia 3 · Segurança](dia-3.md#d3-sec)

### Cadeia de suprimentos
🟢 **Simples:** tudo o que vem de fora e entra no seu projeto: bibliotecas, skills, plugins. Se um elo é ruim, o projeto inteiro fica ruim.
🔴 **Técnico:** as dependências de terceiros. A defesa é fixar versão ou SHA, auditar antes de usar e rodar isolado.
🧭 **No workshop:** [Dia 3 · Segurança](dia-3.md#d3-sec)

### Segredo
🟢 **Simples:** a senha, chave ou token que dá acesso a um sistema. Nunca vai para o código nem para o chat.
🔴 **Técnico:** uma credencial. Fica em variável de ambiente ou num cofre, com o `.env` listado no `.gitignore`; o sandbox bloqueia o `.env` [SRC-07].
🧭 **No workshop:** [Dia 3 · Segurança](dia-3.md#d3-sec)

### Menor privilégio
🟢 **Simples:** dar a cada um só a chave de que precisa, nunca o molho inteiro.
🔴 **Técnico:** permissões e papéis mínimos por tarefa: `command(prefixo)` em vez de `command(*)`, e uma conta de serviço própria em vez de `roles/editor`.
🧭 **No workshop:** [Dia 3 · Segurança](dia-3.md#d3-sec)

### PII
🟢 **Simples:** dado que identifica uma pessoa: nome, e-mail, CPF.
🔴 **Técnico:** Personally Identifiable Information, protegida pela LGPD. Não entra no workspace, nem em prompt, nem em base vetorial.
🧭 **No workshop:** [Dia 3 · Segurança](dia-3.md#d3-sec)

### DataOps
🟢 **Simples:** cuidar de dados e agentes do jeito que se cuida de software: com versão, teste e revisão em tudo.
🔴 **Técnico:** as práticas de engenharia (versionamento, testes automáticos, ambientes e observabilidade) aplicadas a pipelines de dados e de agentes.
🧭 **No workshop:** [Dia 3 · Abertura](dia-3.md#d3-abertura)

### Cron
🟢 **Simples:** um despertador de computador: "rode isto todo dia às 9h".
🔴 **Técnico:** uma expressão de agenda com 5 campos (minuto, hora, dia, mês e dia da semana). Nas automações do Antigravity, ela leva o prefixo `CRON_TZ` [SRC-04].
🧭 **No workshop:** [Dia 1 · Tour](dia-1.md#d1-tour)
