import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook3", methods=["POST"])
def handle_webhook():
    rate = request.get_json()['queryResult']['parameters']['rate']
    db = firestore.client()

    if rate == "全部電影":
        response_text = "您選擇的電影分類是：" + rate + "\n，相關電影："
        movies_collection = db.collection("最新電影_全部")
        query = movies_collection.stream()
    elif rate in ["動作片", "喜劇片", "愛情片", "科幻片", "恐怖片", "劇情片", "戰爭片", "紀錄片"]:
        response_text = "您選擇的電影分類是：" + rate + "\n，相關電影："
        movies_collection = db.collection("最新電影_分類")
        query = movies_collection.where("rate", "==", rate).stream()

    movies = list(query)
    for movie in movies:
        response_text += "\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")

    return make_response(jsonify({
        "fulfillmentText": response_text
    }))