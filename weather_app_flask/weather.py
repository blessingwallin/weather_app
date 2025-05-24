import requests
from datetime import datetime

class Today:
    def __init__(self, api_key, city):
        URL = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
        data = requests.get(URL).json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        self.city = data['location']['name']
        self.region = data['location']['region']
        self.country = data['location']['country']
        self.temp_f = data['current']['temp_f']
        self.condition = data['current']['condition']['text']
        self.pressure = data['current']['pressure_mb']
        self.humidity = data['current']['humidity']
        self.wind_mph = data['current']['wind_mph']

    def get_data(self):
        return {
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "temp_f": self.temp_f,
            "condition": self.condition,
            "pressure": self.pressure,
            "humidity": self.humidity,
            "wind_mph": self.wind_mph,
        }

class Forecast:
    def __init__(self, api_key, city):
        URL = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=3"
        data = requests.get(URL).json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        self.city = data['location']['name']
        self.region = data['location']['region']
        self.country = data['location']['country']
        self.forecast_days = []

        for day in data['forecast']['forecastday']:
            self.forecast_days.append({
                "date": datetime.strptime(day['date'], "%Y-%m-%d").strftime("%B %d, %Y"),
                "condition": day['day']['condition']['text'],
                "high": day['day']['maxtemp_f'],
                "low": day['day']['mintemp_f'],
                "humidity": day['day']['avghumidity'],
                "wind": day['day']['maxwind_mph'],
                "precip": day['day']['totalprecip_in'],
            })

    def get_data(self):
        return {
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "forecast_days": self.forecast_days
        }

class Alerts:
    def __init__(self, api_key, city):
        URL = f"http://api.weatherapi.com/v1/alerts.json?key={api_key}&q={city}&aqi=no"
        data = requests.get(URL).json()

        if "error" in data:
            raise Exception(data["error"]["message"])

        self.city = data['location']['name']
        self.region = data['location']['region']
        self.country = data['location']['country']
        self.alerts = data.get("alerts", {}).get("alert", [])

        # Deduplicate alerts if needed
        seen = set()
        unique_alerts = []
        for alert in self.alerts:
            key = (alert["headline"], alert["areas"], alert["effective"])
            if key not in seen:
                seen.add(key)
                unique_alerts.append(alert)
        self.alerts = unique_alerts

    def get_data(self):
        alerts_list = []
        for alert in self.alerts:
            alerts_list.append({
                "headline": alert['headline'],
                "severity": alert['severity'],
                "areas": alert['areas'],
                "effective": alert['effective'],
                "expires": alert['expires'],
            })
        return {
            "city": self.city,
            "region": self.region,
            "country": self.country,
            "alerts": alerts_list
        }
