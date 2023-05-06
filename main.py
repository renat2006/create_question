import os
import re
import time
from datetime import datetime
import psycopg2
import openai
from dotenv import load_dotenv
from psycopg2 import sql

load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


def create_question():
    prompt = f"Придумай вопрос для игры Что? Где? Когда?. Также должен быть ответ и две подсказки. Данные должны быть в формате JSON, где ключи: question, answer, hint1, hint2"

    print(prompt)
    messages = [{"role": "system", "content": "Ты автор вопросов для игры Что? Где? Когда?"},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,

    )

    data = response.choices[0].message.content
    print(data)

    return data

def connect_to_db():


    conn = psycopg2.connect("""
        host=rc1b-1dkhcvps79tr5wu2.mdb.yandexcloud.net
        port=6432
        dbname=questions
        user=user1
        password=Taner2320
        target_session_attrs=read-write
    """)

    q = conn.cursor()
    q.execute('INSERT INTO questions(question, answer, hint1, hint2) VALUES();')

    conn.autocommit = True
    values = [
        ()
    ]
    insert = sql.SQL('INSERT INTO questions (question, answer, hint1, hint2) VALUES {}').format(
        sql.SQL(',').join(map(sql.Literal, values))
    )

    conn.close()

