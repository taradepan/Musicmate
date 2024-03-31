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
                    - based on the our conversation YOU HAVE TO recommend Me a song to listen from the given Data.
                    - YOU HAVE TO GIVE ATLEAST 1 SONG RECOMMENDATION FROM THE GIVEN DATA.
                    - NO NEED TO MENTION ANYTHING ABOUT THE NAME OF THE SONG ARTIST.
                    - MAKE SURE THE SONG IS INSIDE DOUBLE QUOTES.
                    Conversation: ```{prompt}```
                    DATA: {result}
                    - What is the Output? 
                    - Do you think you have given the correct output? If yes then move to the next step otherwise go back to the first step. REMEMBER YOU HAVE TO PROVIDE ATLEAST 1 SONG.
                    - STRICTLY GIVE YOUR RESPONSE CONTAINING THE SONG NAME (in Double quotes) AND THE REASON FOR SELECTING THIS SONG ONLY. 
                """,
            }
        ],
        model="gemma-7b-it",
    )
    res = chat_completion.choices[0].message.content
    print(res)
    
    with open('data.json') as f:
        data = json.load(f)
    spotify_link = None
    
    try: 
        song_name_pattern = r'\*\*"([^"]*)"\*\*|\*\*(.*?)\*\*|"([^"]*)"'
    
        match = re.search(song_name_pattern, res)

        if match:
            song_name = match.group(1)
            print(song_name)
            for item in data["songs"]:
                if item['title'].lower() == song_name.lower():
                    spotify_link = item['spotify_link']
                    break
    except Exception as e:
        print(e)
    
    return res, spotify_link