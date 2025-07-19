from pymongo import MongoClient

client = MongoClient("mongodb+srv://obs_user:esmanur@obs.tj8yvnb.mongodb.net/?retryWrites=true&w=majority&appName=obs")
db = client["mydb"]
ogrenciler = db["ogrenciler"]
notlar = db["notlar"]
