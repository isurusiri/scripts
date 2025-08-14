#!/usr/bin/env python3
"""
Spotify Playlist Creator

A script to create Spotify playlists with specified songs. Supports both public and private playlists
with configurable settings through environment variables or command line arguments.
"""

import os
import argparse
import sys
from typing import List, Optional
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Create a Spotify playlist with specified songs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Create playlist with default settings
  python3 create_playlist.py

  # Create playlist with custom name and songs
  python3 create_playlist.py --name "My Custom Playlist" --songs "Song1 - Artist1" "Song2 - Artist2"

  # Create private playlist
  python3 create_playlist.py --private

  # Use custom redirect URI
  python3 create_playlist.py --redirect-uri "http://localhost:3000/callback"
        """
    )
    
    parser.add_argument(
        "--name", "-n",
        default=os.getenv("SPOTIFY_PLAYLIST_NAME", "Temple of Chills"),
        help="Playlist name (default: %(default)s)"
    )
    
    parser.add_argument(
        "--description", "-d",
        default=os.getenv("SPOTIFY_PLAYLIST_DESCRIPTION", "Made by the GPT playlist gods"),
        help="Playlist description (default: %(default)s)"
    )
    
    parser.add_argument(
        "--songs", "-s",
        nargs="+",
        default=None,
        help="List of songs in 'Song - Artist' format"
    )
    
    parser.add_argument(
        "--private", "-p",
        action="store_true",
        help="Make playlist private (default: public)"
    )
    
    parser.add_argument(
        "--redirect-uri", "-r",
        default=os.getenv("SPOTIFY_REDIRECT_URI", "http://localhost:8888/callback"),
        help="OAuth redirect URI (default: %(default)s)"
    )
    
    parser.add_argument(
        "--scope", "-S",
        default=os.getenv("SPOTIFY_SCOPE", "playlist-modify-public,playlist-modify-private"),
        help="Spotify API scope (default: %(default)s)"
    )
    
    parser.add_argument(
        "--cache-path", "-c",
        default=os.getenv("SPOTIFY_CACHE_PATH", ".spotify-cache"),
        help="Path for OAuth cache (default: %(default)s)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    return parser.parse_args()

def get_spotify_client(redirect_uri: str, scope: str, cache_path: str) -> spotipy.Spotify:
    """Initialize and authenticate Spotify client"""
    try:
        sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=os.getenv("SPOTIFY_CLIENT_ID"),
                client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
                redirect_uri=redirect_uri,
                scope=scope,
                open_browser=True,
                cache_path=cache_path
            )
        )
        return sp
    except Exception as e:
        print(f"Failed to authenticate with Spotify: {e}")
        print("Please check your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET environment variables")
        sys.exit(1)

def get_default_songs() -> List[str]:
    """Get default song list from environment or use built-in defaults"""
    env_songs = os.getenv("SPOTIFY_DEFAULT_SONGS")
    if env_songs:
        return [song.strip() for song in env_songs.split(",")]
    
    return [
        "Sweet Caroline - Neil Diamond",
        "In Da Club - 50 Cent",
        "Drop It Like It's Hot - Snoop Dogg",
        "Bebot - Black Eyed Peas",
        "Livin' la Vida Loca - Ricky Martin"
    ]

def search_tracks(sp: spotipy.Spotify, songs: List[str], verbose: bool = False) -> List[str]:
    """Search for tracks and return their URIs"""
    track_uris = []
    not_found = []
    
    for i, song in enumerate(songs, 1):
        if verbose:
            print(f"Searching for song {i}/{len(songs)}: {song}")
        
        try:
            result = sp.search(q=song, type='track', limit=1)
            tracks = result['tracks']['items']
            
            if tracks:
                track_uri = tracks[0]['uri']
                track_name = tracks[0]['name']
                artist_name = tracks[0]['artists'][0]['name']
                track_uris.append(track_uri)
                
                if verbose:
                    print(f"  Found: {track_name} by {artist_name}")
            else:
                not_found.append(song)
                if verbose:
                    print(f"  Not found: {song}")
                    
        except Exception as e:
            print(f"  Error searching for '{song}': {e}")
            not_found.append(song)
    
    # Report summary
    print(f"\nSearch Results:")
    print(f"  Found: {len(track_uris)} songs")
    if not_found:
        print(f"  Not found: {len(not_found)} songs")
        for song in not_found:
            print(f"    - {song}")
    
    return track_uris

def create_playlist(sp: spotipy.Spotify, name: str, description: str, public: bool, verbose: bool = False) -> dict:
    """Create a new playlist"""
    try:
        user_id = sp.current_user()['id']
        if verbose:
            print(f"Creating playlist for user: {sp.current_user()['display_name']}")
        
        playlist = sp.user_playlist_create(
            user=user_id,
            name=name,
            public=public,
            description=description
        )
        
        if verbose:
            print(f"Playlist created: {playlist['name']} (ID: {playlist['id']})")
            print(f"   Visibility: {'Public' if public else 'Private'}")
            print(f"   Description: {description}")
        
        return playlist
        
    except Exception as e:
        print(f"Failed to create playlist: {e}")
        sys.exit(1)

def add_tracks_to_playlist(sp: spotipy.Spotify, playlist_id: str, track_uris: List[str], verbose: bool = False) -> bool:
    """Add tracks to the playlist"""
    if not track_uris:
        print("❌ No tracks to add to playlist")
        return False
    
    try:
        if verbose:
            print(f"\nAdding {len(track_uris)} tracks to playlist...")
        
        # Spotify API allows max 100 tracks per request
        batch_size = 100
        for i in range(0, len(track_uris), batch_size):
            batch = track_uris[i:i + batch_size]
            sp.playlist_add_items(playlist_id=playlist_id, items=batch)
            
            if verbose:
                print(f"  Added batch {i//batch_size + 1}: {len(batch)} tracks")
        
        print(f"Successfully added {len(track_uris)} tracks to playlist!")
        return True
        
    except Exception as e:
        print(f"Failed to add tracks to playlist: {e}")
        return False

def main():
    """Main function"""
    args = parse_arguments()
    
    # Check required environment variables
    if not os.getenv("SPOTIFY_CLIENT_ID") or not os.getenv("SPOTIFY_CLIENT_SECRET"):
        print("Missing required environment variables:")
        print("   SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set")
        print("\nPlease set them in your .env file or environment:")
        print("   export SPOTIFY_CLIENT_ID='your_client_id'")
        print("   export SPOTIFY_CLIENT_SECRET='your_client_secret'")
        sys.exit(1)
    
    print("Spotify Playlist Creator")
    print("=" * 40)
    
    # Get songs list
    songs = args.songs if args.songs else get_default_songs()
    print(f"Playlist: {args.name}")
    print(f"Description: {args.description}")
    print(f"Visibility: {'Private' if args.private else 'Public'}")
    print(f"Songs to add: {len(songs)}")
    
    if args.verbose:
        print("\nSong list:")
        for i, song in enumerate(songs, 1):
            print(f"  {i}. {song}")
    
    # Initialize Spotify client
    print(f"\nAuthenticating with Spotify...")
    sp = get_spotify_client(args.redirect_uri, args.scope, args.cache_path)
    print(f"Logged in as: {sp.current_user()['display_name']}")
    
    # Search for tracks
    print(f"\nSearching for tracks...")
    track_uris = search_tracks(sp, songs, args.verbose)
    
    if not track_uris:
        print("No tracks found. Cannot create playlist.")
        sys.exit(1)
    
    # Create playlist
    print(f"\nCreating playlist...")
    playlist = create_playlist(sp, args.name, args.description, not args.private, args.verbose)
    
    # Add tracks
    success = add_tracks_to_playlist(sp, playlist['id'], track_uris, args.verbose)
    
    if success:
        print(f"\nPlaylist '{args.name}' created successfully!")
        print(f"Playlist URL: {playlist['external_urls']['spotify']}")
        print(f"Open in Spotify: {playlist['uri']}")
    else:
        print(f"\nFailed to create playlist completely.")
        sys.exit(1)

if __name__ == "__main__":
    main()
