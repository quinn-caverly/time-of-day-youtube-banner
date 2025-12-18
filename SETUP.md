# Quick Setup Guide

## Prerequisites

- Python 3.11 or higher
- A Google Cloud Platform (GCP) project
- A YouTube channel

## Step-by-Step Setup

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd time-of-day-yt-banner
pip install -r requirements.txt
```

### 2. Get YouTube API Credentials

1. **Create/Select GCP Project**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Note your project ID (you'll reference it in GitHub secrets)

2. **Enable YouTube Data API v3**:
   - In your GCP project, go to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"

3. **Create OAuth Credentials**:
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - If prompted, configure the OAuth consent screen:
     - Choose "External" (unless you have a Google Workspace account)
     - Fill in the required fields
     - Add your email to test users
   - Choose "Desktop app" as application type
   - Name it (e.g., "YouTube Banner Updater")
   - Click "Create"
   - Click "Download JSON" and save it as `client_secret.json` in the project root

### 3. Authenticate Locally

Run the script once to authenticate:

```bash
python update_banner.py
```

This will:
- Open a browser window
- Ask you to sign in to Google
- Ask you to authorize the application
- Create a `token.json` file with your credentials

### 4. Prepare Your Banner Images

Add your PNG images to the appropriate folders. You have several options:

**Option 1: Year-round banners (simplest)**
```
images/
└── default/
    ├── 00.png  # Midnight
    ├── 12.png  # Noon
    └── ...     # Add more as needed (00-23.png)
```

**Option 2: Seasonal banners**
```
images/
├── spring/     # March-May
├── summer/     # June-August
├── fall/       # September-November
└── winter/     # December-February
    └── 00.png through 23.png in each
```

**Option 3: Special periods + seasons**
```
images/
├── default/    # Fallback for year-round
├── spring/
├── summer/
├── fall/
├── winter/
├── christmas/  # Dec 20-26 (takes priority)
├── new_year/   # Dec 29 - Jan 2
└── halloween/  # Oct 28 - Nov 1
```

**Priority System:**
The script checks folders in this order:
1. Special periods (christmas, new_year, halloween, etc.) - highest priority
2. Seasons (spring, summer, fall, winter)
3. Default (year-round) - lowest priority, fallback

**Image Requirements**:
- Format: PNG
- Recommended size: 2560x1440 pixels
- Naming: Use 24-hour format (00.png through 23.png)

**Tips:**
- You don't need images for every hour - the script finds the closest available one
- Start with just a `default/` folder if you want one set of banners year-round
- Add seasonal or special period folders as you create more content

### 5. Set Up GitHub Secrets

1. Go to your GitHub repository
2. Navigate to: **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**

Add these secrets:

#### YOUTUBE_CREDENTIALS_JSON
- **Value**: Open the `token.json` file created in step 3
- Copy the entire JSON content
- Paste it as the secret value

#### YOUTUBE_CHANNEL_ID (Optional)
- **Value**: Your YouTube channel ID
- To find it:
  1. Go to [YouTube Studio](https://studio.youtube.com/)
  2. Settings → Channel → Advanced settings
  3. Copy your Channel ID
- If not set, the script will use the authenticated user's channel

### 6. Test the Workflow

1. Commit and push your changes to GitHub
2. Go to **Actions** tab in your repository
3. Select **Update YouTube Banner** workflow
4. Click **Run workflow** to test manually
5. Check the logs to ensure it runs successfully
6. Verify your YouTube channel banner has been updated

### 7. Schedule

The workflow runs automatically every hour. To change the schedule, edit `.github/workflows/update-banner.yml`:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour
```

## Troubleshooting

### "No valid credentials found"
- Ensure `YOUTUBE_CREDENTIALS_JSON` secret is set correctly
- For local testing, ensure `client_secret.json` exists and you've authenticated

### "No banner image found"
- Check that images exist in the correct season folder
- Verify file naming (00.png, 01.png, etc.)
- Ensure at least one PNG exists per season you're using

### Workflow fails
- Check GitHub Actions logs for detailed error messages
- Verify all secrets are set correctly
- Ensure YouTube Data API v3 is enabled in your GCP project

## Next Steps

- Add more banner images for different times/seasons
- Customize season dates in `update_banner.py` if needed
- Adjust the update frequency in the workflow file

