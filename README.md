# YouTube Banner Time-of-Day Updater

Automatically update your YouTube channel banner based on the time of day and season using GitHub Actions.

## Features

- 🕐 Updates banner based on current hour (00-23)
- 🌸 Supports seasonal banners (Spring, Summer, Fall, Winter)
- 🎄 Supports special periods (Christmas, New Year, Halloween, etc.)
- 🌍 Default folder for year-round banners (applies regardless of season)
- 🔄 Runs automatically every hour via GitHub Actions
- 📁 Flexible folder structure - use as many or as few zones as you want
- 🔍 Automatically finds nearest available banner if exact hour doesn't exist
- ⚡ Priority system: Special periods → Seasons → Default

## Folder Structure

The banner selection uses a **priority system** to find the right banner. You can use any combination of these folders:

```
images/
├── default/           # Year-round banners (lowest priority, fallback)
│   ├── 00.png
│   ├── 01.png
│   └── ... (00-23.png)
├── spring/           # Spring season (March-May)
│   ├── 00.png
│   └── ...
├── summer/           # Summer season (June-August)
│   └── ...
├── fall/             # Fall season (September-November)
│   └── ...
├── winter/           # Winter season (December-February)
│   └── ...
├── christmas/        # Special period: Dec 20-26 (highest priority)
│   └── ...
├── new_year/         # Special period: Dec 29 - Jan 2
│   └── ...
└── halloween/        # Special period: Oct 28 - Nov 1
    └── ...
```

### How Priority Works

The script checks folders in this order:

1. **Special Periods** (highest priority) - e.g., `christmas/`, `new_year/`, `halloween/`
2. **Seasons** - `spring/`, `summer/`, `fall/`, `winter/`
3. **Default** (lowest priority, fallback) - `default/` for year-round banners

**Examples:**
- If it's December 25th at 3 PM and you have `christmas/15.png`, it will use that
- If it's December 25th but no `christmas/` folder exists, it will try `winter/15.png`
- If no winter banner exists either, it will use `default/15.png`
- If you only have a `default/` folder with 00-23.png, those will be used year-round regardless of season

### Image Specifications

- **Format**: PNG
- **Recommended size**: 2560x1440 pixels
- **Naming**: Use 24-hour format (00.png through 23.png)
- **Flexibility**: You don't need images for every hour - the script finds the closest available one

### Special Periods

The following special periods are built-in (you can customize dates in `update_banner.py`):

- **Christmas**: December 20-26
- **New Year**: December 29 - January 2
- **Halloween**: October 28 - November 1

To add more special periods, edit the `get_special_period()` function in `update_banner.py`.

## Quick Start

For detailed step-by-step setup instructions, see [SETUP.md](SETUP.md).

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd time-of-day-yt-banner
```

### 2. Set Up YouTube API Credentials (GCP Project)

You'll need to create OAuth 2.0 credentials in the Google Cloud Console:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one (note your GCP project ID for reference)
3. Enable the **YouTube Data API v3**:
   - Navigate to "APIs & Services" → "Library"
   - Search for "YouTube Data API v3"
   - Click "Enable"
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
   - If prompted, configure the OAuth consent screen first
   - Choose "Desktop app" as the application type
   - Click "Create"
5. Download the credentials JSON file (this is your `client_secret.json`)

### 3. Authenticate (Local Testing)

For local testing, rename your downloaded credentials file to `client_secret.json`:

```bash
# Place your credentials file in the project root
mv ~/Downloads/client_secret.json .
```

Run the script once locally to authenticate:

```bash
pip install -r requirements.txt
python update_banner.py
```

This will open a browser window for authentication. After successful authentication, a `token.json` file will be created.

### 4. Set Up GitHub Secrets

For GitHub Actions to work, you need to add secrets to your repository:

1. Go to your GitHub repository → Settings → Secrets and variables → Actions
2. Add the following secrets:

   - **YOUTUBE_CREDENTIALS_JSON**: The contents of your `token.json` file (created after running authentication locally)
     - After running `python update_banner.py` locally (step 3), a `token.json` file will be created
     - Open `token.json` and copy the entire JSON content
     - Paste it as the secret value (you can also base64 encode it - the script handles both)
   
   - **YOUTUBE_CHANNEL_ID** (optional): Your YouTube channel ID
     - If not provided, the script will use the authenticated user's channel
     - Find it in your YouTube Studio → Settings → Channel → Advanced settings

### 5. Add Your Banner Images

Add your PNG banner images to the appropriate folders:

**Option 1: Year-round banners only (simplest)**
- Place images in `images/default/` (00.png through 23.png)
- These will be used regardless of season or special periods

**Option 2: Seasonal banners**
- Place images in `images/{season}/` folders (spring, summer, fall, winter)
- Each season folder can contain 00.png through 23.png

**Option 3: Special periods + seasons**
- Add special period folders like `images/christmas/` for holiday-specific banners
- These take priority over seasonal banners

**Option 4: Mix and match**
- Use any combination of the above
- The script will automatically choose based on priority: special periods → seasons → default

**Tips:**
- You don't need images for every hour - the script finds the closest available one
- Start with a few images and add more over time
- You can have just a `default/` folder if you want one set of banners year-round

### 6. Test the Workflow

You can manually trigger the workflow:

1. Go to your repository → Actions
2. Select "Update YouTube Banner"
3. Click "Run workflow"

## Configuration

### Changing the Update Frequency

Edit `.github/workflows/update-banner.yml` and modify the cron schedule:

```yaml
schedule:
  - cron: '0 * * * *'  # Every hour (minute 0 of every hour)
  # Other examples:
  # - cron: '0 */2 * * *'  # Every 2 hours
  # - cron: '0 9,12,18 * * *'  # At 9 AM, 12 PM, and 6 PM
```

### Custom Season Dates

To customize season dates, edit the `get_season()` function in `update_banner.py`.

### Custom Image Directory

To use a different directory for images, modify the `images_dir` parameter in the script.

## How It Works

1. **GitHub Actions** triggers the workflow on schedule (every hour by default)
2. The **Python script** (`update_banner.py`) runs:
   - Determines current season and hour
   - Finds the appropriate banner image
   - Authenticates with YouTube API using stored credentials
   - Uploads the banner to your channel

## Troubleshooting

### "No valid credentials found"

- Make sure you've set the `YOUTUBE_CREDENTIALS_JSON` secret in GitHub
- For local testing, ensure `client_secret.json` exists and you've run the script at least once

### "No banner image found"

- Check that you have images in at least one folder: `default/`, a season folder, or a special period folder
- Verify at least one PNG file exists in the checked folders
- Remember the priority: special periods → seasons → default
- If you want year-round banners, just use the `default/` folder

### Banner not updating

- Check the GitHub Actions logs for errors
- Verify your YouTube API credentials are valid
- Ensure the YouTube Data API v3 is enabled in your Google Cloud project

## Contributing

Feel free to submit issues or pull requests if you'd like to improve this project!

## License

MIT License - feel free to use this for your own YouTube channel!

