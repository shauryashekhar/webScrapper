import dataset



def databaseStartUp():
    db = dataset.connect("sqlite:///database.db")
    print("Database set up")
    return db

def getTable(db, tableName):
    table = db[tableName]
    print("Table returned " + table)
    return table

def insertIntoAppDetailsTable(table, details):
    row = table.find_one(details['appID'])
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
    print("insertIntoAppDetailsTable")

def insertIntoAppIdTable(table, details):

    print("insertIntoAppIdTable")

def insertIntoSugesstionsTable(table, details):

    print("insertIntoSugesstionsTable")

def updateTable():
    print("updateTable")