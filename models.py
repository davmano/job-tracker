from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///job_tracker.db'  # Using SQLite for development
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Hashed password
    jobs = db.relationship('Job', backref='user', lazy=True)

# Job Model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Applied')  # e.g., Applied, Interview, Offer, Rejected
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    print("Database tables created successfully!")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure SQLite (change this to PostgreSQL if needed)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///job_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define Job model
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    status = db.Column(db.String(50), default="Pending")
    date_applied = db.Column(db.DateTime)
    notes = db.Column(db.Text)

# Run this only when creating the database
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database and tables created successfully!")

