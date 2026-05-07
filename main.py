from math import fabs
from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://www.urdupoint.com/islam/shia/dallas-prayer-timings.html"

response = requests.get(url)

html_content = response.text
soup = BeautifulSoup(html_content, "html.parser")
info = soup.find("table", class_= "main_timings_table names_tbl prayer_table ltr fs15 lh30 mb20")
day = datetime.today()
day_str = day.strftime("%d %B %Y")
prayer_times = []

for row in info.find_all("tr"):
    cols = row.find_all("td")
    if cols:
        prayer_time = cols[0].get_text(strip=True)
        prayer_times.append(prayer_time)

finished_prayer_times = {
    "Fajar" : prayer_times[0],
    "Thuhr" : prayer_times[2],
    "Asr" : prayer_times[3],
    "Maghrib" : prayer_times[4],
    "Isha" : prayer_times[5]
}

print(day_str)

    

