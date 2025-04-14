from flask import Blueprint, jsonify, request
from tools import list_cities, query_zip_scores, get_zip_details, get_geojson_for_city

# Define a blueprint for the routes
ev_data_bp = Blueprint('ev_data', __name__)

# Route to get all cities
@ev_data_bp.route('/cities', methods=['GET'])
def get_cities():
    try:
        cities = list_cities.invoke(input="")
        return jsonify({"cities": cities}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to get top underserved ZIPs by city
@ev_data_bp.route('/underserved_zips', methods=['GET'])
def get_underserved_zips():
    city = request.args.get('city', default='Austin', type=str)
    top_n = request.args.get('top_n', default=5, type=int)
    try:
        underserved_zips = query_zip_scores.invoke(input=f"{city} {top_n}")
        return jsonify({"underserved_zips": underserved_zips}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to get detailed info for a specific ZIP
@ev_data_bp.route('/zip_details/<zipcode>', methods=['GET'])
def get_zip_details_route(zipcode):
    try:
        zip_details = get_zip_details.invoke(input=zipcode)
        return jsonify({"zip_details": zip_details}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Route to get GeoJSON for a city's ZIPs
@ev_data_bp.route('/geojson', methods=['GET'])
def get_geojson():
    city = request.args.get('city', default='Austin', type=str)
    try:
        geojson = get_geojson_for_city.invoke(input=city)
        return jsonify({"geojson": geojson}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
