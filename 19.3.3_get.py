import requests

status = 'available'

res = requests.get(f'https://petstore.swagger.io/v2/pet/findByStatus?{status}', headers={'accept': 'application/json'})

print(res.status_code)

if 'application/json' in res.headers['Content-Type']:
    print(res.json())
    print(type(res.json()))
else:
    print(res.text)
    print(type(res.text))


