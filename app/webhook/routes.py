from flask import Blueprint, json, request, jsonify
from app.extensions import collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/test-mongo', methods=["GET"])
def test_mongo():
    try:
        # Try to insert a test document
        test_doc = {"test": "connection"}
        collection.insert_one(test_doc)
        # Try to read it back
        result = collection.find_one({"test": "connection"})
        # Clean up: remove the test document
        collection.delete_one({"test": "connection"})
        return jsonify({"success": True, "result": str(result)}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@webhook.route('/receiver', methods=["POST"])
def receiver():
    if request.headers.get('Content-Type') == 'application/json':
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')  # to verify it's a PR event

        if event_type == 'pull_request':
            pr = payload.get("pull_request", {})
            action = payload.get("action")

            # Check if it was merged
            is_merged = pr.get("merged", False)

            data = {
                "request_id": str(pr.get("id")),
                "author": pr.get("user", {}).get("login"),
                "action": "MERGE" if action == "closed" and is_merged else "PULL REQUEST",
                "from_branch": pr.get("head", {}).get("ref"),
                "to_branch": pr.get("base", {}).get("ref"),
                "timestamp": pr.get("updated_at")
            }

            print(data)
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

            print(data)
            collection.insert_one(data)
            return jsonify({"message": "Push data saved"}), 200
        
        return jsonify({"message": f"Ignored event: {event_type}"}), 200

    return jsonify({"error": "Invalid Content-Type"}), 400

@webhook.route('/get-updates', methods=["GET"])
def get_updates():
    events = list(collection.find({}, {"_id": 0}))  # exclude MongoDB's default _id
    return jsonify(events)