# Hook neutralizado: sem opinião, devolve a decisão para o fluxo normal de permissão.
import json
import sys

json.load(sys.stdin)
print(json.dumps({"decision": "ask"}))
