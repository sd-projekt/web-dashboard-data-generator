from random import randint
import pymongo
import datetime

USER = "user"
PASS = "pass"
HOST = "localhost"
PORT = "27017"

CONNECTION_STRING = "mongodb://" + USER + ":" + PASS + "@" + HOST + ":" + PORT + "/" 

def connect_to_mongodb():
    return pymongo.MongoClient(CONNECTION_STRING)

def select_db(mc : pymongo.MongoClient, dbName):
    return mc[dbName]

def select_col(db, colName):
    return db[colName]

# This main function only represents testing data
def main():
    databaseClient = connect_to_mongodb()
    print(databaseClient.list_database_names())
    inverterDB = select_db(databaseClient, "inverter")
    inverterTemperatureCol = select_col(inverterDB, "temperature")

    for i in range(5):
        inverterTemperatureData = { "displayName": "Temperatur", "category": "Inverter", "value": randint(45, 85), "unit": "°C", "timestamp": datetime.datetime.now().isoformat()}

        inverterTemperatureCol.insert_one(inverterTemperatureData)

if __name__ == "__main__":
    main()