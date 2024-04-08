import mysql.connector

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="saketh@2002",
)

cursor = database.cursor()

cursor.execute("CREATE DATABASE marvel")
