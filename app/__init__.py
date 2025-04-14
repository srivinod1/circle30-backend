from flask import Flask
from .tools import list_cities, query_zip_scores, get_zip_details, get_geojson_for_city
from .test_agent import test_agent

def create_app():
    app = Flask(__name__)
    
    # Register blueprints or routes here if needed
    from .api import app as api_blueprint
    app.register_blueprint(api_blueprint)
    
    return app

# Expose the functions at the package level
__all__ = ['list_cities', 'query_zip_scores', 'get_zip_details', 'get_geojson_for_city', 'test_agent']
