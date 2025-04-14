from flask import Flask
from .tools import list_cities, query_zip_scores, get_zip_details, get_geojson_for_city
from .test_agent import test_agent
import logging

logger = logging.getLogger(__name__)

def create_app():
    try:
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
