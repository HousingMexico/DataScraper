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
      
      # clean house details
      # this array contains a specific, unchangable order
      detailsArray = house["details"]

      # dump ALL house details
      # including name and link directly comming from the house dictionary
      details = {
         "name": house["name"],
         "link": house["link"],
         "price": house["price"],
         "size": detailsArray[0],
         "built": detailsArray[1],
         "fullbathrooms": detailsArray[2],
         "halfbathrooms": detailsArray[5],
         "parking": detailsArray[3],
         "bedrooms": detailsArray[4],
         "years": detailsArray[6]
      }

      print(details)