import json

import requests

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}

pet = {
    "id": 541,
    "category": {
        "id": 0,
        "name": "string"
    },
    "name": "dimon",
    "photoUrls": [
        "https://a.d-cd.net/b0798fes-1920.jpg"
    ],
    "tags": [
        {
            "id": 0,
            "name": "string"
        }
    ],
    "status": "available"
}

res = requests.post(f'https://petstore.swagger.io/v2/pet',
                    headers=headers, data=json.dumps(pet)
                    )

print(res.status_code)

if 'application/json' in res.headers['Content-Type']:
    print(res.json())
    print(type(res.json()))
else:
    print(res.text)
    print(type(res.text))
