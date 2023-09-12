import requests


# @staticmethod
def get(url, cookie):
    headers = {
        'Cookie': cookie,
        # 'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    return response


# @staticmethod
def post(url, data, cookie):
    headers = {
        'Cookie': cookie,
        # 'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.post(url=url, data=data, headers=headers)
    return response


# @staticmethod
def post_json(url, data, cookie):
    headers = {
        # 'Cookie': cookie,
        # 'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'Accesstoken': 'eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjEsInVzZXJOYW1lIjoiYWRtaW4iLCJzdWIiOiIxNjg0NzQ5MjUyNTUwIiwiaWF0IjoxNjg0NzQ5MjUyfQ.jnFvdJ3rDXnExejwvWTv5LoaG0c4JUSMZH5deZf5JDA',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(url=url, json=data, headers=headers)
    return response


# @staticmethod
def get_old(url, cookie):
    headers = {
        'Cookie': cookie,
        # 'Host': '8.142.85.77:8630',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    return response


# @staticmethod
def post_old(url, data, cookie):
    headers = {
        'Cookie': cookie,
        # 'Host': '8.142.85.77:8630',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.post(url=url, data=data, headers=headers)
    return response

