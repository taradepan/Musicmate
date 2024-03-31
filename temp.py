import json
import re

with open('data.json') as f:
    data = json.load(f)
res="""sjgsjg "often" sjgsjgjsgsjg"""
song_name_pattern = r'"(.*?)"'
match = re.search(song_name_pattern, res)

if match:
    song_name = match.group(1)
    print(song_name)
    for item in data["songs"]:
        if item['title'].lower() == song_name.lower():
            spotify_link = item['spotify_link']
            print(spotify_link)
            break