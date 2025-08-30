import os
from dotenv import load_dotenv
from pymongo import MongoClient
from passlib.hash import bcrypt
import requests
import json

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)



db = client["vitavoice"]
quiries_col = db["quiries"]
users_col = db["users"]

def queries(username,  query):
    if users_col.find_one({"username": username}):
        output=nlp_processor(query);
        quiries_col.insert_one({"username": username, "query": query,"output":output})
        return output
    else :
        return False, "Username already exists"



def nlp_processor(query):
    prompt = (
    "You are an AI health assistant. Respond to the following patient query in a clear, concise, and professional manner, just like a doctor would.\n"
    f"Patient: {query}\n"
    "AI Doctor:"
    )
    
    api_url = "https://openrouter.ai/api/v1/chat/completions"
    api_key = os.getenv("OPEN_ROUTER_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",  # You can change to another available model
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 300
    }

    response = requests.post(api_url, headers=headers, data=json.dumps(data))
    result = response.json()
    doctor_reply = result["choices"][0]["message"]["content"] if "choices" in result else str(result)

    return doctor_reply

