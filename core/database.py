import mysql.connector
from pymongo import MongoClient
import certifi

from core.config import settings


mysql_connect = mysql.connector.connect(
    host=settings.MYSQL_HOST,
    database=settings.MYSQL_DATABASE,
    user=settings.MYSQL_USER,
    password=settings.MYSQL_PASSWORD
)
mysql_client = mysql_connect.cursor(dictionary=True)

mongo_client = MongoClient(settings.MONGO_URI, tlsCAFile=certifi.where())
