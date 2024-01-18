from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    partner_collection = smartel_db["partners"]

    try:
        mysql_client.execute("SELECT * FROM partner_company;")
        myresult = mysql_client.fetchall()

        for result in myresult:
            result["partner_id"] = result["partner_company_id"]
            del result["partner_company_id"]
            del result["login_id"]
            del result["password"]
            del result["authority"]

        mongo_res = partner_collection.insert_many(myresult)
        print(f"Inserted document IDs: {mongo_res.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        mysql_client.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
