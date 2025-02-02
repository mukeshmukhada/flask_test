from flask import Flask, send_file, request
from datetime import datetime
import os

app = Flask(__name__)

# Set the path to the image you want to serve
IMAGE_PATH = r"C:\Users\Admin\Desktop\Shyamal\Python\Flask\img_1.png"  # Replace with the actual path to your image
LOG_FILE = 'access_logs.txt'

# Create a helper function to log access
def log_access(ip, user_agent):
    log_data = {
        "ip": ip,
        "user_agent": user_agent,
        "timestamp": datetime.now().isoformat()
    }
    with open(LOG_FILE, 'a') as log_file:
        log_file.write(f"{log_data}\n")

@app.route('/image')
def serve_image():
    # Get access info
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Log the access
    log_access(ip, user_agent)

    # Send the image
    return send_file(IMAGE_PATH, mimetype='image/jpeg')

if __name__ == '__main__':
    # Run the Flask application
    app.run(host='0.0.0.0', port=5000,debug=True)
