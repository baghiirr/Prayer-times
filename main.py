import requests
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

date = datetime.today().strftime("%d %B %Y") 

def get_prayer_timings(city="Dallas", country="US"):
    response = requests.get(f"https://api.aladhan.com/v1/timingsByCity?city={city}&country={country}&method=0")
    data = response.json()
    timings = data["data"]["timings"]
    timings_after_convert = {
        "Fajar" : datetime.strptime(timings["Fajr"], "%H:%M").strftime("%I:%M %p").lstrip("0"),
        "Thuhr" : datetime.strptime(timings["Dhuhr"], "%H:%M").strftime("%I:%M %p").lstrip("0"),
        "Asr" : datetime.strptime(timings["Asr"], "%H:%M").strftime("%I:%M %p").lstrip("0"),
        "Maghrib" : datetime.strptime(timings["Maghrib"], "%H:%M").strftime("%I:%M %p").lstrip("0"),
        "Isha" : datetime.strptime(timings["Isha"], "%H:%M").strftime("%I:%M %p").lstrip("0"),
        "Date" : datetime.today().strftime("%d %B %Y") 
    }

    return timings_after_convert







@app.route("/")
def initialize():
    city = request.args.get("city", "Dallas")
    country = request.args.get("country", "US")
    return jsonify(get_prayer_timings(city, country))
    

if __name__ == "__main__":
    app.run(debug=True)
