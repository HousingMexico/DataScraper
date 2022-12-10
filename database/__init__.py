import mysql.connector as mysql
import env

# initialize database
def load_database():
   
   # start mysql connection
   db = mysql.connect(
      host = env.HOST,
      user = env.USER,
      password = env.PASSWORD
   )

   print(db)

   # return database instance
   return db