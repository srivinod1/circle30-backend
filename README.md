# Circle30 Backend API

This is the backend API for the Circle30 project, providing endpoints for analyzing EV charging infrastructure in Texas cities.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the API

Start the Flask server:
```bash
python app/api.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Chat
- **POST** `/chat`
  - Send a message to the agent
  - Request body: `{"message": "your question here"}`
  - Returns agent's response

### Cities
- **GET** `/cities`
  - Get list of available cities
  - Returns list of city names

### ZIP Scores
- **GET** `/zip-scores?city=<city_name>&top_n=<number>`
  - Get underserved ZIP scores for a city
  - Query parameters:
    - `city`: name of the city
    - `top_n`: number of results (default: 5)

### ZIP Details
- **GET** `/zip-details/<zipcode>`
  - Get detailed information for a specific ZIP code

## Frontend Integration

To connect a frontend chat interface:

1. Make POST requests to `/chat` endpoint with user messages
2. Handle the response format:
```json
{
    "response": "agent's response text"
}
```

Example frontend code (JavaScript):
```javascript
async function sendMessage(message) {
    const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
    });
    const data = await response.json();
    return data.response;
}
```

## Deployment

For production deployment:
1. Use a production-grade WSGI server like Gunicorn
2. Set up proper environment variables
3. Configure CORS if needed
4. Use a reverse proxy like Nginx 