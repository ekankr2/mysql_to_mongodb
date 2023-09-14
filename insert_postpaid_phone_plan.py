from core.database import mongo_client, mysql_client


def main():
    smartel_db = mongo_client["smartel"]
    postpaid_phone_plan_collection = smartel_db["postpaid_phone_plans"]

    try:
        mysql_client.execute("SELECT * FROM phone_plan where prepaid_postpaid = '후불';")
        myresult = mysql_client.fetchall()

        for result in myresult:
            data = str(result['data'])
            voice = str(result['voice'])
            everyday = None

            if '/일' in data:
                if '무제한' in voice:
                    add = voice.split('(', 1)[1].replace(")", "").strip() if '(' in voice else ''
                    result['voice'] = dict({'default': 999, 'additional': add})
                elif voice == '미제공':
                    result['voice'] = dict({'default': 0})
                else:
                    result['voice'] = dict({'default': float(voice.split('분', 1)[0].strip())})

                everyday = data.split('GB/일', 1)[0]
                additional_data_speed = float(data.split('Mbps',1)[0][-1])
                result['data'] = dict({'default': 0, 'everyday': float(everyday),
                                       'additional_speed_limit': additional_data_speed})
                result['promotion_duration'] = int(result['promotion_duration']) if result['promotion_duration'] else None
                # del result['phone_plan_id']
                del result['daily_deduction']
                del result['prepaid_postpaid']
                del result['prepaid_type']
                continue

            if '무제한' in voice:
                add = voice.split('(', 1)[1].replace(")", "").strip() if '(' in voice else ''
                result['voice'] = dict({'default': 999, 'additional': add})
            elif voice == '미제공':
                result['voice'] = dict({'default': 0})
            else:
                result['voice'] = dict({'default': float(voice.split('분', 1)[0].strip())})
            data = str(result['data']).split('GB', 1)
            if len(data) > 1 and '매일' in data[1]:
                everyday = float(2)
            additional_data_speed = float(data[1].split('Mbps',1)[0][-1]) if len(data) > 1 and 'Mbps' in data[1] else None

            result['promotion_duration'] = int(result['promotion_duration']) if result['promotion_duration'] else None

            result['data'] = dict({'default': float(data[0]), 'everyday': everyday,
                                   'additional_speed_limit': additional_data_speed})

            # del result['phone_plan_id']
            del result['daily_deduction']
            del result['prepaid_postpaid']
            del result['prepaid_type']

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
