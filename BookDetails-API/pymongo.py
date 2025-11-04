import pymongo 

url = 'mongodb+srv://sss:123@cluster0.f0xb8zo.mongodb.net/'
client = pymongo.MongoClient(url)
db = client['bookstore'] 