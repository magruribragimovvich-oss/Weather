from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    forecast_data = None
    city = None

    if request.method == "POST":
        city = request.form.get("city")

    if city:
        # CURRENT
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            weather = {
                "city": city,
                "temp": data["main"]["temp"],
                "description": data["weather"][0]["description"]
            }

        # FORECAST
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
        forecast_response = requests.get(forecast_url)
        forecast_json = forecast_response.json()

        if forecast_json.get("cod") == "200":
            from datetime import datetime
            raw_list = forecast_json["list"]
            forecast_data = []

            for item in raw_list:
                if "12:00:00" in item["dt_txt"]:
                    date_obj = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    day_name = date_obj.strftime("%a")

                    forecast_data.append({
                        "day": day_name,
                        "temp": item["main"]["temp"],
                        "description": item["weather"][0]["description"],
                        "icon": item["weather"][0]["icon"]
                    })

    return render_template("index.html", weather=weather, forecast=forecast_data)

if __name__ == "__main__":
    app.run(debug=True)