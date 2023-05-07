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


def check_string(string_to_check):
    if re.match(r'^[А-Яа-я ]+$', string_to_check) and len(string_to_check.split()) <= 2:
        return True
    else:
        return False


def create_question():
    prompt = f"Придумай вопрос для викторины. Также должен быть ответ и две подсказки. Ответ должно быть легко произнести. Данные должны быть в формате JSON, где ключи: question, answer, hint1, hint2"

    print(prompt)
    messages = [{"role": "system", "content": "Ты автор вопросов для викторины "},
                {"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,

    )

    data = response.choices[0].message.content
    print(data)

    return eval(data)


def insert_to_db(data):
    conn = psycopg2.connect("""
        host=rc1b-1dkhcvps79tr5wu2.mdb.yandexcloud.net
        port=6432
        dbname=questions
        user=user1
        password=Taner2320
        target_session_attrs=read-write
    """)

    cur = conn.cursor()

    question = data["question"]
    answer = data["answer"]
    hint1 = data["hint1"]
    hint2 = data["hint2"]

    cur.execute("INSERT INTO chgk_questions (question, answer, hint1, hint2) VALUES (%s, %s, %s, %s)",
                (question, answer, hint1, hint2))

    conn.commit()
    cur.close()
    conn.close()
    print("ok")


for i in range(20):

    q_data = create_question()
    if not check_string(q_data["answer"]):
        continue
    insert_to_db(q_data)
    time.sleep(31)
    print("__________________")
