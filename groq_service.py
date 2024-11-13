from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()
client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1"
)


def stream_groq_chat(chat, temprature=1):
    response = client.chat.completions.create(
        messages=chat,
        model="llama-3.2-90b-vision-preview",
        stream=True,
        temperature=temprature,
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield str(chunk.choices[0].delta.content)
