from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from neo4j import GraphDatabase

app = Flask(__name__)

# Enable CORS (VERY IMPORTANT for GitHub Pages)
CORS(app, resources={r"/*": {"origins": "*"}})

# Secret key for JWT
app.config["JWT_SECRET_KEY"] = "nextgen_secret_key"

# Initialize extensions
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Neo4j connection
uri = "bolt://127.0.0.1:7687"
username = "neo4j"
password = "neo4j123"

driver = GraphDatabase.driver(uri, auth=(username, password))

# Demo users
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


# Protected dashboard
@app.route("/dashboard")
@jwt_required()
def dashboard():

    username = get_jwt_identity()

    return jsonify({
        "message": f"Welcome {username} to the dashboard"
    })


# Patient submits details
@app.route("/add_patient", methods=["POST"])
def add_patient():

    data = request.json

    name = data.get("name")
    age = data.get("age")
    cause = data.get("cause")

    with driver.session() as session:
        session.run(
            "CREATE (p:Patient {name:$name, age:$age, cause:$cause})",
            name=name,
            age=age,
            cause=cause
        )

    return jsonify({
        "message": "Patient added successfully"
    })


# Admin sees all patients
@app.route("/patients", methods=["GET"])
@jwt_required()
def get_patients():

    with driver.session() as session:

        result = session.run("MATCH (p:Patient) RETURN p")

        patients = []

        for record in result:
            p = record["p"]
            patients.append(dict(p))

    return jsonify(patients)


# Admin assigns doctor + appointment
@app.route("/assign_doctor", methods=["POST"])
@jwt_required()
def assign_doctor():

    data = request.json

    patient = data.get("patient")
    doctor = data.get("doctor")
    date = data.get("date")

    with driver.session() as session:

        session.run("""
        MATCH (p:Patient {name:$patient})
        MERGE (d:Doctor {name:$doctor})
        CREATE (p)-[:APPOINTMENT {date:$date}]->(d)
        """,
        patient=patient,
        doctor=doctor,
        date=date)

    return jsonify({
        "message": "Doctor assigned successfully"
    })


# Doctor sees assigned patients
@app.route("/doctor_patients/<doctor>", methods=["GET"])
@jwt_required()
def doctor_patients(doctor):

    with driver.session() as session:

        result = session.run("""
        MATCH (p:Patient)-[r:APPOINTMENT]->(d:Doctor {name:$doctor})
        RETURN p.name AS patient, p.cause AS cause, r.date AS date
        """, doctor=doctor)

        data = []

        for record in result:
            data.append({
                "patient": record["patient"],
                "cause": record["cause"],
                "date": record["date"]
            })

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
