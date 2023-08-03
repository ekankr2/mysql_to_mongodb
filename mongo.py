from pymongo import MongoClient
import mysql.connector
import certifi

def main():
    mysqldb = mysql.connector.connect(
        host="localhost",
        database="database",
        user="admin",
        password="password"
    )

    client = MongoClient("<mongo_url>", tlsCAFile=certifi.where())
    db = client["db"]
    collection = db["collection"]

    try:
        mycursor = mysqldb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM phone_plan;")
        myresult = mycursor.fetchall()

        result = collection.insert_many(myresult)
        print(f"Inserted document IDs: {result.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        client.close()

if __name__ == "__main__":
    main()
