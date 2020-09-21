from databaseUtility import *
from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup

def apksupport(db, q):
    numberOfTerms = 0
    while(q.empty() != True):
        time.sleep(1)
        payload = {'q': word, 't': 'app'}
        r = requests.get('https://apk.support/search', params=payload)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Get App Names
        names_table = soup.find_all("div", attrs={"class": "it_column"})
        # Time
        currentTime = datetime.now()
        if(len(names_table) == 0):
            continue
        appIDList = ""
        first = 0
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'ApksupportAppDetails')
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

            # Insert Into AppDetails Table (one per app)
            appDetailsTableEntry = (appID, title, description, stars, imageSource, developerName, 'apk.support', currentTime)
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, description=description, stars=stars, imageSource=imageSource, developerName=developerName, websiteName='apk.support', createdAt=currentTime))

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

        # Create appIdTable & suggestionTable in DB
        appIdTable = getTable(db, 'ApksupportAppId')
        suggestionTable = getTable(db, 'ApksupportSuggestions')        

        # Create entries for tables
        currentTime = datetime.now()
        appIdTableEntry = (word, appIDList, 'apk.support', currentTime)
        suggestionTableEntry = (word, suggestionsString, 'apk.support', currentTime)


        # Enter into appIdTable & suggestionTable (one per word)
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk.support', createdAt = currentTime))
        insertIntoSugesstionsTable(suggestionTable, dict(word=word, relatedSearchTerms= suggestionsString, websiteName = 'apk.support', createdAt = currentTime))

        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break

def apkdl(db, q):
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
        if(len(names_table) == 0):
            continue
        appIDList = ""
        first = 0
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'ApkdlAppDetails')
        currentTime = datetime.now()
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
            insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, stars=stars, imageSource=imageLink, developerName=developerName, websiteName='apk-dl.com', createdAt=currentTime))
            print('App Entered')
        
        appIdTable = getTable(db, 'ApkdlAppId')
        appMainTableEntry = (word, appIDList, 'null', 'apk-dl.com')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apk-dl.com', createdAt = currentTime))
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
        # Create appDetailsTable in DB
        appDetailsTable = getTable(db, 'ApkpureAppDetails')
        currentTime = datetime.now()
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
                insertIntoAppDetailsTable(appDetailsTable, dict(appID=appID, title=title, stars=stars, imageSource=imageLink, developerName=developerName, websiteName='apkpure.com', createdAt=currentTime))
            firstCheck = 0
            if(len(names_table) == 0):
                checkMore = 0
        appMainTableEntry = (word, appIDList, 'null', 'apkpure.com')
        appIdTable = getTable(db, 'ApkpureAppId')
        insertIntoAppIdTable(appIdTable, dict(word=word, appIdList = appIDList, websiteName = 'apkpure.com', createdAt = currentTime))
        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break
