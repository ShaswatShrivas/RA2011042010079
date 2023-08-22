from flask import Flask, request, jsonify
import requests
import gevent
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get('numbers', [])
    except Exception as e:
        pass
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    numbers = set()

    def worker(url):
        nonlocal numbers
        fetched_numbers = fetch_numbers(url)
        numbers.update(fetched_numbers)

    threads = [gevent.spawn(worker, url) for url in urls]
    gevent.joinall(threads, timeout=0.5)

    merged_numbers = sorted(list(numbers))
    response = {'numbers': merged_numbers}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
