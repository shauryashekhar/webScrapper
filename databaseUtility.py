import dataset
from sqlalchemy.sql import text
from collections import defaultdict

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

def getRandomApps(db):
    queryListOfWebsites = 'SELECT DISTINCT websiteName from AppDetails'
    for row in db.query(queryListOfWebsites):
        websiteName = row['websiteName']
        print("==================================")
        print('For websiteName = ' + websiteName)
        print("==================================")
        queryRandomAppsPerWebiste = 'SELECT DISTINCT title FROM AppDetails where websiteName = "{0}" ORDER BY RANDOM() LIMIT 20'.format(websiteName)
        for innerRow in db.query(queryRandomAppsPerWebiste):
            print(innerRow['title'])
        print("==================================")
        print("==================================")

def analyzeAppsInDB(db):
    appDict = defaultdict(set)
    getAllDistinctAppsQuery = 'SELECT DISTINCT appID, websiteName from AppDetails'
    for row in db.query(getAllDistinctAppsQuery):
        appID = row['appID']
        websiteName = row['websiteName']
        if websiteName == 'apk-dl.com':
            slashPos = appID.rfind('/')
            appID = appID[slashPos+1:]
        elif websiteName == 'apkpure.com':
            slashPos = appID.rfind('/')
            appID = appID[slashPos+1:]
        elif websiteName == 'apkplz.com':
            slashPos = appID.rfind('/')
            appID = appID[slashPos+1:]
        elif websiteName == 'apktada.com':
            slashPos = appID.rfind('/')
            appID = appID[slashPos+1:]
        elif websiteName == 'm.allfreeapk.com':
            appID = appID[:-1]
            slashPos = appID.rfind('/')
            appID = appID[slashPos + 1:]
        elif websiteName == 'apkfab.com':
            slashPos = appID.rfind('/')
            appID = appID[slashPos + 1:]
        elif websiteName == 'malavida.com':
            appID = appID[:-1]
            slashPos = appID.rfind('/')
            appID = appID[slashPos + 1:]
        elif websiteName == 'apkgk.com':
            appID = appID[1:]
        
        appDict[appID].add(websiteName)
    
    countArray = [0,0,0,0,0,0,0,0,0]
    for key in appDict:
        valueSize = len(appDict[key])
        countArray[valueSize] = countArray[valueSize] + 1
    for i in range(9):
        perc = countArray[i] / len(appDict) * 100
        if i != 0:
            print('The percentage of apps found in '+ str(i) +' websites is '+ str(perc) + ' %.')
        