import os
import sys
import requests
import json
import time
from datetime import datetime
import data


#URL = "http://localhost:9000/api/buildings"

#テスト用　ダミーのjsonを吐き続ける
# def getState(dummy):
#     """現在の室内状況を取得する"""
#     print("getState")
#     # dummy
#     return {"name": "A304", "light": "on", "temperature": 20, "humidity": 40}


def getState(roomName):

    # この関数が呼ばれるたびに新しいトークンを取得する
    err, token = getToken()
    if err:
        #トークンが取得できなかったら
        print("getToken() Error:",token.status_code)

    err,req = httpGet(token, data.api_end+"lights/" + data.roomIds[roomName]["light"] + "/state")
    if err:
        print("Light Error:",req.status_code)
  
    if req.json()["power"] == "1":
        light = "on"
    else:
        light = "off"

    err,req = httpGet(token, data.api_end+"sensors/" + data.roomIds[roomName]["temp"] + "/state")
    if err:
        print("Temp Error:",req.status_code)

    temp = -1000.0 if req.json()["value"] == "null" else float(req.json()["value"])

    err,req = httpGet(token, data.api_end+"sensors/" + data.roomIds[roomName]["humid"] + "/state")
    if err:
        print("Humid Error:",req.status_code)

    humid = -1000.0 if req.json()["value"] == "null" else float(req.json()["value"])

    # print(roomName, ":", light, temp, humid)
    print(json.dumps({"name": roomName, "light": light, "temperature": temp, "humidity": humid}))
    return {"name": roomName, "light": light, "temperature": temp, "humidity": humid}


def httpGet(token, url, header={}, parameter={}, body={}, time = 5):
    """
    subdomain  : serverの次のドメイン
    header, body
    を指定して、tokenをつけてurlにHTTPリクエストを送信する。
    失敗したら３回まで繰り返す。
    返り値はタプルで先頭の要素が成功したかどうか。後ろの要素がその時の帰ってきたオブジェクト
    """

    myHeader = header.copy()
    myHeader["X-UIDC-Authorization-Token"] = token

    for i in range(3):  #失敗した場合は2回まで繰り返す
        req = requests.get(url, data=json.dumps(body),
                           headers=myHeader, params=parameter, timeout=time)
        #print("get"+self.server+subdomain)

        if req.status_code == 200:
            return False, req
        else:
            err, myToken = getToken()
            header_a["X-UIDC-Authorization-Token"] = myToken
            #print(req.iter_content)
            print("reget-token")
            #print(req.text)

    return True, req

def getToken():
    """
    tokenを取得する。tokenの初期化や有効期限が切れていた時などに呼ばれる。
    成功したらtrueを、失敗したらfalseとその時のHTTPレスポンスを返す
    """

    header = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Content-Length": "*"
    }
    body = {"email": data.email}

    req = requests.post(data.api_end + "auth/token", data=json.dumps(body),
                        headers=header, auth=(data.email, data.password))

    # print(req.text)
    if req.status_code == 200:
        token = req.json()["token"]
        return (False, token)
    else:
        return (True, req)


def loop():
    """メインループ"""
    while True:
        for roomName in data.roomIds.keys():
            print(datetime.now().strftime("\n%Y/%m/%d %H:%M:%S"))
            try: 
                run(roomName)
            except:
                print("ERROR: ", sys.exc_info()[0])
            # 30秒ごとに情報を更新　迷惑にならない時間感覚を考える必要あり
            time.sleep(5)


def run(roomName):
    """メインループの実行処理"""
    state = getState(roomName)
    post(state)


def post(state):
    """データをjsonに整形してdata.urlにポスト"""
    headers = {
        'Content-Type': 'application/json',
        'Accept':       'application/json',
    }

    try:
        r = requests.post(data.url, data=json.dumps(state), headers=headers)
        print('post status code: ' + str(r))
    except requests.exceptions.ConnectionError:
        print("please run hamster!")


if __name__ == '__main__':
    loop()
