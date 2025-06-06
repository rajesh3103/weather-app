# 🌦️ Weather App

A modern, responsive weather application that provides real-time weather information with beautiful animated backgrounds and a sleek user interface. The app features dynamic GIF backgrounds that change based on weather conditions, location management, theme switching, and **user authentication with Google sign-in and phone number verification**.

## ✨ Features

### 🔐 Authentication
- **Google Sign-In** - Secure authentication using Google OAuth
- **Phone Number Authentication** - SMS-based verification system
- **User Sessions** - Persistent login sessions
- **Personal Data** - User-specific location storage
- **Secure Logout** - Safe session termination

### 🎨 User Interface
- **Animated Weather Backgrounds** - Dynamic GIF backgrounds that change based on weather conditions
- **Dark/Light Theme Toggle** - Switch between light and dark modes with persistence
- **Responsive Design** - Optimized for desktop and mobile devices
- **Smooth Transitions** - Beautiful fade-in animations and loading effects
- **Modern UI** - Clean, professional design with enhanced visual effects
- **User Profile Display** - Shows authenticated user information

### 🌍 Location Features
- **Current Location Detection** - Automatic weather detection using GPS/geolocation
- **Personal Saved Locations** - Add, manage, and delete favorite locations per user
- **Custom Location Names** - Set display names for saved locations
- **Quick Access** - One-click weather checking for saved locations

### 🌡️ Weather Information
- **Current Temperature** - Real-time temperature in Celsius
- **Weather Conditions** - Detailed weather descriptions
- **Wind Information** - Wind speed in km/h
- **Humidity Levels** - Current humidity percentage
- **Feels Like Temperature** - Apparent temperature readings
- **Local Time Display** - Shows time in the location's timezone

### ⚡ Interactive Features
- **Search Functionality** - Search weather by city name
- **Location Management** - Add/remove locations with modal dialogs
- **Real-time Updates** - Live time display with timezone support
- **Error Handling** - User-friendly error messages
- **Preloading System** - Smart GIF preloading with JPG fallbacks

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Backend**: Python Flask
- **Authentication**: Google OAuth 2.0, Firebase Phone Auth
- **Templating**: Jinja2
- **API**: Weather API integration
- **Storage**: Session-based user data storage
- **Location Services**: Browser Geolocation API

## 📁 Project Structure

```
weather-app/
├── templates/
│   ├── index.html          # Main application template
│   └── auth.html           # Authentication page
├── static/
│   └── media/              # Animated weather backgrounds
│       ├── default.gif     # Animated backgrounds
│       ├── sunny.gif
│       ├── cloudy.gif
│       ├── rainy.gif
│       ├── stormy.gif
│       ├── snowy.gif
│       ├── default.jpg     # Static fallbacks
│       ├── sunny.jpg
│       ├── cloudy.jpg
│       ├── rainy.jpg
│       ├── stormy.jpg
│       └── snowy.jpg
├── weather_app.py          # Main Flask application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- Weather API key (WeatherAPI recommended)
- Google Cloud Console account (for Google authentication)
- Firebase account (for phone authentication)
- Modern web browser

### Authentication Setup

#### 1. Google Authentication Setup
1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Create a new project** or select an existing one
3. **Enable the Google+ API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google+ API" and enable it
4. **Create OAuth 2.0 credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Web application"
   - Add your domain to "Authorized JavaScript origins" (e.g., `http://localhost:10000`)
   - Add redirect URI (e.g., `http://localhost:10000http://localhost:10000/auth/google`)
5. **Copy the Client ID** for your `.env` file

#### 2. Firebase Phone Authentication Setup
1. **Go to [Firebase Console](https://console.firebase.google.com/)**
2. **Create a new project** or select existing
3. **Enable Authentication**:
   - Go to "Authentication" > "Sign-in method"
   - Enable "Phone" authentication
4. **Get configuration**:
   - Go to "Project settings" > "General"
   - Scroll down to "Your apps" and copy the config
5. **Add your domain** to authorized domains in Authentication settings

#### 3. Environment Variables Setup
Create a `.env` file in your project root with:

```env
# Weather API Configuration
WEATHER_API_KEY=your_weather_api_key_here

# Google Authentication Configuration
GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com

# Firebase Configuration (for phone authentication)
FIREBASE_API_KEY=your_firebase_api_key_here
FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
FIREBASE_PROJECT_ID=your_firebase_project_id_here
```

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd weather-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Fill in your actual API keys and configuration values

4. **Add animated weather backgrounds**
   - Place weather-themed animated GIFs in `static/media/`
   - Name them according to weather types (e.g., `sunny.gif`, `rainy.gif`, `cloudy.gif`)
   - JPG fallbacks are supported (e.g., `sunny.jpg`, `rainy.jpg`)
   - The app will automatically use GIFs if available, fallback to JPGs

5. **Run the application**
   ```bash
   python weather_app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:10000`
   - You'll be redirected to the authentication page

## 📱 Usage

### Authentication
1. **First Visit**: You'll be redirected to the authentication page
2. **Google Sign-In**: Click "Continue with Google" for instant authentication
3. **Phone Authentication**: 
   - Click "Continue with Phone Number"
   - Enter your phone number (with country code, e.g., +1234567890)
   - Enter the 6-digit verification code sent via SMS
4. **Session Management**: Stay logged in across browser sessions
5. **Logout**: Click the logout button in the user menu

### Getting Weather Information
1. **Search by City**: Enter a city name in the search box and click "Get Weather"
2. **Use Current Location**: Click "📍 Current Location" in the sidebar
3. **Saved Locations**: Click on any saved location for instant weather

### Managing Locations
1. **Add Location**: Click "+ Add Location" button
2. **Custom Names**: Set display names for easy identification
3. **Delete Locations**: Hover over a location and click the × button
4. **Personal Storage**: Each user has their own saved locations

### Theme Switching
- Click the 🌞/🌜 icon in the top-right corner to toggle themes
- Theme preference is automatically saved

## 🔧 Configuration

### Weather API Setup
The app requires a weather API key. Supported APIs:
- [WeatherAPI](https://weatherapi.com/) (Recommended)
- OpenWeatherMap
- AccuWeather

### Authentication Security
- **Session Management**: Secure server-side sessions
- **Token Verification**: Google tokens are verified server-side
- **Rate Limiting**: Phone verification has attempt limits
- **Expiration**: Verification codes expire after 5 minutes

### Animated Background Images
Add weather-themed animated GIFs to `static/media/` with these naming conventions:

**Primary (Animated GIFs):**
- `default.gif` - Default animated background
- `sunny.gif` - Clear/sunny weather animation
- `cloudy.gif` - Cloudy conditions animation
- `rainy.gif` - Rain/drizzle animation
- `stormy.gif` - Thunderstorms animation
- `snowy.gif` - Snow conditions animation

**Fallback (Static Images):**
- `default.jpg` - Static fallback background
- `sunny.jpg` - Static sunny weather
- `cloudy.jpg` - Static cloudy conditions
- `rainy.jpg` - Static rain/drizzle
- `stormy.jpg` - Static thunderstorms
- `snowy.jpg` - Static snow conditions

## 🔐 Security Features

- **OAuth 2.0**: Industry-standard Google authentication
- **Phone Verification**: SMS-based two-factor authentication
- **Session Security**: Secure session management
- **CSRF Protection**: Built-in Flask security
- **Token Validation**: Server-side token verification
- **Rate Limiting**: Prevents authentication abuse

## 🌐 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📊 Features in Detail

### Authentication System
- Multiple authentication methods (Google, Phone)
- Persistent user sessions
- User profile display
- Secure logout functionality

### Theme System
- Automatic theme detection based on system preferences
- Manual toggle with instant switching
- Persistent storage using localStorage

### Location Management
- Geolocation API integration for current position
- CRUD operations for saved locations per user
- Temperature caching for quick access
- User-specific data isolation

### Weather Display
- Real-time weather data
- Timezone-aware time display
- Responsive weather cards
- Error handling for invalid locations

## 🔮 Future Enhancements

- [ ] Weather forecasts (5-day, hourly)
- [ ] Weather alerts and notifications
- [ ] Weather maps integration
- [ ] Offline mode support
- [ ] Mobile app version
- [ ] Weather widgets
- [ ] Social sharing features
- [ ] Database storage for users and locations
- [ ] Email notifications
- [ ] Weather history tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by **Rajesh** - A modern weather application with secure authentication for everyday use.

## 🐛 Known Issues

- Background images require manual addition
- Some weather conditions may not have specific backgrounds
- Geolocation requires HTTPS in production
- Phone authentication requires SMS service setup for production use

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

*Enjoy checking the weather with style and security! 🌤️🔐*