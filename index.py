import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__) # 定義一個 Flask 應用程序

@app.route("/webhook3", methods=["POST"])
def handle_webhook():
    # 取得 Dialogflow 中傳遞過來的參數
    rate = request.get_json()['queryResult']['parameters']['movie']

    # 建立 Firestore 的連接
    db = firestore.client()

    # 取得集合
    movies_collection = db.collection("最新電影_分類")

    # 查詢集合中 rate 為動作片的所有文件
    query = movies_collection.where("rate", "==", rate).stream()
    movies = list(query)

    # 建立回應文字
    response_text = "您選擇的電影分類是：" + rate + "，相關電影："
    for movie in movies:
        response_text += "\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")
    
    # 傳回回應文字
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))