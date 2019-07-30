import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="zhang785",
  database="mydatabase"
)

mycursor = mydb.cursor()

#mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")

mycursor.execute("SELECT name, address FROM customers")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)

