from databaseUtility import *
from datetime import datetime
import time

def apksupport(db, q):
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
            # Time
            currentTime = datetime.now()
            # Insert into appDetails table
            appDetailsTableEntry = (appID, title, description, stars, imageSource, developerName, 'apk.support', currentTime)
            insertIntoAppDetailsTable(table, dict(appID=appID, title=title, description=description, stars=stars, imageSource=imageSource, developerName=developerName, websiteName='apk.support', createdAt=currentTime))

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


        # Enter into appIdTable & suggestionTable

        numberOfTerms = numberOfTerms + 1
        if(numberOfTerms == 5000):
            break