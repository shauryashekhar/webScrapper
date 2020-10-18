import requests
import time
from bs4 import BeautifulSoup
import csv
from collections import defaultdict
from databaseUtility import *
from parserUtility import *
from utility import *
import json
import sqlite3
from sqlite3 import Error
from queue import Queue 
import sys
import dataset
import argparse

def countArgumentsPassed(args):
    count = 0
    if args.all:
        count = count + 1
    if args.website:
        count = count + 1
    if args.websites:
        count = count + 1
    if args.statistics:
        count = count + 1
    if args.supportedWebsites:
        count = count + 1
    return count

def runAllSupportedWebsites(termsQueue):
    db = databaseStartUp()
    # apksupport(db, termsQueue)
    # apkdl(db, termsQueue)
    # apkpure(db, termsQueue)
    # apkplz(db, termsQueue)
    # apktada(db, termsQueue)
    # allfreeapk(db, termsQueue)
    # apkfab(db, termsQueue)
    malavida(db, termsQueue)
    # apkgk(db, termsQueue)
    print("Finished Processing for all supported websites")

# dispatcher = {
#     'apksupport': apksupportTest()
# }

def runSingleWebsite(website, termsQueue):
    db = databaseStartUp()
    try:
        dispatcher[website](db, termsQueue)
    except:
        return "Invalid website name"
    print("Came inside single website")

def runWebsiteList(websites, termsQueue):
    db = databaseStartUp()
    print("Came inside run website list")

def getStatistics():
    db = databaseStartUp()
    getStats(db)

def listSupportedWebsites():
    print("The following websites are currently supported!")
    for k, v in dispatcher.items():
        print(k)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="run for all websites", action="store_true")
    parser.add_argument("-w","--website", help="run for one particular website")
    parser.add_argument("-ws", "--websites", help="run for list of webistes")
    parser.add_argument("-s", "--statistics", help="get statistics", action="store_true")
    parser.add_argument("-sw", "--supportedWebsites", help="list supported websites", action="store_true")
    args = parser.parse_args()
    count = countArgumentsPassed(args)
    if count > 1:
        print("Please choose one of the flags available (-a, -w, -ws). Run script with '-h' flag to see how to run it")
        sys.exit(0)
    elif count == 1:
        if args.all:
            termsQueue = readTermsAndCreateQueue()
            print("Run for all websites")
            runAllSupportedWebsites(termsQueue)
        elif args.website:
            termsQueue = readTermsAndCreateQueue()
            print("Running with " + args.website)
            runSingleWebsite(args.website, termsQueue)
        elif args.websites:
            termsQueue = readTermsAndCreateQueue()
            print("Running with list of websites " + args.websites)
            runWebsiteList(args.websites, termsQueue)
        elif args.statistics:
            print("Calling statistics")
            getStatistics()
        elif args.supportedWebsites:
            print("Listing supported websites")
            listSupportedWebsites()
    elif count == 0:
        print("No args passed. Defaulting to all websites")
        termsQueue = readTermsAndCreateQueue()
        runAllSupportedWebsites(termsQueue)
    sys.exit(0)