from flask import Flask, request, render_template, jsonify
import os, json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load Firebase credentials
service_account_json = os.getenv("SERVICE_ACCOUNT_JSON")
service_account_dict = json.loads(service_account_json)

cred = credentials.Certificate(service_account_dict)
firebase_admin.initialize_app(cred)

db = firestore.client()

# ------------------------------
#            ROUTES
# ------------------------------

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/verify")
def verify_page():
    return render_template("verify.html")

@app.route("/recharge_page")
def recharge_page():
    return render_template("recharge.html")

@app.route("/balance_page")
def balance_page():
    return render_template("balance.html")


# ------------------------------
#        CREATE USER
# ------------------------------
@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")

    if not name or not phone:
        return jsonify({"error": "Missing fields"}), 400

    user = db.collection("users").add({
        "name": name,
        "phone": phone,
        "verified": False,
        "balance": 0
    })

    return jsonify({"message": "Account Created", "user_id": user[1].id})


# ------------------------------
#        VERIFY USER
# ------------------------------
@app.route("/verify_user", methods=["POST"])
def verify_user():
    user_id = request.json.get("user_id")

    user_ref = db.collection("users").document(user_id)
    data = user_ref.get()

    if not data.exists:
        return jsonify({"error": "User Not Found"}), 404

    user_ref.update({"verified": True})

    return jsonify({"message": "User Verified"})


# ------------------------------
#          RECHARGE
# ------------------------------
@app.route("/recharge", methods=["POST"])
def recharge():
    data = request.json
    user_id = data.get("user_id")
    amount = int(data.get("amount"))

    user_ref = db.collection("users").document(user_id)
    user = user_ref.get()

    if not user.exists:
        return jsonify({"error": "User Not Found"}), 404

    user = user.to_dict()

    if not user["verified"]:
        return jsonify({"error": "User Not Verified"}), 403

    new_balance = user["balance"] + amount
    user_ref.update({"balance": new_balance})

    db.collection("recharges").add({
        "user_id": user_id,
        "amount": amount,
        "timestamp": firestore.SERVER_TIMESTAMP
    })

    return jsonify({"message": "Recharge Successful", "balance": new_balance})


# ------------------------------
#         CHECK BALANCE
# ------------------------------
@app.route("/get_balance", methods=["POST"])
def get_balance():
    user_id = request.json.get("user_id")

    user_ref = db.collection("users").document(user_id).get()

    if not user_ref.exists:
        return jsonify({"error": "User Not Found"}), 404

    return jsonify({"balance": user_ref.to_dict()["balance"]})


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
