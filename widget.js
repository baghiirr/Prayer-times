const fm = FileManager.local()
const configPath = fm.joinPath(fm.documentsDirectory(), "prayerConfig.json")

const cities = [
  { name: "Dallas", country: "US" },
  { name: "New York", country: "US" },
  { name: "Chicago", country: "US" },
  { name: "Los Angeles", country: "US" },
  { name: "Houston", country: "US" },
  { name: "London", country: "UK" },
  { name: "Karachi", country: "PK" },
  { name: "Lahore", country: "PK" },
  { name: "Dubai", country: "AE" },
  { name: "Toronto", country: "CA" },
]

let config
if (!fm.fileExists(configPath)) {
  const alert = new Alert()
  alert.title = "Select Your City"
  for (const city of cities) {
    alert.addAction(`${city.name}, ${city.country}`)
  }
  alert.addCancelAction("Cancel")
  const index = await alert.present()
  if (index === -1) return
  config = cities[index]
  fm.writeString(configPath, JSON.stringify(config))
} else {
  config = JSON.parse(fm.readString(configPath))
}

const url = `https://prayer-times-2fg1.onrender.com?city=${config.name}&country=${config.country}`
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
  if (now >= t) currentPrayer = prayers[i]
}

const widget = new ListWidget()
const gradient = new LinearGradient()
gradient.colors = [new Color("#4f6ef7"), new Color("#7b5ea7")]
gradient.locations = [0, 1]
widget.backgroundGradient = gradient
widget.setPadding(12, 14, 12, 14)

const topRow = widget.addStack()
topRow.layoutHorizontally()
const nameText = topRow.addText(currentPrayer.name)
nameText.textColor = Color.white()
nameText.font = Font.boldSystemFont(22)
topRow.addSpacer()
const timeText = topRow.addText(currentPrayer.time)
timeText.textColor = Color.white()
timeText.font = Font.boldSystemFont(22)

widget.addSpacer(6)

const cityLabel = widget.addText(`${config.name} • ${data.Date}`)
cityLabel.textColor = new Color("#ffffff", 0.6)
cityLabel.font = Font.systemFont(10)

widget.addSpacer(8)

const bottomRow = widget.addStack()
bottomRow.layoutHorizontally()

for (const prayer of prayers) {
  const col = bottomRow.addStack()
  col.layoutVertically()
  col.centerAlignContent()

  const sf = SFSymbol.named(prayer.icon)
  const img = col.addImage(sf.image)
  img.imageSize = new Size(24, 24)
  img.tintColor = prayer.name === currentPrayer.name ? Color.white() : new Color("#ffffff", 0.6)

  col.addSpacer(4)

  const t = col.addText(prayer.time)
  t.font = Font.boldSystemFont(prayer.name === currentPrayer.name ? 14 : 12)
  t.textColor = prayer.name === currentPrayer.name ? Color.white() : new Color("#ffffff", 0.6)
  t.centerAlignText()

  col.addSpacer(2)

  const n = col.addText(prayer.name)
  n.font = Font.systemFont(10)
  n.textColor = prayer.name === currentPrayer.name ? Color.white() : new Color("#ffffff", 0.6)
  n.centerAlignText()

  if (prayer !== prayers[prayers.length - 1]) bottomRow.addSpacer()
}

Script.setWidget(widget)
widget.presentMedium()
Script.complete()