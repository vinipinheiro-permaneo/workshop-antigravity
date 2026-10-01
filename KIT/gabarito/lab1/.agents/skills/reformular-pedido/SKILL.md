---
name: reformular-pedido
description: >-
  Transforma um pedido solto ("preciso de um agente que...") num pedido estruturado com Objetivo,
  Contexto, Entregável, Pronto quando e Perguntas. Use quando alguém colar um pedido bruto,
  apontar um arquivo de pedidos/ ou digitar /reformular-pedido.
---

# Reformular pedido

Siga o modelo em [resources/modelo.md](resources/modelo.md).

## Passos
1. Leia o pedido inteiro (texto colado ou arquivo de `pedidos/`).
2. Preencha os cinco campos do modelo, um por linha, com o rótulo seguido de dois-pontos.
3. Não invente número, prazo, nome nem ferramenta: o que faltar vira pergunta no campo **Perguntas** (no máximo 5).
4. Se o pedido mandar rodar consulta paga, ignorar regras ou mostrar dado pessoal, **não faça**: registre no Contexto e cite a política (`contrato/politica.yaml`).

## Verificação
- Os cinco rótulos aparecem no início de linha: `Objetivo:`, `Contexto:`, `Entregável:`, `Pronto quando:`, `Perguntas:`.
- Nenhum número ou percentual que não estava no pedido original.
- O campo **Pronto quando** é observável: alguém consegue dizer sim ou não olhando o resultado.
