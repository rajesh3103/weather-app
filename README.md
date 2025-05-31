# 🌦️ Weather App

A modern, responsive weather application that provides real-time weather information with beautiful animated backgrounds and a sleek user interface. The app features dynamic GIF backgrounds that change based on weather conditions, location management, and theme switching.

## ✨ Features

### 🎨 User Interface
- **Animated Weather Backgrounds** - Dynamic GIF backgrounds that change based on weather conditions
- **Dark/Light Theme Toggle** - Switch between light and dark modes with persistence
- **Responsive Design** - Optimized for desktop and mobile devices
- **Smooth Transitions** - Beautiful fade-in animations and loading effects
- **Modern UI** - Clean, professional design with enhanced visual effects

### 🌍 Location Features
- **Current Location Detection** - Automatic weather detection using GPS/geolocation
- **Saved Locations** - Add, manage, and delete favorite locations
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
- **Backend**: Python (Flask/Django - based on template syntax)
- **Templating**: Jinja2
- **API**: Weather API integration
- **Storage**: Local storage for theme preferences
- **Location Services**: Browser Geolocation API

## 📁 Project Structure

```
weather-app/
├── templates/
│   └── index.html          # Main application template
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
├── app.py                  # Main application file (backend)
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- Weather API key (OpenWeatherMap, WeatherAPI, etc.)
- Modern web browser

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
   ```bash
   export WEATHER_API_KEY="your_api_key_here"
   ```

4. **Add animated weather backgrounds**
   - Place weather-themed animated GIFs in `static/media/`
   - Name them according to weather types (e.g., `sunny.gif`, `rainy.gif`, `cloudy.gif`)
   - JPG fallbacks are supported (e.g., `sunny.jpg`, `rainy.jpg`)
   - The app will automatically use GIFs if available, fallback to JPGs

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   - Navigate to `http://localhost:5000`

## 📱 Usage

### Getting Weather Information
1. **Search by City**: Enter a city name in the search box and click "Get Weather"
2. **Use Current Location**: Click "📍 Current Location" in the sidebar
3. **Saved Locations**: Click on any saved location for instant weather

### Managing Locations
1. **Add Location**: Click "+ Add Location" button
2. **Custom Names**: Set display names for easy identification
3. **Delete Locations**: Hover over a location and click the × button

### Theme Switching
- Click the 🌞/🌜 icon in the top-right corner to toggle themes
- Theme preference is automatically saved

## 🔧 Configuration

### Weather API Setup
The app requires a weather API key. Supported APIs:
- OpenWeatherMap
- WeatherAPI
- AccuWeather

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

**Features:**
- Automatic GIF detection with JPG fallback
- Smooth fade-in animations
- Weather-specific visual effects (blur, brightness, contrast)
- Preloading system for better performance

### Customization
- Modify CSS variables in the `:root` selectors for theme colors
- Adjust layout breakpoints for responsive design
- Customize weather condition mappings in the backend

## 🌐 Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## 📊 Features in Detail

### Theme System
- Automatic theme detection based on system preferences
- Manual toggle with instant switching
- Persistent storage using localStorage

### Location Management
- Geolocation API integration for current position
- CRUD operations for saved locations
- Temperature caching for quick access

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

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created by **Rajesh** - A modern weather application for everyday use.

## 🐛 Known Issues

- Background images require manual addition
- Some weather conditions may not have specific backgrounds
- Geolocation requires HTTPS in production

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

*Enjoy checking the weather with style! 🌤️*