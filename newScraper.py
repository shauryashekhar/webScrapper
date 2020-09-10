import requests
import time
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from databaseUtility import *
from parserUtility import *
import json
import sqlite3
from sqlite3 import Error
from queue import Queue 
import sys
import dataset
import argparse

database = ""

def countArgumentsPassed(args):
    count = 0
    if args.all:
        count = count + 1
    if args.website:
        count = count + 1
    if args.websites:
        count = count + 1
    return count

termsList = []
finalTermsList = []

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
    print("Number of elements being searched for ")
    print(len(finalTermsList))
    q = Queue()
    wordSet = set()
    for term in finalTermsList:
        if(term != ""):
            wordSet.add(term)
    for word in wordSet:
        q.put(word)
    print("Queue size is initially ")
    print(q.qsize())
    return q

def runAllSupportedWebsites(termsQueue):
    db = databaseStartUp()
    apksupport(db, termsQueue)
    print("Finished Processing for all supported websites")

def runSingleWebsite(website):
    print("")

def runWebsiteList(websites):
    print("")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="run for all websites", action="store_true")
    parser.add_argument("-w","--website", help="run for one particular website")
    parser.add_argument("-ws", "--websites", help="run for list of webistes")
    args = parser.parse_args()
    count = countArgumentsPassed(args)
    if count > 1:
        print("Please choose one of the flags available (-a, -w, -ws). Run script with '-h' flag to see how to run it")
        sys.exit(0)
    elif count == 1:
        termsQueue = readTermsAndCreateQueue()
        if args.all:
            print("Run for all websites")
            runAllSupportedWebsites(termsQueue)
        elif args.website:
            print("Running with " + args.website)
            runSingleWebsite(args.website)
        elif args.websites:
            print("Running with list of websites " + args.websites)
            runWebsiteList(args.websites)
    elif count == 0:
        print("No args passed. Defaulting to all websites")
        runAllSupportedWebsites()
    sys.exit(0)