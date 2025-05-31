from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        weather_data = None
        error = None
        
        if 'locations' not in session:
            session['locations'] = []
        
        if request.method == 'POST':
            city = request.form.get('city').strip().lower()
            display_name = request.form.get('display_name')
            save_location = request.form.get('save_location')
            
            if city:
                try:
                    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days=5&aqi=no"
                    response = requests.get(url)
                    data = response.json()
                    
                    if response.status_code == 200:
                        weather_data = {
                            'location': f"{data['location']['name']}, {data['location']['country']}",
                            'temp_c': data['current']['temp_c'],
                            'condition': data['current']['condition']['text'],
                            'humidity': data['current']['humidity'],
                            'wind_kph': data['current']['wind_kph'],
                            'feels_like_c': data['current']['feelslike_c'],
                            'weather_type': get_weather_type(data['current']['condition']['text']),
                            'forecast': data['forecast']['forecastday'],
                            'timezone': data['location']['tz_id'],
                            'localtime': data['location']['localtime']
                        }
                        
                        if save_location == 'true':
                            new_location = {
                                'city': city,
                                'name': display_name or data['location']['name'],
                                'temp': data['current']['temp_c']
                            }
                            if not any(loc['city'] == city for loc in session['locations']):
                                session['locations'].append(new_location)
                                session.modified = True
                                
                except Exception as e:
                    error = str(e)
                    print(f"Error fetching weather: {e}")

        return render_template(
            'index.html',
            weather=weather_data,
            error=error,
            locations=session.get('locations', []),
            current_hour=datetime.now().hour
        )
                             
    except Exception as e:
        print(f"Application error: {e}")
        return str(e), 500

@app.route('/delete_location', methods=['POST'])
def delete_location():
    try:
        data = request.get_json()
        city = data.get('city')
        name = data.get('name')
        if 'locations' in session:
            session['locations'] = [
                loc for loc in session['locations']
                if not (loc['city'] == city and loc['name'] == name)
            ]
            session.modified = True
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/edit_location', methods=['POST'])
def edit_location():
    try:
        data = request.get_json()
        city = data.get('city')
        old_name = data.get('old_name')
        new_name = data.get('new_name')
        if 'locations' in session:
            for loc in session['locations']:
                if loc['city'] == city and loc['name'] == old_name:
                    loc['name'] = new_name
                    session.modified = True
                    break
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def get_weather_type(condition):
    condition = condition.lower()
    if any(word in condition for word in ['rain', 'drizzle', 'shower']):
        return 'rainy'
    elif any(word in condition for word in ['cloud', 'overcast']):
        return 'cloudy'
    elif any(word in condition for word in ['clear', 'sunny']):
        return 'clear'
    return 'default'

if __name__ == '__main__':
    os.makedirs('static/media', exist_ok=True)
    if not API_KEY:
        raise ValueError("API_KEY not found in .env file")
    print("Starting Flask application...")
    app.run(debug=True, port=10000)
