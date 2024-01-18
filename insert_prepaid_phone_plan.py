from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    postpaid_phone_plan_collection = smartel_db["prepaid_phone_plans"]

    try:
        mysql_client.execute("SELECT * FROM phone_plan where prepaid_postpaid = '선불';")
        myresult = mysql_client.fetchall()

        for index, result in enumerate(myresult):
            data = str(result['data'])
            voice = str(result['voice'])
            everyday = None
            del result['phone_plan_id']
            result['phone_plan_id'] = index + 1

            if '/일' in data:
                if '무제한' in voice:
                    add = voice.split('(', 1)[1].replace(")", "").strip() if '(' in voice else ''
                    result['voice'] = dict({'default': 999, 'additional': add})
                elif '/초' in voice:
                    result['voice'] = dict({'default': result['voice']})
                else:
                    result['voice'] = dict({'default': float(voice.split('분', 1)[0].strip())})

                everyday = data.split('GB/일', 1)[0]
                additional_data_speed = float(data.split('Mbps',1)[0][-1])
                result['data'] = dict({'default': 0, 'everyday': float(everyday),
                                       'additional_speed_limit': additional_data_speed})
                result['promotion_duration'] = int(result['promotion_duration']) if result['promotion_duration'] else None
                #del result['phone_plan_id']
                del result['prepaid_postpaid']
                continue

            if '무제한' in voice:
                add = voice.split('(', 1)[1].replace(")", "").strip() if '(' in voice else ''
                result['voice'] = dict({'default': 999, 'additional': add})
            elif '/초' in voice:
                result['voice'] = dict({'default': result['voice']})
            else:
                result['voice'] = dict({'default': float(voice.split('분', 1)[0].strip())})

            if 'GB' not in data:
                additional_data_speed = float(data[1].split('Mbps',1)[0][-1]) if len(data) > 1 and 'Mbps' in data[1] else None
                result['data'] = dict({'default': 0.3, 'everyday': 0, 'additional_speed_limit': additional_data_speed})
                continue

            data = str(result['data']).split('GB', 1)
            if len(data) > 1 and '매일' in data[1]:
                everyday = float(2)
            additional_data_speed = float(data[1].split('Mbps',1)[0][-1]) if len(data) > 1 and 'Mbps' in data[1] else None

            result['promotion_duration'] = int(result['promotion_duration']) if result['promotion_duration'] else None

            result['data'] = dict({'default': float(data[0]), 'everyday': everyday,
                                   'additional_speed_limit': additional_data_speed})

            #del result['phone_plan_id']
            del result['prepaid_postpaid']

        modified_data = [
            {k: v if k != 'self_activation' else v == 1 for k, v in d.items()} for d in myresult
        ]
        modified_data = [
            {k: v if k != 'self_activation_displayed' else v == 1 for k, v in d.items()} for d in modified_data
        ]
        modified_data = [
            {k: v if k != 'huhu' else v == 1 for k, v in d.items()} for d in modified_data
        ]

        result = postpaid_phone_plan_collection.insert_many(modified_data)
        print(f"Inserted document IDs: {result.inserted_ids}")

    except Exception as e:
        print(f"Mongo Error: {e}")

    finally:
        # Close the connection
        mysql_client.close()
        mongo_client.close()

if __name__ == "__main__":
    main()
