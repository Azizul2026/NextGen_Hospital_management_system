from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)

# Secret key for JWT
app.config["JWT_SECRET_KEY"] = "nextgen_secret_key"

# Initialize extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)

# Demo users (Admin, Doctor, Patient, Receptionist)
users = [
    {
        "username": "admin",
        "password": bcrypt.generate_password_hash("admin123").decode("utf-8"),
        "role": "admin"
    },
    {
        "username": "doctor1",
        "password": bcrypt.generate_password_hash("doctor123").decode("utf-8"),
        "role": "doctor"
    },
    {
        "username": "patient1",
        "password": bcrypt.generate_password_hash("patient123").decode("utf-8"),
        "role": "patient"
    },
    {
        "username": "reception1",
        "password": bcrypt.generate_password_hash("recep123").decode("utf-8"),
        "role": "receptionist"
    }
]

# Home route
@app.route("/")
def home():
    return "NextGen HMS Backend Running"

# LOGIN API
@app.route("/login", methods=["POST"])
def login():

    data = request.json
    username = data.get("username")
    password = data.get("password")

    for user in users:

        if user["username"] == username and bcrypt.check_password_hash(user["password"], password):

            token = create_access_token(identity=username)

            return jsonify({
                "message": "Login successful",
                "token": token,
                "role": user["role"]
            })

    return jsonify({"message": "Invalid credentials"}), 401


# Protected Route
@app.route("/dashboard")
@jwt_required()
def dashboard():

    username = get_jwt_identity()

    return jsonify({
        "message": f"Welcome {username} to the dashboard"
    })


if __name__ == "__main__":
    app.run(debug=True)