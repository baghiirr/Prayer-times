const fm = FileManager.local()
const configPath = fm.joinPath(fm.documentsDirectory(), "prayerConfig.json")

let config
if (!fm.fileExists(configPath)) {
  const alert = new Alert()
  alert.title = "Prayer Times Setup"
  alert.message = "Enter your city and country code (e.g. US, GB, PK)"
  alert.addTextField("City", "Dallas")
  alert.addTextField("Country Code", "US")
  alert.addAction("Save")
  await alert.present()
  config = { city: alert.textFieldValue(0), country: alert.textFieldValue(1) }
  fm.writeString(configPath, JSON.stringify(config))
} else {
  config = JSON.parse(fm.readString(configPath))
}

const url = `https://your-render-url.onrender.com?city=${config.city}&country=${config.country}`
const data = await new Request(url).loadJSON()

const prayers = [
  { name: "Fajr", time: data.Fajar, icon: "sunrise" },
  { name: "Dhuhr", time: data.Thuhr, icon: "sun.max" },
  { name: "Asr", time: data.Asr, icon: "sun.min" },
  { name: "Maghrib", time: data.Maghrib, icon: "sunset" },
  { name: "Isha", time: data.Isha, icon: "moon" },
]

function parseTime(str) {
  const [time, period] = str.split(" ")
  let [h, m] = time.split(":").map(Number)
  if (period === "PM" && h !== 12) h += 12
  if (period === "AM" && h === 12) h = 0
  const now = new Date()
  return new Date(now.getFullYear(), now.getMonth(), now.getDate(), h, m)
}

const now = new Date()
let currentPrayer = prayers[prayers.length - 1]

for (let i = 0; i < prayers.length; i++) {
  const t = parseTime(prayers[i].time)
  if (now >= t) {
    currentPrayer = prayers[i]
  }
}

const widget = new Lis