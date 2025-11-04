# manage_liked.py
import os, time, datetime
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

# ── config ─────────────────────────────────────────────────────────────────────
SPOTIFY_SCOPES = (
    "playlist-read-private playlist-modify-private playlist-modify-public "
    "user-library-read user-library-modify"
)
CLIENT_ID     = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI  = os.getenv("SPOTIFY_REDIRECT_URI")

# Name of the playlist created by your transfer script (YouTube → Spotify)
TRANSFER_PLAYLIST_NAME = os.getenv("PLAYLIST_NAME", "YouTube Liked → Spotify")

# ── helpers ───────────────────────────────────────────────────────────────────
def auth(cache_path=".spotipy_cache_manage"):
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        scope=SPOTIFY_SCOPES,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        open_browser=True,
        cache_path=cache_path
    ))

def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i+n]

def get_all_liked_uris(sp):
    uris, offset = [], 0
    while True:
        page = sp.current_user_saved_tracks(limit=50, offset=offset)
        items = page.get("items", [])
        if not items: break
        uris.extend(t["track"]["uri"] for t in items if t.get("track"))
        offset += len(items)
    return uris

def create_backup_playlist(sp, name, uris):
    me = sp.current_user()["id"]
    pl = sp.user_playlist_create(
        user=me,
        name=name,
        public=False,
        description="Auto-backup of Liked Songs"
    )
    pid = pl["id"]
    for batch in chunked(uris, 100):
        sp.playlist_add_items(pid, batch)
        time.sleep(0.05)
    return pid

def remove_all_liked(sp, total_count=None):
    # remove in pages; removal is limited to 50 per call
    removed, offset = 0, 0
    while True:
        page = sp.current_user_saved_tracks(limit=50, offset=0)  # always refetch first page
        items = page.get("items", [])
        if not items: break
        batch = [t["track"]["uri"] for t in items if t.get("track")]
        sp.current_user_saved_tracks_delete(batch)
        removed += len(batch)
        print(f"Removed {removed}{'' if total_count is None else f' / {total_count}'}")
        time.sleep(0.05)
    return removed

def find_playlist_by_name(sp, name):
    me = sp.current_user()["id"]
    results = sp.current_user_playlists(limit=50)
    while True:
        for pl in results.get("items", []):
            if pl["name"] == name and pl["owner"]["id"] == me:
                return pl
        if results.get("next"):
            results = sp.next(results)
        else:
            return None

def get_all_playlist_track_uris(sp, playlist_id):
    uris = []
    results = sp.playlist_items(playlist_id, additional_types=["track"], limit=100)
    while True:
        for it in results.get("items", []):
            track = it.get("track")
            if track and track.get("uri"):
                uris.append(track["uri"])
        if results.get("next"):
            results = sp.next(results)
        else:
            break
    return uris

def like_tracks(sp, uris):
    added = 0
    for batch in chunked(uris, 50):
        sp.current_user_saved_tracks_add(batch)
        added += len(batch)
        print(f"Liked {added} / {len(uris)}")
        time.sleep(0.05)
    return added

# ── main flow ─────────────────────────────────────────────────────────────────
def main():
    sp = auth()

    # 1) Backup current liked songs → playlist
    print("Fetching your current Liked Songs…")
    liked_uris = get_all_liked_uris(sp)
    print(f"Found {len(liked_uris)} liked tracks.")

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    backup_name = f"Backup - Liked Songs ({ts})"
    if liked_uris:
        print(f"Creating backup playlist: {backup_name}")
        backup_id = create_backup_playlist(sp, backup_name, liked_uris)
        print(f"Backup created ✓  ({len(liked_uris)} tracks)")
    else:
        print("No liked songs to back up.")

    # 2) Remove everything from Liked Songs
    if liked_uris:
        print("Clearing Liked Songs…")
        removed = remove_all_liked(sp, total_count=len(liked_uris))
        print(f"Removed {removed} tracks from Liked Songs ✓")

    # 3) Add transferred playlist tracks into Liked Songs
    print(f"Looking for transfer playlist: {TRANSFER_PLAYLIST_NAME!r}")
    transfer_pl = find_playlist_by_name(sp, TRANSFER_PLAYLIST_NAME)
    if not transfer_pl:
        print("⚠️ Transfer playlist not found. "
              "Check PLAYLIST_NAME in your .env or create the playlist first.")
        return

    print("Fetching tracks from transfer playlist…")
    transfer_uris = get_all_playlist_track_uris(sp, transfer_pl["id"])
    print(f"Found {len(transfer_uris)} tracks in transfer playlist.")

    if transfer_uris:
        print("Liking transfer playlist tracks…")
        added = like_tracks(sp, transfer_uris)
        print(f"Added {added} tracks to Liked Songs ✓")
    else:
        print("Transfer playlist is empty.")

    print("All done 🎉")

if __name__ == "__main__":
    main()
