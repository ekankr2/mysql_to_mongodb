from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    phone_collection = smartel_db["partners"]

    try:
        mysql_client.execute("SELECT * FROM partner_company;")
        myresult = mysql_client.fetchall()

        modified_data = [
            {k: v for k, v in d.items() if k != 'partner_company_id'} for d in myresult
        ]

        result = phone_collection.insert_many(modified_data)
        print(f"Inserted document IDs: {result.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        mysql_client.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
