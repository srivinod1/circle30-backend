from flask import Blueprint, jsonify, request, send_from_directory
from app import list_cities, query_zip_scores, get_zip_details, get_geojson_for_city, test_agent

# Create a blueprint for the API routes
app = Blueprint('api', __name__)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for chat interactions with the agent.
    Expects a JSON payload with a 'message' field.
    """
    try:
        print("Received request:", request.get_data())  # Log raw request data
        data = request.get_json()
        print("Parsed JSON:", data)  # Log parsed JSON
        
        if not data:
            print("Error: No JSON data received")
            return jsonify({"error": "No JSON data received"}), 400
            
        if 'message' not in data:
            print("Error: 'message' field missing in JSON")
            return jsonify({"error": "Missing 'message' in request body"}), 400
            
        # Use the test_agent function which properly sets up the agent with tools
        response = test_agent(data['message'])
        return jsonify({"response": response}), 200
    except Exception as e:
        print(f"Error in /chat: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

@app.route('/cities', methods=['GET'])
def get_cities():
    """
    Endpoint to get list of available cities.
    """
    try:
        cities = list_cities.invoke("")  # Empty input since no parameters needed
        return jsonify({"cities": cities}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/zip-scores', methods=['GET'])
def get_zip_scores():
    """
    Endpoint to get underserved ZIP scores for a city.
    Query parameters:
    - city: name of the city
    """
    try:
        city = request.args.get('city', '')
        result = query_zip_scores(city)  # Direct function call instead of invoke
        return jsonify({"result": result}), 200
    except Exception as e:
        print(f"Error in /zip-scores: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

@app.route('/zip-details/<zipcode>', methods=['GET'])
def get_zip_details_endpoint(zipcode):
    """
    Endpoint to get detailed information for a specific ZIP code.
    """
    try:
        result = get_zip_details.invoke({"zipcode": zipcode})
        return jsonify({"result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
