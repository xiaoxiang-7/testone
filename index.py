import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__) # 定義一個 Flask 應用程序

@app.route("/webhook3", methods=["POST"])
def webhook3():
    # 構建一個請求對象
    req = request.get_json(force=True)
    # 從 json 中獲取查詢結果
    action =  req.get("queryResult").get("action")
    
    if (action == "movie"):
        rate =  req.get("queryResult").get("parameters").get("movie")
        if (rate == "動作片"):
            rate = "動作片"
        elif (rate == "喜劇片"):
            rate = "喜劇片"
        info = "您選擇的電影分類是：" + rate + "，相關電影：\n"

        collection_ref = db.collection("最新電影_分類")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["rate"]:
                result += "片名：" + dict["text"] + "\n"
                result += "介紹：" + dict["link"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#    app.run()