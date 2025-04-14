from app import create_app
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the app instance
app = create_app()

# Get port from environment variable or default to 8080 (Railway's default)
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    logger.info(f"Starting application on port {port}")
    app.run(host="0.0.0.0", port=port)
