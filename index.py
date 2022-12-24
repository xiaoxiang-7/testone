import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook3", methods=["POST"])
def handle_webhook():
    # 從請求正文中提取“episode”或“movie”或“cartoon”參數
    episode_rate = request.get_json().get('queryResult', {}).get('parameters', {}).get('episode')
    movie_rate = request.get_json().get('queryResult', {}).get('parameters', {}).get('movie')
    cartoon_rate = request.get_json().get('queryResult', {}).get('parameters', {}).get('cartoon')

    # 連接到 Firestore 數據庫
    db = firestore.client()

    # 初始化響應文本
    response_text = ""

    # 檢查“episode”參數的值
    if episode_rate == "全部劇集":
        response_text = "您選擇的劇集分類是：" + episode_rate + "，相關劇集："
        movies_collection = db.collection("最新劇集_全部")
        query = movies_collection.stream()
    elif episode_rate in ["陸劇", "港劇", "台劇", "日劇", "韓劇", "美劇", "海外劇"]:
        response_text = "您選擇的劇集分類是：" + episode_rate + "，相關劇集："
        movies_collection = db.collection("最新劇集_分類")
        query = movies_collection.where("rate", "==", episode_rate).stream()
    else:
        # 檢查“movie”參數的值
        if movie_rate == "全部電影":
            response_text = "您選擇的電影分類是：" + movie_rate + "，相關電影："
            movies_collection = db.collection("最新電影_全部")
            query = movies_collection.stream()
        elif movie_rate in ["動作片", "喜劇片", "愛情片", "科幻片", "恐怖片", "劇情片", "戰爭片", "紀錄片"]:
            response_text = "您選擇的電影分類是：" + movie_rate + "，相關電影："
            movies_collection = db.collection("最新電影_分類")
            query = movies_collection.where("rate", "==", movie_rate).stream()
        elif cartoon_rate == "全部動漫":
            response_text = "您選擇的動漫分類是：" + cartoon_rate + "，相關動漫："
            movies_collection = db.collection("最新動漫_全部")
            query = movies_collection.stream()
        elif cartoon_rate in ["日漫", "冒險", "熱血", "搞笑", "奇幻", "科幻"]:
            response_text = "您選擇的動漫分類是：" + cartoon_rate + "，相關動漫："
            movies_collection = db.collection("最新動漫_分類")
            query = movies_collection.where("rate", "==", cartoon_rate).stream()
        # 如果 'episode' 和 'movie' 和 'cartoon' 參數未設置或具有無效值，則將響應文本設置為錯誤消息
        else:
            response_text = "對不起，您輸入的不正確。"

    # 取得集合中的所有文件
    movies = list(query)
    for movie in movies:
        response_text += "\n\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")  
    # 傳回回應文字
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))