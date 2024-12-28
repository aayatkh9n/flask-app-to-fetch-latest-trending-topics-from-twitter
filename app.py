from flask import Flask, jsonify, render_template
from flask_ngrok import run_with_ngrok
from pymongo import MongoClient
import subprocess
import os
from datetime import datetime
from dotenv import load_dotenv
app = Flask(__name__)
run_with_ngrok(app)

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["twitter_trends"]
collection = db["trending_topics"]

# Flask app setup
app = Flask(__name__)

@app.route("/")
def home():
    """
    Render the homepage.
    """
    return render_template("index.html")

@app.route("/run-scraper", methods=["POST"])
def run_scraper():
    """
    Run the Selenium script to scrape Twitter trends and fetch data from MongoDB.
    """
    try:
        # Run the Selenium scraper script
        subprocess.run(["python", "selenium_script.py"], check=True)

        # Fetch the latest data from MongoDB
        latest_data = collection.find_one(sort=[("end_time", -1)])
        if not latest_data:
            return jsonify({"error": "No data found in the database"}), 500

        # Return the latest data as JSON
        response = {
            "trend1": latest_data.get("trend1", "No data"),
            "trend2": latest_data.get("trend2", "No data"),
            "trend3": latest_data.get("trend3", "No data"),
            "trend4": latest_data.get("trend4", "No data"),
            "trend5": latest_data.get("trend5", "No data"),
            "end_time": latest_data.get("end_time", datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "ip_address": latest_data.get("ip_address", "Unavailable"),
        }
        return jsonify(response), 200

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Failed to run the scraper"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
