from flask import Flask, render_template, request, session, jsonify, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import re
# Authentication imports
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import jwt
import random
import string
import time
from twilio.rest import Client

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
load_dotenv()

API_KEY = os.getenv('WEATHER_API_KEY')
# Authentication configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
FIREBASE_API_KEY = os.getenv('FIREBASE_API_KEY')
FIREBASE_AUTH_DOMAIN = os.getenv('FIREBASE_AUTH_DOMAIN')
FIREBASE_PROJECT_ID = os.getenv('FIREBASE_PROJECT_ID')

TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
TWILIO_FROM = os.getenv('TWILIO_FROM')

# Print configuration status
print("=== Authentication Configuration ===")
print(f"Weather API Key: {'✓ Configured' if API_KEY else '✗ Missing'}")
print(f"Google Client ID: {'✓ Configured' if GOOGLE_CLIENT_ID else '✗ Missing (Google sign-in disabled)'}")
print(f"Firebase Config: {'✓ Configured' if FIREBASE_API_KEY else '✗ Missing (Phone auth disabled)'}")
print("=====================================")

# In-memory storage for verification codes (use Redis or database in production)
verification_codes = {}

def require_auth(f):
    """Decorator to require authentication for routes"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth_page'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/auth')
def auth_page():
    """Authentication page"""
    if 'user' in session:
        return redirect(url_for('index'))
    
    # Get error message from URL parameter (from OAuth callback)
    error_message = request.args.get('error')
    
    # Safe configuration values (handle None values)
    google_client_id = GOOGLE_CLIENT_ID if GOOGLE_CLIENT_ID else ""
    firebase_api_key = FIREBASE_API_KEY if FIREBASE_API_KEY else ""
    firebase_auth_domain = FIREBASE_AUTH_DOMAIN if FIREBASE_AUTH_DOMAIN else ""
    firebase_project_id = FIREBASE_PROJECT_ID if FIREBASE_PROJECT_ID else ""
    #print("FIREBASE_API_KEY:", FIREBASE_API_KEY)
    return render_template('auth.html', 
                         google_client_id=google_client_id,
                         firebase_api_key=firebase_api_key,
                         firebase_auth_domain=firebase_auth_domain,
                         firebase_project_id=firebase_project_id,
                         error=error_message)

@app.route('/auth/google/callback')
def google_callback():
    """Handle Google OAuth callback"""
    try:
        code = request.args.get('code')
        error = request.args.get('error')
        
        if error:
            print(f"Google OAuth error: {error}")
            return redirect(url_for('auth_page', error=f'Google authentication failed: {error}'))
        
        if not code:
            return redirect(url_for('auth_page', error='Google authentication was cancelled'))
        
        # Check if Google authentication is configured
        if not GOOGLE_CLIENT_ID:
            return redirect(url_for('auth_page', error='Google authentication is not configured'))
        
        # Exchange authorization code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        redirect_uri = request.url_root.rstrip('/') + '/auth/google/callback'
        
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),  # Optional for some flows
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        
        print(f"Exchanging code for token with redirect_uri: {redirect_uri}")
        
        # Get access token
        token_response = requests.post(token_url, data=token_data)
        token_info = token_response.json()
        
        if 'access_token' not in token_info:
            print(f"Token exchange failed: {token_info}")
            return redirect(url_for('auth_page', error='Failed to exchange authorization code'))
        
        # Get user information
        userinfo_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token_info['access_token']}"
        user_response = requests.get(userinfo_url)
        user_info = user_response.json()
        
        if 'email' not in user_info:
            print(f"Failed to get user info: {user_info}")
            return redirect(url_for('auth_page', error='Failed to get user information'))
        
        # Create user session
        session['user'] = {
            'id': user_info['id'],
            'email': user_info['email'],
            'name': user_info.get('name', user_info['email']),
            'picture': user_info.get('picture', ''),
            'auth_method': 'google'
        }
        session['authenticated'] = True
        session['just_logged_in'] = True
        
        print(f"Google OAuth authentication successful for: {user_info['email']}")
        return redirect(url_for('index'))
        
    except Exception as e:
        print(f"Google callback error: {e}")
        import traceback
        traceback.print_exc()
        return redirect(url_for('auth_page', error='Google authentication failed'))

@app.route('/auth/google', methods=['POST'])
def google_auth():
    """Handle Google authentication"""
    try:
        # Check if Google authentication is configured
        if not GOOGLE_CLIENT_ID:
            return jsonify({'success': False, 'error': 'Google authentication is not configured on this server'})
        
        data = request.get_json()
        credential = data.get('credential')
        
        if not credential:
            return jsonify({'success': False, 'error': 'No credential provided'})
        
        # Verify the Google token
        try:
            idinfo = id_token.verify_oauth2_token(
                credential, google_requests.Request(), GOOGLE_CLIENT_ID)
            
            print(f"Token verification successful for: {idinfo.get('email', 'unknown')}")
            
        except ValueError as e:
            print(f"Google token verification failed: {e}")
            return jsonify({'success': False, 'error': f'Invalid Google token: {str(e)}'})
        
        # Check if token is for the correct client
        if idinfo.get('aud') != GOOGLE_CLIENT_ID:
            print(f"Token audience mismatch: {idinfo.get('aud')} != {GOOGLE_CLIENT_ID}")
            return jsonify({'success': False, 'error': 'Invalid token audience'})
        
        # Create user session
        session['user'] = {
            'id': idinfo['sub'],
            'email': idinfo['email'],
            'name': idinfo.get('name', idinfo['email']),
            'picture': idinfo.get('picture', ''),
            'auth_method': 'google'
        }
        session['authenticated'] = True
        session['just_logged_in'] = True
        
        print(f"Google authentication successful for: {idinfo['email']}")
        return jsonify({'success': True, 'redirect': url_for('index')})
        
    except Exception as e:
        print(f"Google authentication error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': 'Authentication failed. Please try again.'})

@app.route('/auth/phone/send', methods=['POST'])
def send_phone_verification():
    """Send verification code for phone authentication"""
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return jsonify({'success': False, 'error': 'Phone number required'})
        
        # Validate phone number format
        phone_pattern = r'^\+[1-9]\d{1,14}$'
        if not re.match(phone_pattern, phone):
            return jsonify({'success': False, 'error': 'Please enter a valid phone number with country code (e.g., +1234567890)'})
        
        # Generate random 6-digit code
        code = ''.join(random.choices(string.digits, k=6))
        
        # Store verification code with timestamp (expires in 5 minutes)
        verification_codes[phone] = {
            'code': code,
            'timestamp': time.time(),
            'attempts': 0
        }
        
        # In production, send SMS using Twilio, AWS SNS, or Firebase
        send_sms(phone, f"Your Weather App verification code is: {code}")
        print(f"📱 Sent verification code to {phone}")
        
        return jsonify({
            'success': True, 
            'message': 'Verification code sent'
        })
        
    except Exception as e:
        print(f"Phone verification send error: {e}")
        return jsonify({'success': False, 'error': 'Failed to send verification code. Please try again.'})

@app.route('/auth/phone/verify', methods=['POST'])
def verify_phone():
    data = request.get_json()
    uid = data.get('uid')
    phone = data.get('phone')
    code = data.get('code')

    # If using Firebase (uid present), do not require code
    if uid and phone:
        session['user'] = {
            'id': uid,
            'phone': phone,
            'auth_method': 'phone',
            'name': phone,
            'email': '',
            'picture': ''
        }
        return jsonify({'success': True, 'redirect': url_for('index')})

    # Fallback: demo/server mode (code required)
    if phone and code:
        return jsonify({'success': False, 'error': 'Server-side code verification not implemented'})

    return jsonify({'success': False, 'error': 'Phone and code required'})

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('auth_page'))

@app.route('/', methods=['GET', 'POST'])
@require_auth
def index():
    try:
        weather_data = None
        error = None
        
        # Initialize user-specific locations
        user_id = session['user']['id']
        if 'user_locations' not in session:
            session['user_locations'] = {}
        if user_id not in session['user_locations']:
            session['user_locations'][user_id] = []
        
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
                            # Check if location already exists and update it, or add new one
                            user_locations = session['user_locations'][user_id]
                            existing_location = None
                            for i, loc in enumerate(user_locations):
                                if loc['city'] == city:
                                    existing_location = i
                                    break
                            
                            if existing_location is not None:
                                # Update existing location
                                session['user_locations'][user_id][existing_location] = new_location
                                print(f"Updated existing location: {new_location}")
                            else:
                                # Add new location
                                session['user_locations'][user_id].append(new_location)
                                print(f"Added new location: {new_location}")
                            
                            session.modified = True
                                
                except Exception as e:
                    error = str(e)
                    print(f"Error fetching weather: {e}")

        response = render_template(
            'index.html',
            weather=weather_data,
            error=error,
            locations=session['user_locations'].get(user_id, []),
            current_hour=datetime.now().hour,
            user=session['user']
        )
        if session.get('just_logged_in'):
            session.pop('just_logged_in')
        return response
                             
    except Exception as e:
        print(f"Application error: {e}")
        return str(e), 500

@app.route('/delete_location', methods=['POST'])
@require_auth
def delete_location():
    try:
        data = request.get_json()
        if not data:
            print("Delete error: No JSON data received")
            return jsonify({'success': False, 'error': 'No data received'})
            
        raw_city = data.get('city')
        name = data.get('name')
        user_id = session['user']['id']
        
        if not raw_city or not name:
            print(f"Delete error: Missing data - city: {raw_city}, name: {name}")
            return jsonify({'success': False, 'error': 'Missing city or name'})
        
        city = raw_city.strip().lower()
        print(f"Attempting to delete - city: '{city}', name: '{name}' for user: {user_id}")
        
        if 'user_locations' not in session or user_id not in session['user_locations']:
            print("No locations found in session for user")
            return jsonify({'success': False, 'error': 'No locations in session'})
            
        user_locations = session['user_locations'][user_id]
        print(f"Current locations in session: {user_locations}")
        
        # Find the location to delete
        location_found = False
        for loc in user_locations:
            if loc['city'] == city and loc['name'] == name:
                location_found = True
                break
        
        if not location_found:
            print(f"Location not found - city: '{city}', name: '{name}'")
            print(f"Available locations: {[(loc['city'], loc['name']) for loc in user_locations]}")
            return jsonify({'success': False, 'error': 'Location not found in session'})
        
        # Remove the location
        original_count = len(user_locations)
        session['user_locations'][user_id] = [
            loc for loc in user_locations
            if not (loc['city'] == city and loc['name'] == name)
        ]
        
        new_count = len(session['user_locations'][user_id])
        session.modified = True
        
        if new_count < original_count:
            print(f"Successfully deleted location. Count changed from {original_count} to {new_count}")
            return jsonify({'success': True, 'message': 'Location deleted successfully'})
        else:
            print(f"Unexpected: No location was removed. Count: {original_count} -> {new_count}")
            return jsonify({'success': False, 'error': 'Location was not removed'})
            
    except Exception as e:
        print(f"Delete location error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'})

@app.route('/edit_location', methods=['POST'])
@require_auth
def edit_location():
    try:
        data = request.get_json()
        city = data.get('city').strip().lower()
        old_name = data.get('old_name')
        new_name = data.get('new_name')
        user_id = session['user']['id']
        
        if 'user_locations' in session and user_id in session['user_locations']:
            for loc in session['user_locations'][user_id]:
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

def send_sms(to, message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=message,
        from_=TWILIO_FROM,
        to=to
    )

if __name__ == '__main__':
    os.makedirs('static/media', exist_ok=True)
    if not API_KEY:
        raise ValueError("API_KEY not found in .env file")
    print("Starting Flask application...")
    app.run(debug=True, port=10000)
