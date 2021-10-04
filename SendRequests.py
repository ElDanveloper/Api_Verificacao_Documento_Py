import requests


def sendRequest(body, url, token):
    # values = {
    # "email": "contato@leandroreboucas.com",
    # "password": "041050"
    # }
    # response = requests.post("https://beta.hunno.com.br/api/login",values)
    # print(response.json()["token"])
    # headers = {
    #     'Authorization': 'Bearer {}'.format(response.json()["token"])
    # }
    token = 'Bearer '+token
    headers = {
        'Authorization': '{}'.format(token)
    }
    print(url)
    responseApi = requests.post(url=url, json=body, headers=headers)

    if responseApi.status_code >= 200 and responseApi.status_code <= 299:
        return responseApi.json()
    else:
        print(responseApi.status_code)
        print(responseApi.text)
        return responseApi.text
