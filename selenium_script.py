from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
import os
import requests

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB setup
client = MongoClient(MONGO_URI)
db = client["twitter_trends"]
collection = db["trending_topics"]

def get_trends():
    # Set up Chrome browser
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://x.com/explore/tabs/trending")

        # Wait for the trending section to load
        wait = WebDriverWait(driver, 30)
        trending_section = wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "Timeline")]'))
        )

        # Extract trending topics
        trending_elements = trending_section.find_elements(By.XPATH, '//div[contains(@class, "css-") and not(contains(@aria-hidden, "true"))]')
        trends = [el.text.strip() for el in trending_elements if el.text.strip()][:5]

        # Handle empty trends
        if not trends:
            trends = ["No data available"] * 5

        # Get public IP address
        try:
            ip_address = requests.get("https://api.ipify.org").text
        except Exception:
            ip_address = "IP address unavailable"

        # Create MongoDB document
        doc = {
            "trend1": trends[0] if len(trends) > 0 else "No data",
            "trend2": trends[1] if len(trends) > 1 else "No data",
            "trend3": trends[2] if len(trends) > 2 else "No data",
            "trend4": trends[3] if len(trends) > 3 else "No data",
            "trend5": trends[4] if len(trends) > 4 else "No data",
            "end_time": datetime.now(),
            "ip_address": ip_address
        }

        # Insert into MongoDB and get the inserted ID
        result = collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)

        return doc

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

if __name__ == "__main__":
    result = get_trends()
    print(result)