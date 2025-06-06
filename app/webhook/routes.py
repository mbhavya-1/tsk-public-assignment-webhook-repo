from flask import Blueprint, json, request, jsonify
from .db import collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers.get('Content-Type') == 'application/json':
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')  # to verify it's a PR event

        if event_type == 'pull_request':
            pr = payload.get("pull_request", {})
            data = {
                "request_id": str(pr.get("id")),
                "author": pr.get("user", {}).get("login"),
                "action": "PULL REQUEST",
                "from_branch": pr.get("head", {}).get("ref"),
                "to_branch": pr.get("base", {}).get("ref"),
                "timestamp": pr.get("updated_at")  # already in ISO format
            }
            collection.insert_one(data),
            return jsonify({"message": "Pull Request data saved"}), 200

        return jsonify({"message": "Not a pull request event"}), 200

    return jsonify({"error": "Invalid Content-Type"}), 400

@webhook.route('/get-updates', methods=["GET"])
def get_updates():
    events = list(collection.find({}, {"_id": 0}))  # exclude MongoDB's default _id
    return jsonify(events)