import os
import logging
import uvicorn
from app.api import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get port from environment variable or default to 8080 (Railway's default)
port = int(os.environ.get("PORT", 8080))

if __name__ == "__main__":
    logger.info(f"Starting application on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
