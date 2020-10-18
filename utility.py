import csv
from queue import Queue

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

def readTermsAndCreateQueue():
    termsList = []
    finalTermsList = []
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
                            termsList.append(term)
                else:
                    lineNumber = lineNumber + 1
    for term in termsList:
        result = commaSeparated(term)
        finalTermsList.append(result)
    # print("Number of elements being searched for " + str(len(finalTermsList)))
    q = Queue()
    wordSet = set()
    for term in finalTermsList:
        if(term != ""):
            wordSet.add(term)
    for word in wordSet:
        q.put(word)
    # print("Queue size is initially " + str(q.qsize()))
    return q