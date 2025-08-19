from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cohere v2 Chat API endpoint
COHERE_URL = "https://api.cohere.ai/v2/chat"
COHERE_API_KEY = os.environ.get("COHERE_API_KEY")  # store in Render environment variable

# ---------- PostgreSQL Setup ----------
db = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    dbname=os.environ.get("DB_NAME")
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_responses (
    id SERIAL PRIMARY KEY,
    user_prompt TEXT,
    ai_response TEXT
)
""")
db.commit()

# ---------- API Endpoint ----------
@app.post("/generate")
def chat_with_ai(prompt: str):
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "command-a-03-2025",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(COHERE_URL, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        ai_response = data["message"]["content"][0]["text"]

        # Save into PostgreSQL
        cursor.execute(
            "INSERT INTO ai_responses (user_prompt, ai_response) VALUES (%s, %s)",
            (prompt, ai_response)
        )
        db.commit()

        return {"prompt": prompt, "response": ai_response}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
