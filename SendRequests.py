import requests


def sendRequest(body, url, token):
    token = 'Bearer '+token
    headers = {
        'Authorization': '{}'.format(token)
    }
    responseApi = requests.post(url=url, json=body, headers=headers)

    if responseApi.status_code >= 200 and responseApi.status_code <= 299:
        return responseApi.json()
    else:
        print(responseApi.status_code)
        print(responseApi.text)
        return responseApi.text
