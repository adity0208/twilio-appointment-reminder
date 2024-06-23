from waitress import serve
from app import app  # Import your Flask app

print("Starting server...")

if __name__ == "__main__":
    try:
        serve(app, host="0.0.0.0", port=8081)  # Adjust the port as needed
    except Exception as e:
        print(f"Error starting server: {e}")
from waitress import serve
from app import app  # Import your Flask app

print("Starting server...")

if __name__ == "__main__":
    try:
        serve(app, host="0.0.0.0", port=8081)  # Adjust the port as needed
    except Exception as e:
        print(f"Error starting server: {e}")
