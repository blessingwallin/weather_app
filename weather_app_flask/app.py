from flask import Flask, render_template, request
from dotenv import load_dotenv
import os

from weather import Today, Forecast, Alerts

load_dotenv()
API_KEY = os.getenv("WEATHER_API_KEY")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city')
        option = request.form.get('option')

        try:
            if option == '1':
                today = Today(API_KEY, city)
                data = today.get_data()
                return render_template('today.html', data=data)

            elif option == '2':
                forecast = Forecast(API_KEY, city)
                data = forecast.get_data()
                return render_template('forecast.html', data=data)

            elif option == '3':
                alerts = Alerts(API_KEY, city)
                data = alerts.get_data()
                return render_template('alerts.html', data=data)

            else:
                error = "Invalid option selected."
                return render_template('index.html', error=error)

        except Exception as e:
            return render_template('index.html', error=str(e))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
