from flask import Flask, request, jsonify

app = Flask(name)

# المفاتيح (تتحكم منها)
users = {
    "dark-001": {"active": True},
    "dark-002": {"active": False},
}

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    key = data.get("key")

    if key in users:
        if users[key]["active"]:
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "banned"})
    else:
        return jsonify({"status": "invalid"})

app.run(host="0.0.0.0", port=5000)
