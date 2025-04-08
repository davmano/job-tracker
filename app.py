from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Config SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jobs.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize DB
db = SQLAlchemy(app)

# Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "company": self.company,
            "position": self.position,
            "status": self.status
        }

# Create the tables
with app.app_context():
    db.create_all()

# Routes
@app.route("/")
def home():
    return "Welcome to the Job Tracker API!"

@app.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    return jsonify([job.to_dict() for job in jobs])

@app.route("/jobs", methods=["POST"])
def add_job():
    data = request.json
    new_job = Job(
        company=data["company"],
        position=data["position"],
        status=data["status"]
    )
    db.session.add(new_job)
    db.session.commit()
    return jsonify(new_job.to_dict()), 201

@app.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    data = request.json
    job.company = data.get("company", job.company)
    job.position = data.get("position", job.position)
    job.status = data.get("status", job.status)
    db.session.commit()
    return jsonify(job.to_dict())

@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    job = Job.query.get(job_id)
    if not job:
        return jsonify({"error": "Job not found"}), 404

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted successfully!"})

# Run the app on port 5001
if __name__ == "__main__":
    app.run(debug=True, port=5001)
