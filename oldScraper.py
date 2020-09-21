import requests
import time
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
import json
import sqlite3
from sqlite3 import Error
from queue import Queue 
import sys

terms_list = []
appDictionary = {}
relatedSearchTerms = {}
finalTermsList = []

# Formatting Functions

def commaSeparated(term):
    result = ""
    if len(term.split(' ')) > 1:
        count = len(term.split(' '))
        i = 0
        for word in term.split(' '):
            if i > 0:
                result = result + "+"
            result = result + word
            i = i + 1
        return result
    else:
        return term

# Read Input Terms

def readTerms():
    with open('android_terms.csv','rt')as f:
        data = csv.reader(f)
        lineNumber = 0
        for row in data:
                if lineNumber >= 1:
                    key = row[2]
                    terms = row[3]
                    i = 0
                    for term in terms.split('"'):
                        if i%2 == 0:
                            i = i+1
                            continue
                        else:
                            i = i+1
                            terms_list.append(term)
                else:
                    lineNumber = lineNumber + 1

#Database Functions

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
            
            
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def databaseStartUp(websiteName):
    # Create connection
    # databaseName = websiteName + ".db"
    databaseName = "C:\\Users\\USER\\Desktop\\ScrapperProject\\webScrapper\\test.db"
    conn = create_connection(databaseName)

    # Create table
    if conn is not None:

        sql_create_appDetailsMainTable_table = """ CREATE TABLE IF NOT EXISTS appDetailsMainTable (
                                        key text NOT NULL,
                                        appIDs text NOT NULL,
                                        relatedSearchTerms text,
                                        source text NOT NULL
                                    ); """

        sql_create_appDetails_table = """ CREATE TABLE IF NOT EXISTS appDetails (   
                                        appID text NOT NULL,
                                        title text NOT NULL,
                                        description text,
                                        stars text,
                                        imageSource text,
                                        developerName text,
                                        source text
                                    ); """

        sql_create_relatedSearchTerms_table = """ CREATE TABLE IF NOT EXISTS relatedSearchTerms (
                                        keyTerm text PRIMARY KEY,
                                        terms text NOT NULL,
                                        source text
                                    ); """


        create_table(conn, sql_create_appDetailsMainTable_table)
        create_table(conn, sql_create_appDetails_table)
        create_table(conn, sql_create_relatedSearchTerms_table)
        print("Database created!")
    else:
        print("Error! cannot create the database connection.")
    
    return conn
    
#Class to store app details in object format
class AppDetails:
    def __init__(self, title, description, stars, appID, imageSource, developerName):
        self.title = title
        self.description = description
        self.stars = stars
        self.appID = appID
        self.imageSource = imageSource
        self.developerName = developerName
        
    def toString(application):
        return application.title + ", " + application.appID + ", " + application.description + ", " + application.stars + ", " + application.imageSource + ", " + application.developerName
        
        
def insertIntoAppDetailsMainTable(conn, task):
 
    sql = ''' INSERT INTO appDetailsMainTable(key,appIDs,relatedSearchTerms,source)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def insertIntoAppDetails(conn, task):
 
    sql = ''' INSERT INTO appDetails(appID, title, description, stars, imageSource, developerName, source)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def apksupport():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        payload = {'q': word, 't': 'app'}
        r = requests.get('https://apk.support/search', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Get App Names
        names_table = soup.find_all("div", attrs={"class": "it_column"})
        if(len(names_table) == 0):
            continue
        finalList = []
        appIDList = ""
        first = 0
        for name in names_table:
            # Developer Information
            developerPart = name.find_all("div", attrs={"class": "ss_tg"})
            developerPart = developerPart[0].find_all("a")
            developerTag = developerPart[0]['href']
            developerTag = developerTag[10:]
            developerName = developerPart[0].get_text()
            information = name.find_all("a")
            # Title
            titleTag = information[0].find_all("h3")
            title = titleTag[0].get_text()
            # Description
            descriptionTag = information[0].find_all("p")
            description = descriptionTag[0].get_text()
            # Stars
            starsTag = information[0].find_all("div", attrs = {"class" : "stars"})
            starsSpan = starsTag[0].find_all("span")
            stars = starsSpan[0]['title']
            starCount = stars[stars.rindex(' ')+1:]
            # AppID
            appID = information[0]['href']
            appID = appID[4 : ]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            # Image Source Link
            imageTag = information[0].find_all("div", attrs={"class" : "seo_img"})
            imageTag = imageTag[0].find_all("img")
            imageSource = imageTag[0]['data-original']
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, stars, imageSource, developerName, 'apk.support')
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
            
        # Suggestion Addition
        suggestionList = soup.find_all("div", attrs={"class": "suggest"})
        suggestionList = suggestionList[0].find_all("li")
        suggestions = []
        suggestionsString = ""
        i = 0
        for suggestion in suggestionList:
            suggestionName = suggestion.get_text()
            if (i != 0):
                suggestionsString = suggestionsString + ","
            suggestionsString = suggestionsString + suggestionName
            i = 1
            suggestions.append(suggestionName)
            modifiedSuggestionName = commaSeparated(suggestionName)
            if(modifiedSuggestionName not in wordSet):
                wordSet.add(modifiedSuggestionName)
                q.put(modifiedSuggestionName)
        
        #Insert Into Main Table
        taskMainTable = (word, appIDList, suggestionsString, 'apk.support')
        insertIntoAppDetailsMainTable(conn, taskMainTable)
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

def apkdl():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        print("Starting " + word + " " + str(numberOfTerms) + " with queue length " + str(q.qsize()))
        payload = {'q': word}
        payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
        r = requests.get('https://apk-dl.com/search', params=payload_str)
        soup = BeautifulSoup(r.text, 'html.parser')
        names_table = soup.find_all("div", attrs={"class": "card no-rationale square-cover apps small"})
        appIDList = ""
        first = 0
        for name in names_table:
            appIDPart = name.find("a", attrs={"class": "card-click-target"})
            appID = appIDPart['href']
            imageLinkPart = name.find("img", attrs={"class": "cover-image lazy"})
            imageLink = imageLinkPart['data-original']
            titlePart = name.find("a", attrs={"class": "title"})
            title = titlePart.get_text()
            developerNamePart = name.find("a", attrs={"class": "subtitle"})
            developerName = developerNamePart.get_text()
            starsPart = name.find("div", attrs={"class" : "current-rating"})
            stars = starsPart['style']
            stars = stars.rsplit(' ', 1)[1]
            stars = stars[:-2]
            stars = int(stars)/10
            
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1

            appTableEntry = (appID, title, 'null', stars, imageLink, developerName, 'apk-dl.com')
            insertIntoAppDetails(conn, appTableEntry)
        
        appMainTableEntry = (word, appIDList, 'null', 'apk-dl.com')
        insertIntoAppDetailsMainTable(conn, appMainTableEntry)
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break
        
def apkpure():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        checkMore = 1
        firstCheck = 1
        interval = 0
        appIDList = ""
        first = 0
        while(checkMore):
            if(firstCheck == 0):
                interval = interval + 15
            payload = {'q': word,  't': 'app', 'begin': interval}
            payload_str = "&".join("%s=%s" % (k,v) for k,v in payload.items())
            r = requests.get('https://apkpure.com/search-page', params=payload_str)
            soup = BeautifulSoup(r.text, 'html.parser')
            names_table = soup.find_all("dl", attrs={"class": "search-dl"})
            if(len(names_table) == 0):
                print("Skipping " + word)
                break
            for name in names_table:
                dtPart = name.find_all("dt")
                ddPart = name.find_all("dd")
                aPart = dtPart[0].find_all("a")
                appID = aPart[0]['href']
                imagePart = aPart[0].find_all("img")
                imageLink = imagePart[0]['src']
                titlePart = ddPart[0].find_all("p", attrs={"class": "search-title"})
                title = titlePart[0].find("a").get_text()
                starsPart = ddPart[0].find_all("span", attrs={"class": "score"})
                stars = starsPart[0]['title']
                stars = stars.rsplit(' ', 1)[1]
                pParts = ddPart[0].find_all("p")
                developerPart = pParts[1].find_all("a")
                developerName = developerPart[0].get_text()
                if first != 0:
                    appIDList = appIDList + ","
                appIDList = appIDList + appID
                first = 1
                
                appTableEntry = (appID, title, 'null', stars, imageLink, developerName, 'apkpure.com')
                insertIntoAppDetails(conn, appTableEntry)
            firstCheck = 0
            if(len(names_table) == 0):
                checkMore = 0
        appMainTableEntry = (word, appIDList, 'null', 'apkpure.com')

        insertIntoAppDetailsMainTable(conn, appMainTableEntry)
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

def apkplz():
    numberOfTerms = 0
    while(q.empty() != True):
        print(q.qsize())
        word = q.get()
        time.sleep(1)
        payload = {'q': word}
        r = requests.get('https://apkplz.net/search?', params=payload);
        soup = BeautifulSoup(r.text, 'html.parser');
        appList = soup.find_all("div", attrs={"class":"section row nop-sm"})
        appList = appList[0].find_all("div",attrs={"class":"row itemapp"});
        finalList = []
        appIDList = ""
        first = 0
        for app in appList:
            appDetails  = app.find_all("div",attrs={"class" : "col-md-12 col-sm-9 vcenter apptitle"}) 
            title = appDetails[0].find_all("a")
            title = title[0]['title']
            starCount = "NULL"
            description = "NULL"
            developerName = "NULL"
            imageSource = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            imageSource = imageSource[0].find_all("img");
            imageSource = imageSource[0]["data-original"];
            appID = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            appID = appID[0].find_all("a")
            appID = appID[0]["href"]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'apkplz.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'apkplz.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
    
def apktada():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        payload = {'q': word};
        print(payload)
        r = requests.get('https://apktada.com/search?', params=payload);
        print(r)
        soup = BeautifulSoup(r.text, 'html.parser');
        appList = soup.find_all("div", attrs={"class":"section row nop-sm"})
        appList = appList[0].find_all("div",attrs={"class":"row itemapp"});
        finalList = []
        appIDList = ""
        first = 0
        for app in appList:
            appDetails  = app.find_all("div",attrs={"class" : "col-md-12 col-sm-9 vcenter apptitle"}) 
            title = appDetails[0].find_all("a")
            title = title[0]['title']
            starCount = "NULL"
            description = "NULL"
            developerName = "NULL"
            imageSource = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            imageSource = imageSource[0].find_all("img");
            imageSource = imageSource[0]["data-original"];
            appID = app.find_all("div",attrs={"class" : "col-md-12 col-sm-3 vcenter"}) 
            appID = appID[0].find_all("a")
            appID = appID[0]["href"]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'apktada.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'apktada.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
        

def allfreeapk():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        payload = {'q': word};
        print(payload)
        r = requests.get('https://m.allfreeapk.com/search.html?', params=payload);
        print(r)
        soup = BeautifulSoup(r.text, 'html.parser');
        appList = soup.find_all("div", attrs={"class":"list"})
        appList = appList[0].find_all("li");
        finalList = []
        appIDList = ""
        first = 0
        for app in appList:
            appDetails  = app.find_all("div",attrs={"class":"l"}) 
            title =  app.find_all("div",attrs={"class":"r"}) 
            title = title[0].find_all("a")
            title = title[0].get_text()
            starCount = "NULL"
            description = "NULL"
            developerName = "NULL"
            imageSource = appDetails[0].find_all("img")
            imageSource = imageSource[0]["data-original"]
            appID = appDetails[0].find_all("a")
            appID = appID[0]["href"]
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'm.allfreeapk.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'm.allfreeapk.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
        
def apkfab():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        payload = {'q': word};
        r = requests.get('https://apkfab.com/search', params=payload);
        soup = BeautifulSoup(r.text, 'html.parser');
        appList = soup.find_all("div", attrs={"class":'list'})
        finalList = []
        appIDList = ""
        first = 0
        for app in appList:
            title = app.find_all("div",attrs={"class":"title"})
            if(len(title)  < 1):
                continue
            title = title[0].get_text()
            rating = app.find_all("span", attrs={"class":"rating"})
            starCount = rating[0].get_text()
            description = "NULL"
            developerName = "NULL"
            imageSource = app.find_all("img")
            imageSource  = imageSource[0]['data-src']
            appID = app.find_all("a")
            appID = appID[0]['href']
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'apkfab.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'apkfab.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
            
def malavida():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        word = word.replace('+','-')
        r = requests.get('https://www.malavida.com/en/s/'+word);
        soup = BeautifulSoup(r.text, 'html.parser');
        appDetails = soup.find_all("section", attrs={"class":'app-list'})
        appList = soup.find_all("section", attrs={"class":'app-download'})
        counter = 0
        finalList = []
        appIDList = ""
        first = 0
        notFound = soup.find_all("section", attrs={"class":'not-found'})
        if(len(notFound)>0):
            continue
        for app in appList:
            appSrc = app.find_all("div", attrs={"class":"title"})
            appDesc = app.find_all("p")
            imageSource = app.find_all('img')
            imageSource = imageSource[0]['src']
            appLink = appSrc[0].find_all("a")
            appID = appLink[0]['href']
            title = appLink[0].get_text()
            description = appDesc[0].get_text()
            counter = counter+1
            
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            starCount = "NULL"
            developerName = "NULL"
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'malavida.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
            counter=counter+1
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'malavida.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
        

def apkgk():
    numberOfTerms = 0
    while(q.empty() != True):
        word = q.get()
        time.sleep(1)
        payload = {'keyword': word}
        r = requests.get('https://apkgk.com/search/', params=payload);
        soup = BeautifulSoup(r.text, 'html.parser');
        appId = soup.find_all("ul", attrs={"class":'topic-wrap'})
        if(len(appId) == 0):
            print("Skipping " + word)
            continue
        appId = appId[0].find_all("a")
        names_table = soup.find_all('div', attrs={"class":'topic-bg'})
        if(len(names_table) == 0):
            print("Skipping " + word)
            continue
        finalList = []
        appIDList = ""
        first = 0
        counter = 0
        for name in names_table:
            appName = name.find_all("div", attrs={"class": "topic-tip-name"})
            appDesc = name.find_all("div", attrs={"class": "topic-tip-description"})
            appSrcMain  = name.find_all("div", attrs={"class": "c-lz-load"})
            imageTag = appSrcMain[0].find_all("img")
            appLink = imageTag[0]['data-src']
            
            appID = appId[counter]['href']
            if first != 0:
                appIDList = appIDList + ","
            appIDList = appIDList + appID
            first = 1
            imageSource = appLink
            description = appDesc[0].get_text()
            title = appName[0].get_text()
            starCount = "NULL"
            developerName = "NULL"
            perAppObject = AppDetails(title, description, starCount, appID, imageSource, developerName)
            
            # Insert Into App Table
            taskAppTable = (appID, title, description, starCount, imageSource, developerName, 'apkgk.com');
            insertIntoAppDetails(conn, taskAppTable)
            
            finalList.append(perAppObject)
            counter=counter+1
        #Insert Into Main Table
        suggestionsString = "NULL"
        taskMainTable = (word, appIDList, suggestionsString, 'apkgk.com');
        insertIntoAppDetailsMainTable(conn, taskMainTable)
        
        
if __name__ == "__main__":

    n = len(sys.argv)
    if(n != 2):
        print("Incorrect usage: Please pass in the website you would like to scrape")
        sys.exit(0)
    
    currentWebsiteName = sys.argv[1]

    supportedWebsites = {"https://apkpure.com", "https://apk-dl.com", "https://apk.support", "https://apkplz.net", "https://apktada.com", "https://m.allfreeapk.com", "https://apkfab.com", "https://www.malavida.com", "https://apkgk.com/"}

    if currentWebsiteName not in supportedWebsites:
        print("The website you entered " + currentWebsiteName + " is not currently supported")
    else :
        print("Starting processing for " + currentWebsiteName)

    # STARTUP STUFF
    readTerms()
    conn = databaseStartUp(currentWebsiteName)

    print("Database set up...")

    # CLEAN INPUT SEARCH TERMS
    for term in terms_list:
        result = commaSeparated(term)
        finalTermsList.append(result)
    print("Number of elements being searched for ")
    print(len(finalTermsList))

    # CREATION OF QUEUE
    q = Queue()
    wordSet = set()
    for term in finalTermsList:
        if(term != ""):
            wordSet.add(term)
    for word in wordSet:
        q.put(word)
    print("Queue size is initially ")
    print(q.qsize())

    if(currentWebsiteName == "https://apk-dl.com"):
        apkdl()
    elif(currentWebsiteName == "https://apkpure.com"):
        apkpure()
    elif(currentWebsiteName == "https://apk.support"):
        apksupport()
    elif(currentWebsiteName == "https://apkplz.net"):
        apkplz()
    elif(currentWebsiteName == "https://apktada.com"):
        apktada()
    elif(currentWebsiteName == "https://m.allfreeapk.com"):
        allfreeapk()
    elif(currentWebsiteName == "https://apkfab.com"):
        apkfab()
    elif(currentWebsiteName == "https://www.malavida.com"):
        malavida()
    elif(currentWebsiteName == "https://apkgk.com"):
        apkgk()

    print("Task completed...")
    sys.exit(0)
