from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv(dotenv_path=".env")

API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and "current" in data:
            weather_data = {
                'location': data['location']['name'],
                'temp_c': data['current']['temp_c'],
                'condition': data['current']['condition']['text']
            }
        else:
            error = data.get('error', {}).get('message', 'Something went wrong')
    
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)
