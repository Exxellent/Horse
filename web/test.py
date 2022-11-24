import os 
import json
pylint = os.popen('pylint ./app').read()
if pylint:
    print("Ошибки качества кода")

os.system('bandit -r ./app/ -o bandit.json -f json')
with open('bandit.json', 'r') as f:
    b = json.load(f)
if b['results']:
    raise RuntimeError('Ошибки')