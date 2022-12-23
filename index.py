import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req.get("queryResult").get("action")

    if (action == "movie"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的電影分類是：" + rate + "，相關電影：\n"
        collection_ref = db.collection("最新電影_全部")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    elif (action == "movie"):
        rate =  req.get("queryResult").get("parameters").get("rate")
        info = "您選擇的電影分類是：" + rate + "，相關電影：\n"
        collection_ref = db.collection("最新電影_分類")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "分類：" + dict["rate"] + "\n\n"
                result += "介紹網址：" + dict["link"] + "\n\n\n"
        info += result
    
    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#    app.run()