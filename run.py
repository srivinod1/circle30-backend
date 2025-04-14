from app import create_app
import os

# Create the app instance
app = create_app()

# Get port from environment variable or default to 5002
port = int(os.environ.get("PORT", 5002))

# Run the app with debugging enabled
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
