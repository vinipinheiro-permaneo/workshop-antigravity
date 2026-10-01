# Agente ADK: revisor de pedidos (para casa)

O mesmo loop que o workshop montou em YAML, agora como agente do Google ADK:

| Pilar do loop | No `loop.yaml` | No ADK (`revisor/agent.py`) |
|---|---|---|
| etapas | `etapas:` | `sub_agents=[escritor, critico]` |
| VERIFICAR | `verificadores:` | o agente `critico` e a lista fixa |
| ESTADO | `estado.onde` | `output_key` (rascunho, crítica) no estado da sessão |
| PARADA | `parada.sucesso` / `max_iteracoes` | `exit_loop` / `max_iterations=3` |
| guarda de custo | hook `guarda_custo.py` | `before_model_callback` em `revisor/guarda.py` |

## Sem custo (dá para fazer já)
```
pip install google-adk==2.3.0
python -c "import sys; sys.path.insert(0, 'adk'); from revisor import agent; print(agent.root_agent.name, agent.root_agent.max_iterations)"
```
Só importa o agente e mostra a estrutura. Nenhuma chamada ao modelo acontece.

## 💲 Com modelo (combine antes com o facilitador)
1. Copie `revisor/.env.exemplo` para `revisor/.env` e preencha **uma** das opções.
2. `adk run adk/revisor` e cole o texto de `pedidos/exemplo-01.md`.
3. Ou `adk web adk`, abra `http://localhost:8000`, escolha `revisor` e veja cada volta do loop na aba de eventos.

Cada volta chama o modelo duas vezes (escritor e crítico), com no máximo 3 voltas. O guarda-corpo bloqueia pedidos com `bq query`, `gcloud`, `.env` ou "ignore as regras" antes de chamar o modelo, então esses pedidos não custam nada.
