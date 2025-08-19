from fastapi import FastAPI
import mysql.connector

app=FastAPI()

def my_connection():
    connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="userdb"
    )

    return connection

@app.get("/users")
def getusers():
    conn = my_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id,name,email FROM users")
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    return {"users": users}