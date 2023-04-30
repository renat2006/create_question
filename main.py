import os
import re
import time
from datetime import datetime



import openai
from dotenv import load_dotenv



load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")

def createPostcontentName():
    prompt = f"Придумай необычную тему для поста"

    print(prompt)
    messages = [{"role": "system", "content": "Ты креативный автор блога про здоровый образ жизни"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,

    )

    theme_ = response.choices[0].message.content
    print(theme_)
    if '.' in theme_:
        theme_ = theme_.split('.')[0]
    print(theme_)
    return theme_