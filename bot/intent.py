import requests

from config.settings import DM_IP_NEW


def getIntentFromOld(workspace_id, cookie):
    url = "http://8.142.85.77:8630/config/intent/list?intentClass=NORMAL&workspaceId={}&query=".format(workspace_id)
    headers = {
        'Cookie': cookie,
        'Host': '8.142.85.77:8630',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    json = response.json()
    print(json)
    return json["result"]


def addIntent(name, description, workspace_id, version_id, cookie):
    url = "{}/configNew/intent/add?name={}&description={}&workspaceId={}&versionId={}"\
        .format(DM_IP_NEW, name, description, workspace_id, version_id)
    headers = {
        'Cookie': cookie,
        'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.post(url=url, headers=headers)
    pass


# 获取新平台意图
def getIntentList(workspace_id, version_id, cookie):
    url = "{}/configNew/intent/list?intentClass=NORMAL&workspaceId={}&versionId={}&query="\
        .format(DM_IP_NEW, workspace_id, version_id)
    headers = {
        'Cookie': cookie,
        # 'Host': '39.99.244.42:18631',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    response = requests.get(url, timeout=5, headers=headers)
    json = response.json()
    print(json)
    return json["result"]


# 更新接口
def copyIntent(old_workspace_id, workspace_id, version_id, old_cookie, cookie):
    intentList = getIntentFromOld(old_workspace_id, old_cookie)
    for one in intentList:
        addIntent(one["name"], one["description"], workspace_id, version_id, cookie)
    pass


if __name__ == '__main__':
    old_cookie = 'JSESSIONID=node0iy58prmgrdkinsi0xv4tf1cj2014259.node0'
    cookie = 'JSESSIONID=node01irhuwbfvw4z4uvmsw6bpiie74.node0'
    copyIntent(350, 20717, 23487, old_cookie, cookie)