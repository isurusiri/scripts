import requests
import pandas as pd
import time
import os
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# ---- CONFIG ----
ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")
REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")
CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
OUTPUT_FILE = "strava_activities_last_2_years.csv"
SUMMARY_FILE = "strava_summary_by_sport.csv"
DAYS_BACK = 730  # Two years
PER_PAGE = 200
# ----------------

def refresh_access_token():
    """Refresh the access token using the refresh token"""
    if not all([REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET]):
        raise ValueError("Missing refresh token, client ID, or client secret for token refresh")
    
    print("Refreshing access token...")
    
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": REFRESH_TOKEN,
            "grant_type": "refresh_token"
        }
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to refresh token: {response.status_code} - {response.text}")
    
    data = response.json()
    
    # Update environment variables
    os.environ["STRAVA_ACCESS_TOKEN"] = data["access_token"]
    os.environ["STRAVA_REFRESH_TOKEN"] = data["refresh_token"]
    os.environ["STRAVA_TOKEN_EXPIRES_AT"] = str(data["expires_at"])
    
    # Update .env file
    env_content = f"""STRAVA_CLIENT_ID={CLIENT_ID}
STRAVA_CLIENT_SECRET={CLIENT_SECRET}
STRAVA_ACCESS_TOKEN={data['access_token']}
STRAVA_REFRESH_TOKEN={data['refresh_token']}
STRAVA_TOKEN_EXPIRES_AT={data['expires_at']}
"""
    with open(".env", "w") as f:
        f.write(env_content)
    
    print("Token refreshed successfully")
    return data["access_token"]

def make_api_request(url, headers, params=None, max_retries=3):
    """Make API request with retry logic and rate limiting"""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 60))
                print(f"Rate limited. Waiting {retry_after} seconds...")
                time.sleep(retry_after)
                continue
            
            # Handle token expiration
            if response.status_code == 401:
                if attempt == 0:  # Only try to refresh once
                    try:
                        new_token = refresh_access_token()
                        headers["Authorization"] = f"Bearer {new_token}"
                        continue
                    except Exception as e:
                        print(f"Failed to refresh token: {e}")
                        raise
            
            if response.status_code == 200:
                return response
            
            # For other errors, wait and retry
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Request failed (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
                time.sleep(wait_time)
                continue
            
            # Final attempt failed
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise Exception(f"API request failed after {max_retries} attempts: {e}")
            wait_time = 2 ** attempt
            print(f"Network error (attempt {attempt + 1}/{max_retries}). Retrying in {wait_time}s...")
            time.sleep(wait_time)
    
    raise Exception("Unexpected error in API request")

def main():
    if not ACCESS_TOKEN:
        raise ValueError("Missing STRAVA_ACCESS_TOKEN environment variable")

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    url = "https://www.strava.com/api/v3/athlete/activities"
    after = int((datetime.now() - timedelta(days=DAYS_BACK)).timestamp())
    page = 1
    all_activities = []

    print("Fetching Strava activities for the past 2 years...")
    print(f"Fetching activities after: {datetime.fromtimestamp(after).strftime('%Y-%m-%d')}")
    print()

    try:
        while True:
            params = {
                "after": after,
                "page": page,
                "per_page": PER_PAGE
            }

            response = make_api_request(url, headers, params)
            data = response.json()

            if not data:
                print(f"No more activities found. Total pages: {page - 1}")
                break

            for activity in data:
                all_activities.append({
                    "id": activity["id"],
                    "name": activity["name"],
                    "sport_type": activity.get("sport_type", activity["type"]),
                    "start_date": activity["start_date_local"],
                    "distance_km": round(activity.get("distance", 0) / 1000, 2),
                    "moving_time_min": round(activity.get("moving_time", 0) / 60, 1),
                    "elapsed_time_min": round(activity.get("elapsed_time", 0) / 60, 1),
                    "average_speed_kmph": round(activity.get("average_speed", 0) * 3.6, 2),
                    "max_speed_kmph": round(activity.get("max_speed", 0) * 3.6, 2),
                    "total_elevation_gain_m": activity.get("total_elevation_gain", ""),
                    "average_heartrate": activity.get("average_heartrate", ""),
                    "max_heartrate": activity.get("max_heartrate", ""),
                    "calories": activity.get("calories", ""),
                    "trainer": activity.get("trainer", 0),
                    "commute": activity.get("commute", 0),
                })

            print(f"Fetched page {page} with {len(data)} activities.")
            page += 1
            time.sleep(1)  # Avoid hitting rate limits

        # Convert to DataFrame
        if not all_activities:
            print("No activities found for the specified time period.")
            return

        df = pd.DataFrame(all_activities)
        df.fillna("", inplace=True)
        df.to_csv(OUTPUT_FILE, index=False)

        # Summary by sport type
        summary_df = df.groupby("sport_type").agg({
            "distance_km": "sum",
            "id": "count"
        }).rename(columns={"id": "activity_count"}).reset_index()
        summary_df.to_csv(SUMMARY_FILE, index=False)

        # Print summary
        print(f"\nSuccess! Exported {len(df)} activities to {OUTPUT_FILE}")
        print(f"Summary saved to {SUMMARY_FILE}")
        print(f"\nActivity Summary:")
        for _, row in summary_df.iterrows():
            print(f"  {row['sport_type']}: {row['activity_count']} activities, {row['distance_km']:.1f} km")

    except Exception as e:
        print(f"Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
