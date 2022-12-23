import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook3", methods=["POST"])
def handle_webhook():

    movie_rate = request.get_json()['queryResult']['parameters']['movie']
    episode_rate = request.get_json()['queryResult']['parameters']['episode']

    db = firestore.client()

    if movie_rate == "全部電影":
        response_text = "您選擇的電影分類是：" + movie_rate + "，相關電影："
        movies_collection = db.collection("最新電影_全部")
        query = movies_collection.stream()
    elif movie_rate in ["動作片", "喜劇片", "愛情片", "科幻片", "恐怖片", "劇情片", "戰爭片", "紀錄片"]:
        response_text = "您選擇的電影分類是：" + movie_rate + "，相關電影："
        movies_collection = db.collection("最新電影_分類")
        query = movies_collection.where("rate", "==", movie_rate).stream()
    elif episode_rate == "全部劇集":
        response_text = "您選擇的劇集分類是：" + episode_rate + "，相關劇集："
        movies_collection = db.collection("最新劇集_全部")
        query = movies_collection.stream()
    elif episode_rate in ["陸劇", "港劇", "台劇", "日劇", "韓劇", "美劇", "海外劇"]:
        response_text = "您選擇的劇集分類是：" + episode_rate + "，相關劇集："
        movies_collection = db.collection("最新劇集_分類")
        query = movies_collection.where("rate", "==", episode_rate).stream()

    movies = list(query)
    for movie in movies:
        response_text += "\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")
    episodes = list(query)
    for episode in episodes:
        response_text += "\n片名：" + episode.get("text") + "\n介紹：" + episode.get("link")

    return make_response(jsonify({
        "fulfillmentText": response_text
    }))