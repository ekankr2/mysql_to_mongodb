import mysql.connector

mysqldb = mysql.connector.connect(
    host="localhost",
    database="database",
    user="admin",
    password="password"
)

mycursor = mysqldb.cursor(dictionary=True)
mycursor.execute("SELECT * FROM phone_plan;")
myresult = mycursor.fetchall()

# you can modify data like this
modified_data = [{k: v for k, v in d.items() if k != 'table_id'} for d in myresult]

print(modified_data)

print(myresult)
