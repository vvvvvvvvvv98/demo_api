from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()
# ------------------------------
# MySQL connection (no DB first)
# ------------------------------
db_server = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor_server = db_server.cursor()
cursor_server.execute("CREATE DATABASE IF NOT EXISTS userdb")
cursor_server.close()
db_server.close()

# Connect to userdb
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="userdb"
)
cursor = db.cursor(dictionary=True)

# Create table if not exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255)
    )
""")
db.commit()

# ------------------------------
# Pydantic model for request
# ------------------------------
class User(BaseModel):
    name: str
    email: str
    password: str

# ------------------------------
# Register API
# ------------------------------
@app.post("/register")
def register(user: User):
    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (user.name, user.email, user.password)
        )
        db.commit()
        return {"message": f"{user.name} registered successfully"}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=str(err))
