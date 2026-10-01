import json
import sys

json.load(sys.stdin)
print(json.dumps({"decision": "allow"}))
