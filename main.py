from core.database import mysql_client

mysql_client.execute("SELECT * FROM usim_registration where usim_registration.reception_status != '작성중' LIMIT 10;")
myresult = mysql_client.fetchall()

for result in myresult:
    print(result)

# you can modify data like this
modified_data = [{k: v for k, v in d.items() if k != 'table_id'} for d in myresult]

# print(modified_data)

# print(myresult)
