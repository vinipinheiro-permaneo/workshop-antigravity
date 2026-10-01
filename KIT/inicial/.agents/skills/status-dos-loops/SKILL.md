---
name: status-dos-loops
description: >-
  Mostra o estado dos loops deste workspace: quais existem, se passam no validador e o que falta em cada um.
  Use quando a pessoa perguntar "como estão os loops", "o que está quebrado" ou pedir /status-dos-loops.
---

# Status dos loops

1. Rode `python ferramentas/validar.py --json` e leia a saída.
2. Monte uma tabela com as colunas: loop | válido? | problemas.
3. Para cada problema, diga em uma frase como corrigir. Não corrija sozinho: quem decide é a pessoa.
4. Termine com a contagem no formato `N válidos · M com problema`.

## Verificação
A tabela precisa ter exatamente uma linha por pasta em `loops/`. Confira com `python ferramentas/validar.py --json`, campo `resumo`.
