import os
from dotenv import load_dotenv
from groq import Groq
import upload
import re
import json
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def generate_response(prompt):
    input = f"""Your task is to analyze the given conversation and generate few keywords that can be used to search for a song.
        These Keywords can be based on the mood of the conversation, the genre of the song, the artist, or the lyrics of the song.
        Conversation: {prompt}
    """
    print(prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model="gemma-7b-it",
    )

    res = chat_completion.choices[0].message.content
    print(res)
    result = upload.query_search(res)
    print(result)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
                - UNDERSTAND THE GIVEN CONVERSATION
                - based on the our conversation YOU HAVE TO recommend Me a song to listen from the given Data.
                - YOU HAVE TO GIVE ATLEAST `1` SONG RECOMMENDATION
                - NO NEED TO MENTION ANYTHING ABOUT THE NAME OF THE SONG ARTIST
                - MAKE SURE THE SONG NAME IS INSIDE DOUBLE QUOTES
                
                Conversation: ```{prompt}```
                DATA: ```{result}```
                """,
            }
        ],
        model="gemma-7b-it",
    )
    res = chat_completion.choices[0].message.content
    print(res)
    
    with open('data.json') as f:
        data = json.load(f)
    spotify_links = []
    spotify_link = None

    try: 
        song_name_pattern = r'\*\*"([^"]*)"\*\*|\*\*(.*?)\*\*|"([^"]*)"'
        matches = re.findall(song_name_pattern, res)

        for match in matches:
            # Get the first non-None group
            song_name = next(group for group in match if group is not None)
            print(song_name)

            for item in data["songs"]:
                if item['title'].lower() == song_name.lower() and 'spotify_link' in item and item['spotify_link']:
                    spotify_links.append(item['spotify_link'])
                    break
            
            spotify_link = spotify_links[0] if spotify_links else None
            if spotify_link:
                print(spotify_link)
            else:
                print(f"No Spotify link found for song: {song_name}")

    except Exception as e:
        print(e)
    
    return res, spotify_link 