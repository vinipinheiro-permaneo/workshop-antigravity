---
name: validar-loops
description: >-
  Valida os loops do workspace e corrige os problemas um de cada vez, rodando o validador depois
  de cada correção. Use quando a pessoa pedir para validar ou consertar loops, ou digitar /validar-loops.
---

# Validar loops

1. Rode `python ferramentas/validar.py --json`.
2. Se `resumo.com_problema` for 0, diga "todos os loops válidos" e pare.
3. Para cada problema, **um de cada vez**:
   - explique em uma frase o que está errado e qual pilar (verificar, estado, parada) ele afeta;
   - proponha a correção mostrando o trecho de YAML;
   - aplique só depois de a pessoa responder "pode";
   - rode o validador de novo.
4. Nunca apague um loop para "passar" no validador.

## Verificação
A última linha da sua resposta é a saída de `python ferramentas/validar.py`, com `0 com problema`.
