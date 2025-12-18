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
- 🔐 Secure credential management with automatic token refresh

## Quick Setup Summary

1. **GCP Setup** (5 min): Create project, enable YouTube API, create OAuth client → download `client_secret.json`
2. **Local Auth** (1 min): Run `python update_banner.py` once → creates `token.json`
3. **GitHub Secret** (1 min): Copy `token.json` content → paste into GitHub Secret `YOUTUBE_CREDENTIALS_JSON`
4. **Add Images**: Put banner PNGs in `images/default/` or season folders
5. **Done!** Workflow runs automatically every hour

**See [SETUP.md](SETUP.md) for detailed instructions.**

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

## Setup Instructions

For detailed step-by-step setup instructions, see [SETUP.md](SETUP.md).

### Quick Overview:

1. **GCP Project Setup**: Create project, enable YouTube Data API v3, create OAuth 2.0 Client ID
2. **One-Time Local Auth**: Run `python update_banner.py` to generate `token.json`
3. **GitHub Secret**: Copy `token.json` content → GitHub Secret `YOUTUBE_CREDENTIALS_JSON`
4. **Add Banner Images**: Place PNG files in `images/` folders
5. **Test**: Manually trigger workflow or wait for scheduled run

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
   - Finds the appropriate banner image (using priority system)
   - Authenticates with YouTube API using stored credentials
   - Automatically refreshes token if needed
   - Uploads the banner to your channel

## Credentials & Security

- **One-time setup**: You authenticate locally once to get a refresh token
- **GitHub Secrets**: The refresh token is stored securely as a GitHub Secret
- **Auto-refresh**: The script automatically refreshes expired access tokens
- **No expiration**: Refresh tokens don't expire as long as they're used regularly (workflow runs hourly)

## Troubleshooting

### "Access blocked" / "access_denied" Error

If you see "Youtube Banner Changer has not completed the Google verification process":

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → Your project
2. **APIs & Services** → **OAuth consent screen**
3. Scroll to **"Test users"** section
4. Click **"+ ADD USERS"**
5. Add your email address (the one you're signing in with)
6. Click **"Add"**
7. Try running the script again

### "redirect_uri_mismatch" Error

If you see this error when running `python update_banner.py`:

1. Go to [Google Cloud Console](https://console.cloud.google.com/) → Your project
2. **APIs & Services** → **Credentials**
3. Click on your OAuth 2.0 Client ID
4. Under **"Authorized redirect URIs"**, add: `http://localhost:8080/`
5. Click **"Save"**
6. Run the script again

See [OAUTH_SETUP.md](OAUTH_SETUP.md) for details.

### "No valid credentials found"

- Make sure you've set the `YOUTUBE_CREDENTIALS_JSON` secret in GitHub
- Verify the secret contains the full JSON from your `token.json` file
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
- Check that your OAuth app has your email in the test users list

### Token expired / Authentication errors

- The script should auto-refresh tokens, but if you get errors:
  - Re-run the local auth step: `python update_banner.py`
  - Copy the new `token.json` content to the GitHub Secret
  - Make sure your OAuth app is still in "Testing" mode or published

## Contributing

Feel free to submit issues or pull requests if you'd like to improve this project!

## License

MIT License - feel free to use this for your own YouTube channel!
