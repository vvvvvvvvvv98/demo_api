from fastapi import FastAPI, Depends, HTTPException, Header
import requests

app = FastAPI()

BASE_URL = "https://jsonplaceholder.typicode.com"

@app.get("/post")
def getpost():
    response=requests.get(f"{BASE_URL}/posts")
    if response.status_code==200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Error fetching posts")



