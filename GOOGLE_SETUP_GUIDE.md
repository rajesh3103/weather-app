# 🔧 Google OAuth Setup Guide

## Fix for "Error 400: redirect_uri_mismatch"

Follow these **exact steps** to configure Google OAuth correctly:

### Step 1: Go to Google Cloud Console
1. Open [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account

### Step 2: Create or Select Project
1. Click the project dropdown at the top
2. Click "New Project" or select an existing project
3. If creating new: Enter project name and click "Create"

### Step 3: Enable Required APIs
1. Go to **"APIs & Services"** > **"Library"**
2. Search for **"Google+ API"**
3. Click on it and click **"Enable"**

### Step 4: Create OAuth 2.0 Credentials
1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"OAuth client ID"**
3. If prompted, configure the OAuth consent screen first:
   - Choose "External" user type
   - Fill in required fields (App name, User support email, Developer contact)
   - Add your email to test users
   - Save and continue through all steps

### Step 5: Configure OAuth Client ID
1. Application type: **"Web application"**
2. Name: `Weather App` (or any name you prefer)

### Step 6: Add Authorized Origins (CRITICAL)
In the **"Authorized JavaScript origins"** section, add:
```
http://localhost:10000
```

### Step 7: Add Authorized Redirect URIs (CRITICAL)
In the **"Authorized redirect URIs"** section, add:
```
http://localhost:10000/auth/google/callback
```

⚠️ **Important**: This MUST be the exact callback URL including the `/auth/google/callback` path

### Step 8: Save and Copy Client ID
1. Click **"Create"**
2. Copy the **Client ID** (it looks like: `123456789-abcdef.apps.googleusercontent.com`)

### Step 9: Update Your .env File
Add your Client ID to the `.env` file:
```env
GOOGLE_CLIENT_ID=your_actual_client_id_here.apps.googleusercontent.com
```

### Step 10: Test the Configuration
1. Restart your Flask app: `python weather_app.py`
2. Go to `http://localhost:10000/auth`
3. Click "Continue with Google"
4. The Google sign-in should work without errors

## Common Issues and Solutions

### Issue 1: "This app isn't verified"
- **Solution**: Click "Advanced" > "Go to Weather App (unsafe)"
- This is normal for development apps

### Issue 2: Still getting redirect_uri_mismatch
- **Solution**: Double-check that you added `http://localhost:10000` (no trailing slash)
- Make sure you're running the app on port 10000
- Clear browser cache and try again

### Issue 3: "Access blocked" 
- **Solution**: Make sure your email is added to test users in OAuth consent screen

## Production Deployment
When deploying to production, add your domain:
- Authorized origins: `https://yourdomain.com`
- Authorized redirect URIs: `https://yourdomain.com`

## 📱 Phone Authentication Note
If you're getting Firebase errors for phone authentication:
1. The app will automatically fall back to server-side verification
2. Check the console output for verification codes in demo mode
3. To set up proper SMS sending, configure Twilio or AWS SNS

---

**Need help?** Make sure you follow each step exactly as written above. The redirect URI configuration is the most common cause of issues. 