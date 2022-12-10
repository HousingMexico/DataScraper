import mysql.connector as mysql
import env

# database class
class Database:
   
   # initialze database
   def __init__(self):

      # start mysql connection
      db = mysql.connect(
         host = env.HOST,
         user = env.USER,
         password = env.PASSWORD
      )
      return db

   # store a specific house
   def storeHouseInformation(self, house):
      print("DATABASE INSERT HOUSE")
      print(house)