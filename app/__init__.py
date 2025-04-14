from flask import Flask
from .tools import list_cities, query_zip_scores, get_zip_details, get_geojson_for_city
from .test_agent import test_agent
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    try:
        # Log environment variables (without sensitive data)
        logger.info("Checking environment variables...")
        logger.info(f"AWS_REGION: {os.getenv('AWS_REGION')}")
        logger.info("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set" if os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY') else "AWS credentials are missing!")
        
        app = Flask(__name__)
        
        # Register blueprints or routes here if needed
        from .api import app as api_blueprint
        app.register_blueprint(api_blueprint)
        
        logger.info("Application created successfully")
        return app
    except Exception as e:
        logger.error(f"Error creating application: {str(e)}")
        raise

# Expose the functions at the package level
__all__ = ['list_cities', 'query_zip_scores', 'get_zip_details', 'get_geojson_for_city', 'test_agent']
