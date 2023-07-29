import grab
import secret
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_playlists_readable(sp, exclude=None):
    if exclude is None:
        exclude = []
    results = sp.current_user_playlists()
    playlists = []
    for idx, item in enumerate(results['items']):
        playlists.append(f"{item['name']} | {item['id']}")
    for each in exclude:
        if each[-1:] == '\n':
            each = each[:-1]
        playlists.remove(each)
        playlists = playlists.sort()
    return playlists


def run():
    data = grab.Default()
    hi = secret.Secrets()
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(hi.id(), hi.password(), "http://localhost:8080", scope='playlist-read-private playlist-modify-private playlist-modify-public'))



    playlists = []

    for each in get_playlists_readable(sp, data.exclude):
        playlists.append(each[each.index('|') + 2:])

    songs = []
    for playlist in playlists:
        results = sp.playlist_items(playlist)
        tracks = results['items']
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        for i in tracks:
            try:
                track = i['track']['uri']
                songs.append(track)
            except TypeError:
                continue

    res = list(dict.fromkeys(songs))

    if 'spotify:track:None' in res:
        res.remove('spotify:track:None')
    for each in res:
        if 'local' in each:
            res.remove(each)
    if filter:
        for each in res:
            if 'episode' in each:
                res.remove(each)
    res.sort()
    print(res[0])

    def divide_chunks(l, n):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    res = list(divide_chunks(res, 100))
    sp.playlist_replace_items(data.id, [])
    for chunk in res:
        sp.playlist_add_items(data.id, chunk)