from pymongo import MongoClient
from app.settings import get_database_string_conection


CONNECTION_STRING = get_database_string_conection()

def get_database():
   client = MongoClient(CONNECTION_STRING)
   return client['db_votacion']