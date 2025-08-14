# Spotify Playlist Creator

A powerful tool to create Spotify playlists with specified songs. Supports both public and private playlists with configurable settings through environment variables or command line arguments.

## Features

- **OAuth Authentication**: Secure authentication with Spotify API using OAuth 2.0
- **Flexible Song Input**: Accept songs via command line, environment variables, or use built-in defaults
- **Customizable Playlists**: Set custom names, descriptions, and visibility (public/private)
- **Smart Track Search**: Intelligent song matching with detailed search results
- **Batch Processing**: Efficiently add multiple tracks to playlists
- **Environment Configuration**: Support for `.env` files and environment variables
- **Verbose Output**: Optional detailed logging for debugging and monitoring
- **Cross-platform**: Works on macOS, Linux, and Windows

## Prerequisites

### System Requirements
- **Python 3.7+**: For running the script
- **pip**: For Python package management

### Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Note down your **Client ID** and **Client Secret**
4. Set the **Redirect URI** to `http://localhost:8888/callback` (or your preferred URI)
5. Add the following scopes to your app:
   - `playlist-modify-public`
   - `playlist-modify-private`

## Installation

### Quick Setup (Recommended)

Use the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Installation

1. **Clone or download** this directory
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables** (see Configuration section below)

## Configuration

### Environment Variables

Create a `.env` file in the `spotify/` directory with your Spotify credentials:

```env
# Required
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here

# Optional (with defaults)
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
SPOTIFY_SCOPE=playlist-modify-public,playlist-modify-private
SPOTIFY_CACHE_PATH=.spotify-cache
SPOTIFY_PLAYLIST_NAME=Temple of Chills
SPOTIFY_PLAYLIST_DESCRIPTION=Made by the GPT playlist gods
SPOTIFY_DEFAULT_SONGS=Song1 - Artist1,Song2 - Artist2,Song3 - Artist3
```

### Alternative: Set Environment Variables Directly

```bash
export SPOTIFY_CLIENT_ID="your_client_id_here"
export SPOTIFY_CLIENT_SECRET="your_client_secret_here"
```

## Usage

### Basic Usage

Create a playlist with default settings:

```bash
python3 create_playlist.py
```

### Advanced Usage

Create a custom playlist with specific songs:

```bash
python3 create_playlist.py \
  --name "My Awesome Mix" \
  --description "A collection of my favorite songs" \
  --songs "Bohemian Rhapsody - Queen" "Hotel California - Eagles" "Stairway to Heaven - Led Zeppelin"
```

Create a private playlist:

```bash
python3 create_playlist.py --private
```

Use verbose output for detailed information:

```bash
python3 create_playlist.py --verbose
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--name` | `-n` | Playlist name | `Temple of Chills` |
| `--description` | `-d` | Playlist description | `Made by the GPT playlist gods` |
| `--songs` | `-s` | List of songs in 'Song - Artist' format | Built-in defaults |
| `--private` | `-p` | Make playlist private | Public |
| `--redirect-uri` | `-r` | OAuth redirect URI | `http://localhost:8888/callback` |
| `--scope` | `-S` | Spotify API scope | `playlist-modify-public,playlist-modify-private` |
| `--cache-path` | `-c` | Path for OAuth cache | `.spotify-cache` |
| `--verbose` | `-v` | Enable verbose output | False |

## Examples

### Example 1: Quick Start
```bash
# Set credentials
export SPOTIFY_CLIENT_ID="abc123"
export SPOTIFY_CLIENT_SECRET="xyz789"

# Create default playlist
python3 create_playlist.py
```

### Example 2: Custom Playlist
```bash
python3 create_playlist.py \
  --name "Workout Mix 2024" \
  --description "High-energy songs for my daily workouts" \
  --songs \
    "Eye of the Tiger - Survivor" \
    "We Will Rock You - Queen" \
    "Lose Yourself - Eminem" \
    "Stronger - Kanye West"
```

### Example 3: Private Playlist with Verbose Output
```bash
python3 create_playlist.py \
  --name "Personal Favorites" \
  --private \
  --verbose \
  --songs "Wonderwall - Oasis" "Creep - Radiohead"
```

## Output

### Console Output
The script provides detailed feedback during execution:

```
Spotify Playlist Creator
========================================
Playlist: Temple of Chills
Description: Made by the GPT playlist gods
Visibility: Public
Songs to add: 5

Authenticating with Spotify...
Logged in as: John Doe

Searching for tracks...

Search Results:
  Found: 5 songs

Creating playlist...
Successfully added 5 tracks to playlist!

Playlist 'Temple of Chills' created successfully!
Playlist URL: https://open.spotify.com/playlist/...
Open in Spotify: spotify:playlist:...
```

### Generated Files
- **`.spotify-cache`**: OAuth token cache (automatically managed)
- **Playlist**: Created in your Spotify account

## Troubleshooting

### Common Issues

**"Missing required environment variables"**
- Ensure `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` are set
- Check your `.env` file or environment variables

**"Failed to authenticate with Spotify"**
- Verify your Client ID and Secret are correct
- Ensure your redirect URI matches what's set in Spotify Dashboard
- Check that your app has the required scopes

**"No tracks found"**
- Verify song names and artist names are correct
- Use the `--verbose` flag to see detailed search results
- Some songs may not be available on Spotify

**OAuth Cache Issues**
- Delete the `.spotify-cache` file if you change redirect URIs
- Clear browser cookies for localhost if authentication fails

### Error Messages

- **"Failed to authenticate"**: Check credentials and app configuration
- **"No tracks found"**: Review song list and try with `--verbose`
- **"Failed to create playlist"**: Check API permissions and network connection
- **"Failed to add tracks"**: Verify playlist creation and track URIs

## Security Notes

- **Never commit** your `.env` file to version control
- **Keep credentials secure** and don't share them
- **Use environment variables** in production environments
- **OAuth tokens** are automatically cached and refreshed
- **API scopes** are limited to playlist modification only

## API Limits

Spotify API has the following limits:
- **Rate limiting**: 100 requests per second
- **Playlist size**: Maximum 10,000 tracks per playlist
- **Search results**: Limited to 50 tracks per search query
- **Token expiration**: Automatically handled by the script

## Customization

### Adding Default Songs

Set the `SPOTIFY_DEFAULT_SONGS` environment variable:

```env
SPOTIFY_DEFAULT_SONGS=Song1 - Artist1,Song2 - Artist2,Song3 - Artist3
```

### Custom Scopes

Modify the scope in your `.env` file:

```env
SPOTIFY_SCOPE=playlist-modify-public,playlist-modify-private,user-read-private
```

### Custom Cache Location

Set a custom cache path:

```env
SPOTIFY_CACHE_PATH=/path/to/your/cache
```

## License

This tool is provided as-is for personal use. Please respect Spotify's API terms of service and usage guidelines.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool. When contributing:

1. Follow the existing code style
2. Add appropriate error handling
3. Update documentation for new features
4. Test with various Spotify API responses
