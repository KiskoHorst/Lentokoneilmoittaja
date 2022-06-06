# Lentokoneilmoittaja
Telegram notifications for ADS-B equipped airplanes using dump1090 aircraft.json

# Required files
* config.json:
```
{
  "aircraft_json_url": "<url of dump1090 aircraft.json>",
  "telegram_bot_token": "<Telegram bot token>",
  "telegram_chat_id": "<Telegram chat ID>",
  "planespotters_session_token": "<Planespotters login session token, from the cookie ps_sessid>"
}
```
* aircrafts.json:
Generate using tar1090-db
* newTypes.json:
Generate using tar1090-db
