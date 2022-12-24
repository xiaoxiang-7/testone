import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route('/webhook3', methods=['POST'])
def handle_webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''

  query_result = req.get('queryResult')
  if query_result.get('action') == 'movie':
    # Get the user's input keyword
    keyword = query_result.get('queryText')
    movie_rate = request.get_json()['queryResult']['parameters']['movie']
    db = firestore.client()
    response_text = "您輸入的關鍵字是：" + keyword + "\n您選擇的電影分類是：" + movie_rate + "，相關電影："
    movies_collection = db.collection("最新電影_全部")
    query = movies_collection.stream()
  elif query_result.get('action') == 'episode':
    # Get the user's input keyword
    keyword = query_result.get('queryText')
    episode_rate = request.get_json()['queryResult']['parameters']['episode']
    db = firestore.client()
    response_text = "您輸入的關鍵字是：" + keyword + "\n您選擇的劇集分類是：" + episode_rate + "，相關劇集："
    movies_collection = db.collection("最新劇集_全部")
    query = movies_collection.stream()
  
  # 取得集合中的所有文件
    movies = list(query)
    for movie in movies:
        response_text += "\n片名：" + episode.get("text") + "\n介紹：" + episode.get("link")  
    # 傳回回應文字
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))