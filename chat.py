import os
from dotenv import load_dotenv
from groq import Groq
import upload
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


def generate_response(prompt):
    input = f"""Your task is to analyze the given conversation and generate few keywords that can be used to search for a song.
        These Keywords can be based on the mood of the conversation, the genre of the song, the artist, or the lyrics of the song.
        Conversation: {prompt}
    """
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
                "content": f"What are the name of the songs in the given data? DATA: {result}",
            }
        ],
        model="gemma-7b-it",
    )
    return chat_completion.choices[0].message.content

# print(generate_response("Hello"))