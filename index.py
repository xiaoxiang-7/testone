import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def handle_webhook():
    # Extract the movie or episode type from the request payload
    intent = request.get_json()['queryResult']['intent']['displayName']

    # Initialize the Firestore client and retrieve a reference to the relevant collection
    db = firestore.client()
    if intent == "Movie":
        collection_name = "最新電影_全部"
        type_name = "電影"
    elif intent == "Episode":
        collection_name = "最新劇集_全部"
        type_name = "劇集"
    else:
        return make_response(jsonify({
            "fulfillmentText": "Invalid movie or episode type"
        }))

    movies_collection = db.collection(collection_name)
    query = movies_collection.stream()

    # Construct the response string containing the names and links of the movies or episodes
    response_text = "您選擇的{}分類是：{}，相關{}：".format(type_name, type_name, type_name)
    movies = list(query)
    for movie in movies:
        response_text += "\n片名：" + movie.get("text") + "\n介紹：" + movie.get("link")

    # Return the response as the fulfillment text in a JSON object
    return make_response(jsonify({
        "fulfillmentText": response_text
    }))