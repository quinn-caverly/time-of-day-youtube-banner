#!/usr/bin/env python3
"""
YouTube Banner Updater
Updates YouTube channel banner based on time of day and season.
"""

import os
import sys
from datetime import datetime
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import json
import base64


# YouTube API scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

# Image dimensions for YouTube banner (recommended: 2560x1440)
BANNER_DIMENSIONS = (2560, 1440)


def get_season(month: int) -> str:
    """
    Determine season based on month.
    Northern hemisphere seasons:
    - Spring: March (3), April (4), May (5)
    - Summer: June (6), July (7), August (8)
    - Fall: September (9), October (10), November (11)
    - Winter: December (12), January (1), February (2)
    """
    if month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    elif month in [9, 10, 11]:
        return 'fall'
    else:  # 12, 1, 2
        return 'winter'


def get_special_period(month: int, day: int) -> str:
    """
    Check if current date falls within a special period.
    Returns the special period name if found, None otherwise.
    
    You can customize these dates as needed.
    Examples:
    - Christmas: December 20-26
    - New Year: December 29 - January 2
    - Halloween: October 28 - November 1
    """
    # Christmas period (Dec 20 - Dec 26)
    if month == 12 and 20 <= day <= 26:
        return 'christmas'
    
    # New Year period (Dec 29 - Jan 2)
    if (month == 12 and day >= 29) or (month == 1 and day <= 2):
        return 'new_year'
    
    # Halloween period (Oct 28 - Nov 1)
    if (month == 10 and day >= 28) or (month == 11 and day <= 1):
        return 'halloween'
    
    # Add more special periods here as needed
    # Example for Valentine's Day:
    # if month == 2 and 10 <= day <= 14:
    #     return 'valentines'
    
    return None


def get_banner_path(zone: str, hour: int, images_dir: Path = Path('images')) -> Path:
    """
    Get the path to the banner image based on zone and hour.
    
    Format: images/{zone}/{hour:02d}.png
    Example: images/spring/12.png for spring at noon
    Example: images/christmas/12.png for Christmas at noon
    Example: images/default/12.png for default/year-round at noon
    """
    banner_path = images_dir / zone / f'{hour:02d}.png'
    return banner_path


def find_banner_in_zone(zone: str, hour: int, images_dir: Path) -> Path:
    """
    Find an available banner image in a specific zone for the given hour.
    Tries the exact hour first, then looks for the closest available hour.
    Returns the path if found, None otherwise.
    """
    zone_dir = images_dir / zone
    if not zone_dir.exists():
        return None
    
    # Try exact hour first
    banner_path = get_banner_path(zone, hour, images_dir)
    if banner_path.exists():
        return banner_path
    
    # Try adjacent hours (±1, ±2, etc.)
    for offset in range(1, 24):
        for direction in [-1, 1]:
            try_hour = (hour + direction * offset) % 24
            try_path = get_banner_path(zone, try_hour, images_dir)
            if try_path.exists():
                return try_path
    
    return None


def find_available_banner(special_period: str, season: str, hour: int, images_dir: Path = Path('images')) -> Path:
    """
    Find an available banner image using a priority system:
    1. Special periods (e.g., christmas, new_year, halloween)
    2. Season-specific folders (spring, summer, fall, winter)
    3. Default folder (year-round, applies regardless of season)
    
    Tries the exact hour first, then looks for the closest available hour in each zone.
    """
    # Priority 1: Check special periods first
    if special_period:
        banner_path = find_banner_in_zone(special_period, hour, images_dir)
        if banner_path:x
        print(f"No banner found in special period '{special_period}', trying season...")
    
    # Priority 2: Check season-specific folder
    banner_path = find_banner_in_zone(season, hour, images_dir)
    if banner_path:
        return banner_path
    print(f"No banner found in season '{season}', trying default...")
    
    # Priority 3: Check default folder (year-round)
    banner_path = find_banner_in_zone('default', hour, images_dir)
    if banner_path:
        return banner_path
    
    # If no banner found in any zone, raise error
    zones_checked = []
    if special_period:
        zones_checked.append(f"special/{special_period}")
    zones_checked.extend([f"season/{season}", "default"])
    
    raise FileNotFoundError(
        f"No banner image found for hour {hour:02d} in any zone. "
        f"Checked: {', '.join(zones_checked)}. "
        f"Please add images to at least one of these folders."
    )


def get_authenticated_service():
    """
    Get authenticated YouTube API service.
    Uses credentials from environment variable or file.
    """
    creds = None
    
    # Try to get credentials from environment variable (for GitHub Actions)
    creds_json = os.environ.get('YOUTUBE_CREDENTIALS_JSON')
    if creds_json:
        try:
            creds_data = json.loads(creds_json)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
            
            # Refresh if needed
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
        except json.JSONDecodeError:
            # Try as base64 encoded
            try:
                creds_data = json.loads(base64.b64decode(creds_json).decode())
                creds = Credentials.from_authorized_user_info(creds_data, SCOPES)
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
            except Exception as e:
                print(f"Error parsing credentials from environment: {e}")
                sys.exit(1)
    
    # Fallback to client_secret.json (for local development)
    if not creds or not creds.valid:
        if os.path.exists('client_secret.json'):
            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES)
                creds = flow.run_local_server(port=0)
            elif creds.expired and creds.refresh_token:
                creds.refresh(Request())
            
            # Save credentials for future use
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        else:
            # Try token.json if it exists
            if os.path.exists('token.json'):
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
                if creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
    
    if not creds or not creds.valid:
        raise Exception(
            "No valid credentials found. Please set YOUTUBE_CREDENTIALS_JSON "
            "environment variable or provide client_secret.json"
        )
    
    return build('youtube', 'v3', credentials=creds)


def upload_banner(youtube_service, banner_path: Path):
    """
    Upload banner image to YouTube channel.
    Uses channelBanners().insert() to upload, then updates channel brandingSettings.
    """
    # Step 1: Upload the banner image
    print(f"Uploading banner image: {banner_path}")
    upload_request = youtube_service.channelBanners().insert(
        media_body=MediaFileUpload(
            str(banner_path),
            mimetype='image/png',
            resumable=True
        ),
        body={}
    )
    upload_response = upload_request.execute()
    banner_url = upload_response['url']
    print(f"Banner uploaded successfully. URL: {banner_url}")
    
    # Step 2: Get channel ID
    channel_id = os.environ.get('YOUTUBE_CHANNEL_ID')
    if not channel_id:
        # Try to get channel ID from authenticated user
        request = youtube_service.channels().list(part='id', mine=True)
        response = request.execute()
        if response['items']:
            channel_id = response['items'][0]['id']
        else:
            raise Exception("Could not determine channel ID. Set YOUTUBE_CHANNEL_ID environment variable.")
    
    # Step 3: Update channel brandingSettings with the new banner URL
    print(f"Updating channel banner (Channel ID: {channel_id})...")
    youtube_service.channels().update(
        part='brandingSettings',
        body={
            'id': channel_id,
            'brandingSettings': {
                'image': {
                    'bannerExternalUrl': banner_url
                }
            }
        }
    ).execute()
    
    print(f"Successfully updated banner: {banner_path}")


def main():
    """
    Main function to update YouTube banner.
    """
    # Get current time
    now = datetime.now()
    special_period = get_special_period(now.month, now.day)
    season = get_season(now.month)
    hour = now.hour
    
    print(f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    if special_period:
        print(f"Special period: {special_period}")
    print(f"Season: {season}, Hour: {hour:02d}")
    
    # Find banner image
    images_dir = Path('images')
    try:
        banner_path = find_available_banner(special_period, season, hour, images_dir)
        print(f"Using banner: {banner_path}")
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Authenticate and upload
    try:
        youtube_service = get_authenticated_service()
        upload_banner(youtube_service, banner_path)
        print("Banner update completed successfully!")
    except Exception as e:
        print(f"Error updating banner: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

