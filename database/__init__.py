import mysql.connector as mysql
import env

# database class
class Database:
   
   # initialze database
   def __init__(self):

      """ # start mysql connection
      db = mysql.connect(
         host = env.HOST,
         user = env.USER,
         password = env.PASSWORD
      )
      return db """
      print("Database hello world")

   # store a specific house
   # "house" parameter is a dictionary containing link and name
   def storeHouseInformation(self, house):
      print("DATABASE INSERT HOUSE")
      # house["link"] & house["name"]