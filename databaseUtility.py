import dataset



def databaseStartUp():
    db = dataset.connect("sqlite:///database.db")
    print("Database set up")
    return db

def createTable(db, tableName):
    table = db[tableName]
    print("Table returned " + table)
    return table

def insertIntoTable():
    print("insertIntoTable")