# OAuth Setup Guide

Common OAuth setup issues and how to fix them.

## Error: "Ineligible accounts not added" / "account is not eligible for designation as a test user"

If you see this error when trying to add a test user:

**Solution:** Use the exact email address you're logged into Google Cloud Console with.

1. Check which email you're using in Google Cloud Console:
   - Look at the top-right corner of the Google Cloud Console
   - You'll see your profile picture/icon with your email
   - This is the email you need to add as a test user

2. If you're using a different Google account, you have two options:
   - **Option A:** Sign into Google Cloud Console with the email you want to use (`quinncaverly@gmail.com`)
   - **Option B:** Use the email that's currently logged into Google Cloud Console

3. Add that exact email as a test user:
   - Go to **APIs & Services** → **OAuth consent screen**
   - Scroll to **"Test users"** section
   - Click **"+ ADD USERS"**
   - Enter the email address you're logged in with
   - Click **"Add"**

**Important:** The test user email must match the Google account you'll use to sign in when authenticating. Make sure you're using the same email for both Google Cloud Console and when you run `python update_banner.py`.

---

## Error: "Access blocked: app has not completed Google verification process"

If you see this error, you need to add yourself as a test user:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **APIs & Services** → **OAuth consent screen**
4. Scroll down to **"Test users"** section
5. Click **"+ ADD USERS"**
6. Enter your email address (the one you're signing in with)
7. Click **"Add"**
8. Try authenticating again

**Note:** For personal use, "Testing" mode is fine. If you want to make it available to others or avoid test user limits, you can publish the app (same page → "PUBLISH APP" button).

---

## Error: "redirect_uri_mismatch"

If you get this error, you need to add the redirect URI to your OAuth client:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Go to **APIs & Services** → **Credentials**
4. Click on your OAuth 2.0 Client ID (the "Desktop app" one)
5. Scroll down to **"Authorized redirect URIs"**
6. Click **"+ ADD URI"**
7. Add: `http://localhost:8080/` (with trailing slash)
8. Click **"Save"**
9. Run the script again

---

## Quick Checklist

Before running `python update_banner.py`, make sure:

- [ ] Your email is added to "Test users" in OAuth consent screen
- [ ] The email matches the one you'll use to sign in
- [ ] `http://localhost:8080/` is added to "Authorized redirect URIs" in your OAuth client
- [ ] You have `client_secret.json` in the project root
