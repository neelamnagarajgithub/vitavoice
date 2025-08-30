import os
from dotenv import load_dotenv
from pymongo import MongoClient
from passlib.hash import bcrypt

load_dotenv()  # Load variables from .env

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)


db = client["vitavoice"]
users_col = db["users"]

# Signup
def signup(username,  password,role):
    if users_col.find_one({"username": username}):
        return False, "Username already exists"
    hashed_pw = bcrypt.hash(password)
    users_col.insert_one({"username": username, "password": hashed_pw,"role":role})
    return True, "User created successfully"

# Login
def login(username, password, role):
    user = users_col.find_one({"username": username})
    if not user:
        return False, "User not found"
    if bcrypt.verify(password, user["password"]):
        if user["role"] == role:
            return True, "Login successful"
        else:
            return False, "Incorrect role"
    return False, "Incorrect password"
