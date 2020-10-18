import dataset
from sqlalchemy.sql import text


def databaseStartUp():
    db = dataset.connect("sqlite:///database.db")
    print("Database set up")
    return db

def getTable(db, tableName):
    table = db[tableName]
    return table

def insertIntoAppDetailsTable(table, details):
    row = table.find_one(appID = details['appID'])
    if row == None:
        # First time entry hence, insert
        table.insert(details)
    else:
        # Else see if there are changes, if there are, update the same tuple
        for key in details.keys():
            if key != 'createdAt':
                if row[key] == details[key]:
                    continue
                else:
                    table.insert(details)
                    break


def insertIntoAppIdTable(table, details):
    row = table.find_one(word = details['word'])
    if row == None:
        # First time entry hence, insert
        table.insert(details)
    else:
        # Else see if there are changes, if there are, update the same tuple
        for key in details.keys():
            if key != 'createdAt':
                if row[key] == details[key]:
                    continue
                else:
                    table.insert(details)
                    break

def insertIntoSugesstionsTable(table, details):
    row = table.find_one(word = details['word'])
    if row == None:
        # First time entry hence, insert
        table.insert(details)
    else:
        # Else see if there are changes, if there are, update the same tuple
        for key in details.keys():
            if key != 'currentTime' and row[key] == details[key]:
                continue
            else:
                table.insert(details)
    print("insertIntoSugesstionsTable")

def getStats(db):
    statement = 'SELECT websiteName, COUNT(DISTINCT appID) c from AppDetails GROUP BY websiteName ORDER BY COUNT(DISTINCT appID)'
    print('The statistics of AppDetails are:')
    print("==================================")
    print("{:<20} {:<10}".format("Website Name", "Unique Apps"))
    print("==================================")
    for row in db.query(statement):
        websiteName = row['websiteName']
        elementCount = row['c']
        print("{:<20} {:<10}".format(websiteName, elementCount))