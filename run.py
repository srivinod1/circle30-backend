from app import create_app

# Create the app instance
app = create_app()

# Run the app with debugging enabled
if __name__ == "__main__":
    app.run(debug=True, port=5002)
