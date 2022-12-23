import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook3", methods=["POST"])
def webhook3():
    # 構建一個請求對象
    req = request.get_json(force=True)
    # 從 json 中獲取查詢結果
    action =  req.get("queryResult").get("action")
    
    if (action == "rateChoice"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        if (rate == "輔12級"):
            rate = "輔導級(未滿十二歲之兒童不得觀賞)"
        elif (rate == "輔15級"):
            rate = "輔導級(未滿十五歲之人不得觀賞)"
        info = "您選擇的電影分級是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("子青電影")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))
