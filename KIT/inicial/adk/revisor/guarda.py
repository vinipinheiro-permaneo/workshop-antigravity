"""Guarda-corpo do agente: bloqueia ANTES de chamar o modelo.

Duas vantagens: pedido perigoso não chega ao modelo, e o bloqueio não custa nada.
A regra fica numa função pura (`motivo_de_bloqueio`) para poder ser testada sem ADK e sem modelo.
"""
from __future__ import annotations

import re

PERIGOSO = [
    (re.compile(r"\bbq\s+query\b|\bgcloud\b", re.I), "consulta ou comando de nuvem pedido direto no chat (POL-CUSTO)"),
    (re.compile(r"ignore\s+(as|todas\s+as)\s+regras|desconsidere\s+as\s+regras", re.I), "tentativa de desligar as regras (injeção de prompt)"),
    (re.compile(r"\.env\b|\bchave\s+de\s+api\b|\bapi[_\s-]?key\b", re.I), "pedido de segredo ou credencial"),
]


def motivo_de_bloqueio(texto: str) -> str | None:
    for rx, motivo in PERIGOSO:
        if rx.search(texto or ""):
            return f"Não vou seguir com este pedido: {motivo}. Reescreva sem essa parte ou peça aprovação a quem responde pela política."
    return None


def bloquear_pedido_perigoso(callback_context, llm_request):
    """before_model_callback: devolver um LlmResponse pula a chamada ao modelo; devolver None segue normal."""
    ultimo = ""
    for conteudo in reversed(llm_request.contents or []):
        if conteudo.role == "user":
            ultimo = " ".join(p.text for p in (conteudo.parts or []) if getattr(p, "text", None))
            break
    motivo = motivo_de_bloqueio(ultimo)
    if motivo is None:
        return None
    from google.adk.models import LlmResponse
    from google.genai import types
    return LlmResponse(content=types.Content(role="model", parts=[types.Part(text=motivo)]))
