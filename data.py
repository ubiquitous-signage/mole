import os
import sys
import atexit
import json
import requests

#hamsterのserverのアドレス
url = "http://35.200.70.212:9000/api/rooms"

#APIサーバのエンドポイント
api_end = "http://172.31.8.129/api/1.0/"

#状態を取得したい部屋のucodeリスト
roomIds = {
    "A301":{
        "light": "00001C000000000000020000000D44F2",
        "temp":  "00001C00000000000002000000063433",
        "humid": "00001C00000000000002000000063434"
    },
    "A302":{
        "light": "00001C000000000000020000000D44F3",
        "temp": "00001C00000000000002000000063436",
        "humid": "00001C00000000000002000000063437"
    },
    "A303":{
        "light": "00001C000000000000020000000D44F4",
        "temp": "00001C00000000000002000000063439",
        "humid": "00001C0000000000000200000006343A"
    },
    "A304":{
        "light": "00001C000000000000020000000D44F5",
        "temp": "00001C0000000000000200000006343C",
        "humid": "00001C0000000000000200000006343D"
    },
    "A305":{
        "light": "00001C000000000000020000000D44F6",
        "temp": "00001C0000000000000200000006343F",
        "humid": "00001C00000000000002000000063440"
    }
}

#アカウント情報
email  = os.environ["DUCRB_API_USERNAME"]
password = os.environ["DUCRB_API_PASSWORD"]

if ("--slack" in sys.argv):
    slack = os.environ["MOLE_SLACK_HOOK"]
    @atexit.register
    def notifyExit():
        requests.post(slack, json.dumps({"username": "ubiquitous-signage/mole", "icon_emoji": ":sleuth_or_spy:", "text": "mole exited!"}))
