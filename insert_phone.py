from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    phone_collection = smartel_db["phone_models"]

    try:
        mysql_client.execute("SELECT * FROM phone;")
        myresult = mysql_client.fetchall()

        modified_data = [
            {k: v for k, v in d.items() if k != 'phone_id'} for d in myresult
        ]

        result = phone_collection.insert_many(modified_data)
        print(f"Inserted document IDs: {result.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        mongo_client.close()
        mysql_client.close()

if __name__ == "__main__":
    main()
