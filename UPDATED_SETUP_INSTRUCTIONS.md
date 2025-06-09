# 🔧 Updated Authentication Setup Guide

## 🚨 IMPORTANT: New Google OAuth Configuration Required

The Google authentication has been updated to use a more reliable redirect-based flow. You **MUST** update your Google Cloud Console settings.

## 📋 Step-by-Step Setup

### 1. Update Google Cloud Console (CRITICAL)

1. **Go to [Google Cloud Console](https://console.cloud.google.com/)**
2. **Navigate to APIs & Services > Credentials**
3. **Click on your existing OAuth client ID**
4. **Update "Authorized redirect URIs" to include:**
   ```
   http://localhost:10000/auth/google/callback
   ```
   ⚠️ **CRITICAL**: Use this EXACT URL with `/auth/google/callback` at the end

5. **Keep "Authorized JavaScript origins" as:**
   ```
   http://localhost:10000
   ```

6. **Click "Save"**

### 2. Update Your .env File

```env
# Weather API (Required)
WEATHER_API_KEY=your_weather_api_key_here

# Google Authentication
GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com

# Firebase (Optional - for phone auth)
FIREBASE_API_KEY=your_firebase_api_key_here
FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
FIREBASE_PROJECT_ID=your_firebase_project_id_here
```

### 3. Test Your Setup

1. **Restart your app**: `python weather_app.py`
2. **Go to**: `http://localhost:10000/auth`
3. **Test Google Sign-In**:
   - Click "Continue with Google"
   - Should redirect to Google sign-in page
   - After signing in, should redirect back to your weather app
   - You should see the main dashboard with your user info

4. **Test Phone Authentication**:
   - Click "Continue with Phone Number"
   - Enter phone number with country code (e.g., `+1234567890`)
   - Click "Send Verification Code"
   - **Demo Mode**: Check your server console/terminal for the 6-digit code
   - Enter the code and click "Verify Code"

## 🔍 What's New

### ✅ **Fixed Issues:**
- **Google OAuth Error**: No more `hereredirect_uri_mismatch` errors
- **Firebase Error**: Proper fallback to server-side phone verification
- **Improved Error Handling**: Clear error messages for all issues
- **Better User Experience**: Smooth redirects and loading states

### 🎯 **How It Works Now:**

**Google Authentication:**
- Uses direct OAuth redirect (most reliable method)
- No popups or complex JavaScript
- Standard OAuth 2.0 flow

**Phone Authentication:**
- Tries Firebase first (if configured)
- Falls back to server-side verification (demo mode)
- Shows clear instructions for demo mode

## 🧪 Expected Behavior

### Google Sign-In Success Flow:
1. Click "Continue with Google" → Button shows "🔄 Redirecting to Google..."
2. Redirected to Google sign-in page
3. Sign in with your Google account
4. Redirected back to weather app
5. See main dashboard with user profile

### Phone Auth Success Flow:
1. Click "Continue with Phone Number" → Form appears
2. Enter phone number → Click "Send Verification Code"
3. Button shows "Sending..." → Success message appears
4. **Demo Mode**: Check terminal for code like: `📱 Verification code for +1234567890: 123456`
5. Enter code → Click "Verify Code" → Redirected to dashboard

## 🐛 Troubleshooting

### Google Sign-In Issues:
- **"redirect_uri_mismatch"**: Double-check the redirect URI is exactly `http://localhost:10000/auth/google/callback`
- **"This app isn't verified"**: Click "Advanced" → "Go to Weather App (unsafe)" (normal for development)
- **"Access blocked"**: Add your email to test users in OAuth consent screen

### Phone Auth Issues:
- **Firebase errors**: App automatically falls back to demo mode
- **"Invalid phone number"**: Use format `+1234567890` with country code
- **No SMS received**: In demo mode, codes appear in server console

### General Issues:
- **Clear browser cache** if you have persistent issues
- **Restart the Flask app** after changing .env
- **Check server console** for detailed error messages

## 📱 Production Notes

For production deployment:
- Add your production domain to Google Cloud Console
- Set up proper SMS service (Twilio, AWS SNS) for phone auth
- Use HTTPS for all authentication flows
- Configure proper Firebase settings for phone auth

## ✅ Quick Test Checklist

- [ ] Google Client ID in .env file
- [ ] Updated redirect URI in Google Console to `/auth/google/callback`
- [ ] App restarts successfully
- [ ] `/auth` page loads without errors
- [ ] Google sign-in redirects properly
- [ ] Phone auth shows demo mode instructions
- [ ] Both authentication methods create user sessions

---

**🎉 Once both authentication methods work, your weather app is ready to use with secure user accounts!** 