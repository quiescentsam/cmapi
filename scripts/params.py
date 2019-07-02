import json, pprint

with open('config.json') as json_file:
    data = json.load(json_file)
    json.dumps(data)