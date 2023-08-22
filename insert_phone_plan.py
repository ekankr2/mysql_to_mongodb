from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    phone_plan_collection = smartel_db["phone_plans"]

    try:
        mysql_client.execute("SELECT * FROM phone_plan;")
        myresult = mysql_client.fetchall()

        # modified_data = [
        #     {k: v for k, v in d.items() if k != 'phone_plan_id'} for d in myresult
        # ]
        modified_data = [
            {k: v if k != 'self_activation' else v == 1 for k, v in d.items()} for d in myresult
        ]
        modified_data = [
            {k: v if k != 'self_activation_displayed' else v == 1 for k, v in d.items()} for d in modified_data
        ]
        modified_data = [
            {k: v if k != 'huhu' else v == 1 for k, v in d.items()} for d in modified_data
        ]

        result = phone_plan_collection.insert_many(modified_data)
        print(f"Inserted document IDs: {result.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        mysql_client.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
