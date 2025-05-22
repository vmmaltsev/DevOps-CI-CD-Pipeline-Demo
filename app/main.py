import os
import logging
from flask import Flask, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Create Flask application
app = Flask(__name__)

# Load configuration from environment variables
app.config["ENV"] = os.getenv("FLASK_ENV", "production")
app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"


@app.route("/")
def index():
    logger.info("Index endpoint called")
    return "Hello, DevOps!"


@app.route("/health")
def health():
    logger.info("Health check endpoint called")
    return jsonify({"status": "healthy"})


@app.errorhandler(404)
def not_found(error):
    logger.error(f"404 error: {error}")
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting application on {host}:{port}")
    app.run(host=host, port=port)
