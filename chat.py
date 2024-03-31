import os
from dotenv import load_dotenv
from groq import Groq
import upload
import re
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
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""based on the our conversation which song do you recommend Me to listen from the given Data.
                    Conversation: ```{prompt}```
                    DATA: {result}
                """,
            }
        ],
        model="gemma-7b-it",
    )
    return chat_completion.choices[0].message.content

def get_music(data):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Your task is to analyze the given text data and find the best music that the user can listen to which is mentioned in the given data.
                    GIVE ONLY ONE SONG.
                    Output should be in following format:
                    Song Name: <song name>

                    DATA: {data}
                """,
            }
        ],
        model="gemma-7b-it",
    )
    res = upload.query_search(chat_completion.choices[0].message.content, n=1)
    print(res)
    res = res[0][0]
    spotify_link_pattern = r'https://open\.spotify\.com/embed/track/[^\s\'\"]*'
    match = re.search(spotify_link_pattern, str(res))

    if match:
        spotify_link = match.group()
        print(spotify_link)

    return spotify_link