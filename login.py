from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Enable CORS (optional if using frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- Database Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # change if not local
        user="root",            # your mysql username
        password="",# your mysql password
        database="userdb"       # your database name
    )

# ---------- Request Model ----------
class LoginRequest(BaseModel):
    email: str
    password: str

# ---------- API Route ----------
@app.post("/login")
def login_user(request: LoginRequest):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = "SELECT id, name, email FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (request.email, request.password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return {"message": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")
