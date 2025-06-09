from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient


client = MongoClient("mongodb+srv://pratham:prem2003@cluster0.pw1dc.mongodb.net/")
Checkpointer = MongoDBSaver(client)