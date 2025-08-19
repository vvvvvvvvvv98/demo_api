from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import mysql.connector

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
COHERE_API_KEY = "xPn6OZ8TLcWsjtI1aKJBo6ZkwS1GZIuudd1daZc2"  


db_server = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor_server = db_server.cursor()
cursor_server.execute("CREATE DATABASE IF NOT EXISTS ai_chat_db")
cursor_server.close()
db_server.close()
# ---------- MySQL Setup ----------
db = mysql.connector.connect(
    host="localhost",
    user="root",          # your MySQL username
    password="",  # your MySQL password
    database="ai_chat_db"
)
cursor = db.cursor()





cursor.execute("""
CREATE TABLE IF NOT EXISTS ai_responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_prompt TEXT,
    ai_response TEXT
)
""")


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

        # Save into MySQL
        cursor.execute(
            "INSERT INTO ai_responses (user_prompt, ai_response) VALUES (%s, %s)",
            (prompt, ai_response)
        )
        db.commit()

        return {"prompt": prompt, "response": ai_response}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)
