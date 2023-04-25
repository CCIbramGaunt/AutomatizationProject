import json

import requests

headers = {
    'accept': 'application/json'
}

petId = 541

res = requests.delete(f'https://petstore.swagger.io/v2/pet/{petId}', headers=headers)

print(res.status_code)
print(res.text)
print(type(res.text))
