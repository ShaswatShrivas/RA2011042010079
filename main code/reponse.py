import requests

urls = [
    'http://20.244.56.144/numbers/primes',
    'http://20.244.56.144/numbers/fibo',
    'http://20.244.56.144/numbers/odd'
]

response = requests.get('http://localhost:8008/numbers', params={'url':urls})
data = response.json()
print(data)
