import os
import time
import csv
from dotenv import load_dotenv
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from rapidfuzz import fuzz

load_dotenv()

# --- Config ---
YTM_HEADERS = os.getenv("YTMUSIC_HEADERS_FILE", "headers_auth.json")
PLAYLIST_NAME = os.getenv("PLAYLIST_NAME", "YouTube Liked → Spotify")

SPOTIFY_SCOPES = "playlist-modify-private playlist-modify-public"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def normalize_title(t):
    return t.split("(")[0].split("[")[0].strip()

def best_spotify_match(sp, title, artists):
    query = f'{title} {" ".join(artists)}'
    results = sp.search(q=query, type="track", limit=5)
    if not results["tracks"]["items"]:
        return None

    target = f"{title} {' '.join(artists)}".lower()
    best = None
    best_score = 0

    for item in results["tracks"]["items"]:
        candidate = f"{item['name']} {' '.join(a['name'] for a in item['artists'])}".lower()
        score = fuzz.token_set_ratio(candidate, target)
        if score > best_score:
            best_score = score
            best = item["uri"]

    return best if best_score >= 70 else None

def chunked(iterable, size=100):
    for i in range(0, len(iterable), size):
        yield iterable[i:i+size]

def main():
    # --- YouTube liked songs ---
    yt = YTMusic(YTM_HEADERS)
    liked = yt.get_liked_songs(limit=None)
    songs = [
        {"title": t["title"], "artists": [a["name"] for a in t["artists"]]}
        for t in liked["tracks"]
    ]
    print(f"Fetched {len(songs)} liked songs from YouTube Music.")

    # --- Spotify auth ---
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=SPOTIFY_SCOPES,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        open_browser=True,
        cache_path=".spotipy_cache"
    ))
    user_id = sp.current_user()["id"]

    # Create playlist
    playlist = sp.user_playlist_create(
        user=user_id,
        name=PLAYLIST_NAME,
        public=False,
        description="Imported from YouTube Music"
    )
    playlist_id = playlist["id"]
    print(f"Created playlist: {PLAYLIST_NAME}")

    matched_uris = []
    unmatched = []

    for idx, s in enumerate(songs, 1):
        uri = best_spotify_match(sp, s["title"], s["artists"])
        if uri:
            matched_uris.append(uri)
            print(f"[{idx}] ✓ {s['title']} – {', '.join(s['artists'])}")
        else:
            unmatched.append(s)
            print(f"[{idx}] ✗ {s['title']} – {', '.join(s['artists'])}")

        time.sleep(0.05)

    # Add tracks in batches
    for batch in chunked(matched_uris):
        sp.playlist_add_items(playlist_id, batch)

    # Save unmatched
    if unmatched:
        with open("unmatched.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "artists"])
            writer.writeheader()
            for s in unmatched:
                writer.writerow({
                    "title": s["title"],
                    "artists": ", ".join(s["artists"])
                })
        print(f"Transfer complete. {len(unmatched)} songs unmatched → unmatched.csv")
    else:
        print("Transfer complete. All songs matched 🎉")

if __name__ == "__main__":
    main()
