from flask import Blueprint, jsonify, request, send_from_directory
from app import test_agent
import logging

logger = logging.getLogger(__name__)

# Create a blueprint for the API routes
app = Blueprint('api', __name__)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint for chat interactions with the agent.
    Expects a JSON payload with a 'message' field.
    """
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
            
        logger.info(f"Received chat message: {data['message']}")
        response = test_agent(data['message'])
        logger.info("Agent response generated successfully")
        return jsonify({"response": response}), 200
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
