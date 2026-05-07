import json
from math import fabs
from bs4 import BeautifulSoup
import requests
from datetime import date, datetime
from flask import Flask, jsonify

app = Flask(__name__)
day = datetime.today()
day_str = day.strftime("%d %B %Y")

def get_prayer_times():
    url = "https://www.urdupoint.com/islam/shia/dallas-prayer-timings.html"

    response = requests.get(url)

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    info = soup.find("table", class_= "main_timings_table names_tbl prayer_table ltr fs15 lh30 mb20")


    prayer_times = []

    for row in info.find_all("tr"):
        cols = row.find_all("td")
        if cols:
            prayer_times.append(cols[0].get_text(strip=True))

    finished_prayer_times = {
        "Fajar" : prayer_times[0],
        "Thuhr" : prayer_times[2],
        "Asr" : prayer_times[3],
        "Maghrib" : prayer_times[4],
        "Isha" : prayer_times[5]
    }

    for prayer, time in finished_prayer_times.items():
        finished_prayer_times[prayer] = datetime.strptime(time, "%H:%M").strftime("%-I:%M %p")


    return {"date": day_str, "times": finished_prayer_times}

print(get_prayer_times())
print(day_str)


result = get_prayer_times()

@app.route('/')
def prayer_api():
    return jsonify(get_prayer_times())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)






    

