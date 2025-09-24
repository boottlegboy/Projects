from ytmusicapi import YTMusic

yt = YTMusic("headers_auth.json")
liked = yt.get_liked_songs(limit=5)
for t in liked["tracks"]:
    print(t["title"], "-", ", ".join(a["name"] for a in t["artists"]))
