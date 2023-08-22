from bson import ObjectId

from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    usim_registration_db = mongo_client["usim_registration"]
    phone_plan_collection = smartel_db["phone_plans"]
    post_paid_collection = usim_registration_db["registrations"]

    try:
        mysql_client.execute("SELECT * FROM usim_registration WHERE usim_registration.reception_status != '작성중' LIMIT 500;")
        myresult = mysql_client.fetchall()

        for result in myresult:
            phone = None
            print("phoneid: ", result["phone_id"])
            mysql_client.execute(f"SELECT * FROM partner_company where partner_company_id = {result['partner_company_id']};")
            partner_company = mysql_client.fetchone()

            phone_plan = phone_plan_collection.find_one({"phone_plan_id": result["phone_plan_id"]})
            object_id = phone_plan.get("_id")

            if(result["phone_id"] != None):
                mysql_client.execute(f"SELECT * FROM phone where phone_id = {result['phone_id']};")
                phone = mysql_client.fetchone()


            result["legacy_phone_plan_id"] = result["phone_plan_id"]
            result["phone_plan_id"] = ObjectId(object_id)
            result["phone_eid"] = result["phoneeid"]
            result["partner_company"] = partner_company["name"]
            result["phone_model"] = phone["phone_model"] if phone != None else None
            del result["partner_company_id"]
            del result["is_active"]
            del result["happycall_count"]
            del result["happycall_date"]
            del result["happycall_status"]
            del result["phoneeid"]
            del result["phone_id"]
            del result["is_prepaid"]
            del result["is_usim_claimed"]
            del result["welcome_registration_number"]
            del result["partner_request_number"]

            result["is_delivered"] = True if result["is_delivered"] == 1 else False
            result["marketing_consent"] = True if result["marketing_consent"] == 1 else False
            result["has_usim"] = True if result["has_usim"] == 1 else False
            result["is_black"] = True if result["is_black"] == 1 else False

            print(result)

            insert_res = post_paid_collection.insert_one(result)
            print(f"Inserted document IDs: {insert_res.inserted_id}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        mysql_client.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
