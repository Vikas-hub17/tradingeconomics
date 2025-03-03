from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

app = Flask(__name__)

def fetch_country_data(country):
    url = f"https://api.tradingeconomics.com/country/{country}?c={API_KEY}"
    print(f"Fetching URL: {url}")  # Debugging
    
    try:
        response = requests.get(url)
        print(f"Response Status: {response.status_code}")  # Debugging
        print(f"Response Data: {response.text}")  # Debugging

        data = response.json()
        return data if response.status_code == 200 else {"error": "Invalid response"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/json/<string:country>')
def show_json_page(country):
    data = fetch_country_data(country)
    return render_template('json_display.html', data=data)

# Homepage with search form
@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None

    if request.method == "POST":
        country = request.form.get("country")
        if country:
            data = fetch_country_data(country)
            if "error" in data:
                error = data["error"]

    return render_template("index.html", data=data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
