import mysql.connector as mysql
import env

# database class


class Database:

    # initialze database
    def __init__(self):

        # start mysql connection
        db = mysql.connect(
            host=env.HOST,
            user=env.USER,
            password=env.PASSWORD,
            database=env.DATABASE
        )

        if (db.is_connected()):
            print("DATABASE IS CONNECTED")
        else:
            print("DATABASE CONNECTION UNSUCCESSFUL")

        self.db = db
        self.cursor = db.cursor()

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

        # prepare SQL statement
        SQL = (
            "INSERT INTO houses(name, link, price, size, built, fullbathrooms, halfbathrooms, parking, bedrooms, years)"
            "VALUES (NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''), NULLIF(%s, ''))"
        )
        DATA = (details["name"], details["link"], details["price"], details["size"], details["built"],
                details["fullbathrooms"], details["halfbathrooms"], details["parking"], details["bedrooms"], details["years"])

        # on Mongoose, this is new Schema()
        self.cursor.execute(SQL, DATA)

        # on Mongoose, this is data.save()
        self.db.commit()

        print("[DATABASE] Value has been saved")
