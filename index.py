import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__) # 定義一個 Flask 應用程式

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Get the request data
    data = request.get_json()
    query_result = data['queryResult']
    media_type = query_result['parameters']['media_type']
    media_rate = query_result['parameters']['media_rate']

    # Connect to the Firestore database
    db = firestore.client()

    # Initialize the response text
    response_text = "您選擇的" + media_type + "分類是：" + media_rate + "，相關" + media_type + "："

    # Query the appropriate collection based on the media type and rate
    if media_type == "電影":
        if media_rate == "全部電影":
            media_collection = db.collection("最新電影_全部")
            query = media_collection.stream()
        elif media_rate in ["動作片", "喜劇片", "愛情片", "科幻片", "恐怖片", "劇情片", "戰爭片", "紀錄片"]:
            media_collection = db.collection("最新電影_分類")
            query = media_collection.where("rate", "==", media_rate).stream()
    elif media_type == "劇集":
        if media_rate == "全部劇集":
            media_collection = db.collection("最新劇集_全部")
            query = media_collection.stream()
        elif media_rate in ["陸劇", "港劇", "台劇", "日劇", "韓劇", "美劇", "海外劇"]:
            media_collection = db.collection("最新劇集_分類")
            query = media_collection.where("rate", "==", media_rate).stream()

    # Loop through the media and append information about each item to the response text
    media = list(query)
    for item in media:
        response_text += "\n片名：" + item.get("text") + "\n介紹：" + item.get("link")

    # Send the response
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))