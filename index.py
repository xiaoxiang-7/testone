import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__) # 定義一個 Flask 應用程式

@app.route("/webhook3", methods=["POST"])
def handle_webhook():
    # 取得 Dialogflow 中傳遞過來的參數
    rate = request.get_json()['queryResult']['parameters']['movie']
    episode = request.get_json()['queryResult']['parameters']['episode']

    # 建立 Firestore 的連接
    db = firestore.client()

    if rate == "全部電影":
        # 建立回應文字
        response_text = "您選擇的電影分類是：" + rate + "，相關電影："
        movies_collection = db.collection("最新電影_全部")
        query = movies_collection.stream()
    elif rate in ["動作片", "喜劇片", "愛情片", "科幻片", "恐怖片", "劇情片", "戰爭片", "紀錄片"]:
        # 建立回應文字
        response_text = "您選擇的電影分類是：" + rate + "，相關電影："
        movies_collection = db.collection("最新電影_分類")
        query = movies_collection.where("rate", "==", rate).stream()

    elif episode == "全部劇集":
        # 建立回應文字
        response_text = "您選擇的劇集分類是：" + episode + "，相關劇集："
        series_collection = db.collection("最新劇集_全部")
        query = series_collection.stream()
    elif episode in ["陸劇", "港劇", "台劇", "日劇", "韓劇", "美劇", "海外劇"]:
        # 建立回應文字
        response_text = "您選擇的劇集分類是：" + episode + "，相關劇集："
        series_collection = db.collection("最新劇集_分類")
        query = series_collection.where("episode", "==", episode).stream()

    # 取得集合中的所有文件
    movies = list(query)
    for movie in movies:
        response_text += "\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")
    
    # 傳回回應文字
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))