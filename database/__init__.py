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
      
      if (db.is_connected()):
         print("DATABASE IS CONNECTED")
      else:
         print("DATABASE CONNECTION UNSUCCESSFUL")


   # store a specific house
   # "house" parameter is a dictionary containing link and name
   def storeHouseInformation(self, house):
      
      # clean house details
      # this dictionary contains housing relevant data
      # bedrooms? parking lot? construction size?
      detailsDict = house["details"]

      # dump ALL house details
      # including name and link directly comming from the house dictionary
      details = {
         "name": house["name"],
         "link": house["link"],
         "price": house["price"],
         "size": detailsDict["size"],
         "built": detailsDict["built"],
         "fullbathrooms": detailsDict["fullbathrooms"],
         "halfbathrooms": detailsDict["halfbathrooms"],
         "parking": detailsDict["parking"],
         "bedrooms": detailsDict["bedrooms"],
         "years": detailsDict["years"]
      }

      print(details)