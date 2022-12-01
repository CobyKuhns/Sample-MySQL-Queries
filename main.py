##############################################################
# MySQLTesting                                               #
# This is script that runs through some basic MySQL          #
# commands, to prove experience with Python and MySQL.       #
#                                                            #
##############################################################

#We start by importing a library to connect to a MySQL server
#and a library to hide our password when we enter it in the console

#We also are importing the CSV library to parse through a list of entries
#to add to our server

from getpass import getpass
from mysql.connector import connect, Error
import csv
#Then, we parse through our csv to prepare our list of entries
def main():

    gameList = parseCSV()
    #Next, we get the input from our user and attempt to connect to the server
    try:
        with connect(
            host= input("Hostname: "),
            user= input("Username: "),
            password= getpass("Password: "),
        ) as connection:
            #assuming we're successful, we create a cursor and then start excuting our queries
            cursor = connection.cursor()
            databaseName = input("Please input a name for the new database: ")
            cursor.execute("CREATE DATABASE " + databaseName)
            #After creating the new database, we get a list of all the databases in the server,
            #then print that list to the console
            cursor.execute("show databases")
            for db in cursor:
                print(db)
            # Next, we create a table in the new database, then add some random entries to it
            create_table_query = """
            CREATE TABLE {}.games (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100),
                release_year YEAR(4),
                series VARCHAR(100)
            )
            """.format(databaseName)
            cursor.execute(create_table_query)
            for entry in gameList:
                add_query = """
                INSERT INTO {}.games (title, release_year, series)
                VALUE (\"{}\", {}, "{}\")""".format(databaseName,entry[0],entry[1],entry[2])
                cursor.execute(add_query)
            connection.commit()
            #Showing all entries in games table
            cursor.execute("SELECT * FROM {}.games".format(databaseName))
            print("\nAll Entries:")
            for entry in cursor:
                print(entry)
            #Querying for entries with Series= Super Mario
            cursor.execute("SELECT * FROM {}.games WHERE series= \"Super Mario\"".format(databaseName))
            print("\nEntries in the Super Mario series: ")
            for entry in cursor:
                print(entry)
            #Querying for entries released in 1996
            cursor.execute("SELECT * FROM {}.games WHERE release_year= 1996".format(databaseName))
            print("\nEntries released in 1996: ")
            for entry in cursor:
                print(entry)
            #Removing entries from 2002
            print("Removing Entries from 2002...")
            cursor.execute("DELETE FROM {}.games WHERE release_year= 2002".format(databaseName))
            connection.commit()
            #Print out updated list
            cursor.execute("SELECT * FROM {}.games".format(databaseName))
            print("Updated List:")
            for entry in cursor:
                print(entry)


    except Error as e:
        print(e)

def parseCSV():
    gameEntries = []
    gameEntry = []
    with open('gameList.csv', 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            gameEntry = []
            for column in row:
                gameEntry.append(column)
            gameEntries.append(gameEntry)
        gameEntries.pop(0)
        print(gameEntries)
    return gameEntries

if __name__ == "__main__":
    main()