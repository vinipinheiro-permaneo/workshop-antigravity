"""Revisor de pedidos no ADK: o mesmo loop do workshop (escrever → verificar → parar), como agente.

Pilares do loop, agora em código:
  VERIFICAR  o `critico` confere o rascunho contra uma lista fixa
  ESTADO     `output_key` guarda rascunho e crítica no estado da sessão
  PARADA     o `critico` chama `exit_loop` quando passa; `max_iterations` é o limite

💲 Rodar chama o modelo: veja adk/README.md antes (chave, custo, projeto de testes).
   adk run adk/revisor        (terminal)
   adk web adk                (interface no navegador, porta 8000)
"""
import os

from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools import exit_loop

from . import guarda

MODELO = os.environ.get("ADK_MODELO", "gemini-3.5-flash")
CAMPOS = "Objetivo, Contexto, Entregável, Pronto quando, Perguntas"

escritor = LlmAgent(
    name="escritor",
    model=MODELO,
    description="Reescreve o pedido do usuário no formato estruturado.",
    instruction=(
        f"Reformule o pedido do usuário usando exatamente estes campos, um por linha: {CAMPOS}.\n"
        "Não invente números, prazos nem nomes: o que faltar vira pergunta no campo Perguntas.\n"
        "Se existir crítica da volta anterior, corrija só o que ela apontou.\n"
        "Crítica anterior: {critica?}"
    ),
    output_key="rascunho",
    before_model_callback=guarda.bloquear_pedido_perigoso,
)

critico = LlmAgent(
    name="critico",
    model=MODELO,
    description="Confere o rascunho contra a lista e decide se o loop para.",
    instruction=(
        "Revise o rascunho abaixo contra esta lista:\n"
        f"1. os campos {CAMPOS} estão todos presentes;\n"
        "2. não há número, prazo ou nome que não estava no pedido original;\n"
        "3. nada pede para executar consulta paga ou expor dado pessoal.\n\n"
        "Rascunho:\n{rascunho}\n\n"
        "Se os três itens passam, chame a ferramenta exit_loop e não escreva mais nada.\n"
        "Se algum falha, escreva só a lista do que precisa mudar."
    ),
    tools=[exit_loop],
    output_key="critica",
)

root_agent = LoopAgent(
    name="revisor_de_pedidos",
    description="Escreve e revisa um pedido estruturado até passar na lista ou completar 3 voltas.",
    sub_agents=[escritor, critico],
    max_iterations=3,
)
