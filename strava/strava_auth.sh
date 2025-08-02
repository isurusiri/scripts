#!/bin/bash

# Check for required dependencies
check_dependency() {
    if ! command -v "$1" &> /dev/null; then
        echo "Error: $1 is not installed. Please install it first."
        exit 1
    fi
}

echo "Checking dependencies..."
check_dependency "curl"
check_dependency "jq"

# Check if .env exists, create if not
if [[ ! -f ".env" ]]; then
    echo "Creating .env file..."
    touch .env
fi

# Load client ID and secret from .env or prompt if not available
source .env 2>/dev/null

if [[ -z "$STRAVA_CLIENT_ID" ]]; then
  read -p "Enter your Strava CLIENT_ID: " STRAVA_CLIENT_ID
fi

if [[ -z "$STRAVA_CLIENT_SECRET" ]]; then
  read -p "Enter your Strava CLIENT_SECRET: " STRAVA_CLIENT_SECRET
fi

REDIRECT_URI="http://localhost"
SCOPE="activity:read_all"
AUTH_URL="https://www.strava.com/oauth/authorize?client_id=$STRAVA_CLIENT_ID&response_type=code&redirect_uri=$REDIRECT_URI&approval_prompt=force&scope=$SCOPE"

echo ""
echo "Opening browser for authentication..."
echo "If it doesn't open, visit this URL:"
echo "$AUTH_URL"
echo ""

sleep 2

# Try to open browser (macOS, Linux, Windows)
if command -v open &> /dev/null; then
    open "$AUTH_URL" 2>/dev/null
elif command -v xdg-open &> /dev/null; then
    xdg-open "$AUTH_URL" 2>/dev/null
elif command -v start &> /dev/null; then
    start "$AUTH_URL" 2>/dev/null
else
    echo "Could not automatically open browser. Please visit the URL manually."
fi

read -p "Paste the 'code' from the redirected URL: " CODE

# Validate code format
if [[ -z "$CODE" || ${#CODE} -lt 10 ]]; then
    echo "Error: Invalid authorization code. Please try again."
    exit 1
fi

echo ""
echo "Exchanging code for access token..."

RESPONSE=$(curl -s -X POST https://www.strava.com/oauth/token \
  -F client_id=$STRAVA_CLIENT_ID \
  -F client_secret=$STRAVA_CLIENT_SECRET \
  -F code=$CODE \
  -F grant_type=authorization_code)

# Check if curl request was successful
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to connect to Strava API. Check your internet connection."
    exit 1
fi

STRAVA_ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
STRAVA_REFRESH_TOKEN=$(echo $RESPONSE | jq -r '.refresh_token')
STRAVA_TOKEN_EXPIRES_AT=$(echo $RESPONSE | jq -r '.expires_at')

if [[ "$STRAVA_ACCESS_TOKEN" == "null" || -z "$STRAVA_ACCESS_TOKEN" ]]; then
    echo "Error: Failed to retrieve access token."
    echo "Response: $RESPONSE"
    echo ""
    echo "Possible issues:"
    echo "- Authorization code may have expired (try again)"
    echo "- Invalid client ID or secret"
    echo "- Network connectivity issues"
    exit 1
fi

# Save to .env
echo ""
echo "Auth successful. Saving to .env ..."
cat <<EOF > .env
STRAVA_CLIENT_ID=$STRAVA_CLIENT_ID
STRAVA_CLIENT_SECRET=$STRAVA_CLIENT_SECRET
STRAVA_ACCESS_TOKEN=$STRAVA_ACCESS_TOKEN
STRAVA_REFRESH_TOKEN=$STRAVA_REFRESH_TOKEN
STRAVA_TOKEN_EXPIRES_AT=$STRAVA_TOKEN_EXPIRES_AT
EOF

echo "All set! You can now run your Python script."
echo "Token expires at: $(date -r $STRAVA_TOKEN_EXPIRES_AT)"
