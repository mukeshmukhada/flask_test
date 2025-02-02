from flask import Flask, send_file, request
import logging
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename="access.log", level=logging.INFO, format="%(asctime)s - %(message)s")

@app.route("/image")
def serve_image():
    # Get client details
    ip = request.remote_addr
    user_agent = request.headers.get("User-Agent")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log the access
    log_message = f"Access from {ip} | Time: {timestamp} | User-Agent: {user_agent}"
    app.logger.info(log_message)

    # Serve the image
    return send_file("image.jpg", mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
