# Prayer Times Widget

An iPhone widget that displays daily prayer times for any city, with automatic notifications at each prayer time.

## Features
- Shows all 5 daily prayer times (Fajr, Dhuhr, Asr, Maghrib, Isha)
- Highlights the current prayer
- Sends a notification at each prayer time
- Supports multiple cities worldwide
- Updates automatically every day

## Setup

### 1. Install Scriptable
Download [Scriptable](https://apps.apple.com/app/scriptable/id1405459188) from the App Store (free).

### 2. Add the script
1. Open Scriptable
2. Tap **+** to create a new script
3. Paste the contents of `widget.js`
4. Tap **Run** to test — a city picker will appear on first run

### 3. Add the widget to your home screen
1. Long press your home screen
2. Tap **+** → search **Scriptable**
3. Choose the **medium** size widget
4. Tap the widget → select your prayer times script

### 4. Set up automatic daily refresh (recommended)
1. Open the **Shortcuts** app
2. Tap **Automation** → **+** → **Time of Day**
3. Set time to **4:00 AM**
4. Turn off "Ask Before Running"
5. Add action → **Scriptable** → **Run Script** → select your script
6. Save

This schedules notifications for all 5 prayers every morning.

## Supported Cities
- Dallas, US
- New York, US
- Chicago, US
- Los Angeles, US
- Houston, US
- London, GB
- Karachi, PK
- Lahore, PK
- Dubai, AE
- Toronto, CA

To add more cities, edit the `cities` array in `widget.js`.

## Changing Your City
Delete `prayerConfig.json` from Scriptable's file browser and run the script again to pick a new city.
