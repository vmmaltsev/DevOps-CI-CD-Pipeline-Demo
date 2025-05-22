import os
import logging
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from prometheus_flask_exporter import PrometheusMetrics

# Load environment variables from .env file if present
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

# Create Flask application
def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config["ENV"] = os.getenv("FLASK_ENV", "production")
    app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"
    
    # Initialize Prometheus metrics
    metrics = PrometheusMetrics(app)
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Register routes
    @app.route("/")
    @metrics.counter('index_requests_total', 'Number of requests to index endpoint')
    def index():
        logger.info(f"Index endpoint called from {request.remote_addr}")
        return "Hello, DevOps!"
    
    @app.route("/health")
    @metrics.counter('health_requests_total', 'Number of requests to health endpoint')
    def health():
        logger.info(f"Health check endpoint called from {request.remote_addr}")
        return jsonify({
            "status": "healthy",
            "version": "1.0.0"
        })
    
    # Register error handlers
    @app.errorhandler(404)
    def not_found(error):
        logger.error(f"404 error: {error}")
        return jsonify({"error": "Not found"}), 404
    
    @app.errorhandler(500)
    def server_error(error):
        logger.error(f"500 error: {error}")
        return jsonify({"error": "Internal server error"}), 500
    
    @app.before_request
    def log_request():
        logger.debug(f"Request: {request.method} {request.path} from {request.remote_addr}")
        
    @app.after_request
    def log_response(response):
        logger.debug(f"Response: {response.status_code}")
        return response
        
    return app

# Create the Flask app instance
app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    logger.info(f"Starting application on {host}:{port}")
    app.run(host=host, port=port)
