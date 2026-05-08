import requests
from datetime import datetime
from flask import Flask, request

#initialize app
app = Flask(__name__)

date = datetime.today().strftime("%d %B %Y") 

# get prayer times 

def get_prayer_timings(): 
    response = requests.get("https://api.aladhan.com/v1/timingsByCity?city=Dallas&country=US&method=0")
    data = response.json()
    
    # Timings is being initialized as a variable to reduce headache and write cleaner code

    timings = data["data"]["timings"]

    # convering timings to am and pm while also puttinng them into a dictionary
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
    return get_prayer_timings()
    

if __name__ == "__main__":
    app.run(debug=True)
