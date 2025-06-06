from flask import Blueprint, json, request, jsonify

# Importing MongoDB
from app.extensions import collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():

    # receiving the json data from action-repo
    if request.headers.get('Content-Type') == 'application/json':
        payload = request.json

        # Extracting the event_type from json, i.e. Push, Pull or Merge
        event_type = request.headers.get('X-GitHub-Event')


        # Checking the type of event and inserting the data in MngoDB accordingly
        if event_type == 'pull_request':
            pr = payload.get("pull_request", {})
            action = payload.get("action")


            is_merged = pr.get("merged", False)

            data = {
                "request_id": str(pr.get("id")),
                "author": pr.get("user", {}).get("login"),
                "action": "MERGE" if action == "closed" and is_merged else "PULL REQUEST",
                "from_branch": pr.get("head", {}).get("ref"),
                "to_branch": pr.get("base", {}).get("ref"),
                "timestamp": pr.get("updated_at")
            }

            # Inserting daat to MongoDB
            collection.insert_one(data)
            return jsonify({"message": "Pull Request data saved"}), 200

        elif event_type == 'push':
            data = {
                "request_id": payload.get("after"),  # commit hash
                "author": payload.get("pusher", {}).get("name"),
                "action": "PUSH",
                "from_branch": payload.get("ref").split("/")[-1],  # refs/heads/main -> main
                "to_branch": None,  # Not applicable in push
                "timestamp": payload.get("head_commit", {}).get("timestamp")
            }

            collection.insert_one(data)
            return jsonify({"message": "Push data saved"}), 200
        
        return jsonify({"message": f"Ignored event: {event_type}"}), 200

    return jsonify({"error": "Invalid Content-Type"}), 400

@webhook.route('/get-updates', methods=["GET"])

# Function to deliver data to frontend on GET Request 
def get_updates():
    events = list(collection.find({}, {"_id": 0}))  # exclude MongoDB's default _id
    return jsonify(events)