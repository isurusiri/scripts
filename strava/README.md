# Strava Data Export Tool

A tool to authenticate with Strava API and export your activity data to CSV format. This tool fetches your activities from the past 2 years and provides both detailed activity data and summary statistics.

## Features

- **OAuth Authentication**: Secure authentication with Strava API
- **Token Refresh**: Automatic token refresh when expired
- **Data Export**: Export activities to CSV with comprehensive metrics
- **Summary Statistics**: Generate activity summaries by sport type
- **Error Handling**: Robust error handling with retry logic
- **Rate Limiting**: Respects Strava API rate limits
- **Cross-platform**: Works on macOS, Linux, and Windows

## Prerequisites

### System Requirements
- **curl**: For API requests
- **jq**: For JSON parsing
- **Python 3.7+**: For data processing
- **pip**: For Python package management

### Strava API Setup
1. Go to [Strava API Settings](https://www.strava.com/settings/api)
2. Create a new application
3. Note down your **Client ID** and **Client Secret**
4. Set the **Authorization Callback Domain** to `localhost`

## Installation

1. **Clone or download** this directory
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Make the auth script executable**:
   ```bash
   chmod +x strava_auth.sh
   ```

## Usage

### Step 1: Authenticate with Strava

Run the authentication script:

```bash
./strava_auth.sh
```

The script will:
- Check for required dependencies
- Prompt for your Strava Client ID and Secret (if not in `.env`)
- Open your browser for OAuth authorization
- Exchange the authorization code for access tokens
- Save tokens to `.env` file

### Step 2: Export Your Activities

Run the Python script to fetch and export your activities:

```bash
python3 fetch_strava_activities.py
```

The script will:
- Fetch all activities from the past 2 years
- Handle token refresh automatically if needed
- Export detailed activity data to `strava_activities_last_2_years.csv`
- Generate summary statistics in `strava_summary_by_sport.csv`
- Display progress and summary information

## Output Files

### `strava_activities_last_2_years.csv`
Contains detailed information for each activity:
- **id**: Strava activity ID
- **name**: Activity name
- **sport_type**: Type of sport/activity
- **start_date**: Activity start date and time
- **distance_km**: Distance in kilometers
- **moving_time_min**: Moving time in minutes
- **elapsed_time_min**: Total elapsed time in minutes
- **average_speed_kmph**: Average speed in km/h
- **max_speed_kmph**: Maximum speed in km/h
- **total_elevation_gain_m**: Total elevation gain in meters
- **average_heartrate**: Average heart rate (if available)
- **max_heartrate**: Maximum heart rate (if available)
- **calories**: Calories burned
- **trainer**: Whether activity was on trainer (0/1)
- **commute**: Whether activity was commute (0/1)

### `strava_summary_by_sport.csv`
Contains summary statistics grouped by sport type:
- **sport_type**: Type of sport/activity
- **distance_km**: Total distance for that sport type
- **activity_count**: Number of activities for that sport type

## Configuration

### Environment Variables
The tool uses a `.env` file to store configuration:

```env
STRAVA_CLIENT_ID=your_client_id
STRAVA_CLIENT_SECRET=your_client_secret
STRAVA_ACCESS_TOKEN=your_access_token
STRAVA_REFRESH_TOKEN=your_refresh_token
STRAVA_TOKEN_EXPIRES_AT=token_expiration_timestamp
```

### Customization
You can modify the following variables in `fetch_strava_activities.py`:
- `DAYS_BACK`: Number of days to look back (default: 730 = 2 years)
- `PER_PAGE`: Number of activities per API request (default: 200)
- `OUTPUT_FILE`: Name of the detailed CSV file
- `SUMMARY_FILE`: Name of the summary CSV file

## Troubleshooting

### Common Issues

**"curl not found" or "jq not found"**
- Install the missing dependency:
  - **macOS**: `brew install curl jq`
  - **Ubuntu/Debian**: `sudo apt-get install curl jq`
  - **Windows**: Use WSL or install via package manager

**"Missing STRAVA_ACCESS_TOKEN"**
- Run the authentication script first: `./strava_auth.sh`

**"Failed to retrieve access token"**
- Check your Client ID and Secret are correct
- Ensure your Strava app has the correct callback domain
- Try the authentication process again

**"Rate limited"**
- The script automatically handles rate limiting by waiting
- If you hit limits frequently, consider reducing `PER_PAGE`

**"Token expired"**
- The script automatically refreshes expired tokens
- If refresh fails, re-run the authentication script

### Error Messages

- **Error: [dependency] is not installed**: Install the missing system dependency
- **Error: Invalid authorization code**: Try the authentication process again
- **Error: Failed to connect to Strava API**: Check your internet connection
- **Rate limited**: The script will automatically wait and retry
- **Refreshing access token**: Normal behavior when token expires

## Security Notes

- The `.env` file contains sensitive tokens - keep it secure
- Tokens are automatically refreshed and updated in the `.env` file
- Never commit the `.env` file to version control
- Tokens expire after 6 hours but are automatically refreshed

## API Limits

Strava API has the following limits:
- **Rate limit**: 1000 requests per day, 100 requests per 15 minutes
- **Data access**: Activities from the past 2 years
- **Token expiration**: 6 hours (automatically handled)

## License

This tool is provided as-is for personal use. Please respect Strava's API terms of service.