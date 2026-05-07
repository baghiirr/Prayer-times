from bs4 import BeautifulSoup
import requests
from datetime import datetime
from flask import Flask, jsonify

app = Flask(__name__)

def get_prayer_times():
    url = "https://www.urdupoint.com/islam/shia/dallas-prayer-timings.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    response = requests.get(url, headers=headers)

    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    info = soup.find("table", class_= "main_timings_table names_tbl prayer_table ltr fs15 lh30 mb20")

    if info is None:
        return {"error": "Could not fetch prayer times", "status": response.status_code}


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

    day_str = datetime.today().strftime("%d %B %Y")

    for prayer, time in finished_prayer_times.items():
        t = datetime.strptime(time, "%H:%M")
        finished_prayer_times[prayer] = t.strftime("%I:%M %p").lstrip("0")

    return {"date": day_str, "times": finished_prayer_times}

@app.route('/')
def prayer_api():
    return jsonify(get_prayer_times())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)






    

