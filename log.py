from flask import Flask, send_file, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# Use the PostgreSQL connection string from Render
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://image_logs_db_user:o7Bz04na8qRaMpHwDNCyp4V3nKEpgbMw@dpg-cufjhl3tq21c73f6ldog-a/image_logs_db")

# Configure SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Define the Logs table
class AccessLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_agent = db.Column(db.String(500))

# Create the database tables (only needed once)
with app.app_context():
    db.create_all()

@app.route("/image")
def serve_image():
    # Get real client IP from X-Forwarded-For header
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    user_agent = request.headers.get("User-Agent")

    # Save log to the database
    log_entry = AccessLog(ip=ip, user_agent=user_agent)
    db.session.add(log_entry)
    db.session.commit()

    return send_file("image.jpg", mimetype="image/jpeg")

# Route to view the last 10 logs
@app.route("/logs")
def view_logs():
    logs = AccessLog.query.order_by(AccessLog.timestamp.desc()).limit(10).all()
    return "<br>".join([f"{log.timestamp} - {log.ip} - {log.user_agent}" for log in logs])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
