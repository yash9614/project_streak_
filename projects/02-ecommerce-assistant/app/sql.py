import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

sql_prompt = """You are an expert SQL writer.
Table: product (title, brand, price, discount, avg_rating)
Generate a single SELECT * query for the user's question.
Always use LIKE for brand names (case-insensitive).
Return only the SQL query, nothing else.
"""

def generate_sql(question: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[
            {"role": "system", "content": sql_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )
    return response.choices[0].message.content.strip()


import sqlite3
import pandas as pd
from pathlib import Path

db_path = Path(__file__).parent.parent / "data" / "db.sqlite"

def run_query(sql: str):
    with sqlite3.connect(db_path) as conn:
        return pd.read_sql_query(sql, conn)

def answer_from_data(question: str, df) -> str:
    prompt = f"""Turn the following data into a short, natural answer.
Do not mention SQL or databases.

QUESTION: {question}
DATA: {df.to_dict(orient='records')}
"""
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content