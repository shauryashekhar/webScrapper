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

db = databaseStartUp()
termsQueue = readTermsAndCreateQueue()

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

def runAllSupportedWebsites():
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

dispatcher = {
    'apksupport': apksupportTest,
    'apkdl': apkdlTest,
    'apkpure': apkpure,
    'apkplz': apkplz,
    'apktada': apktada,
    'allfreeapk': allfreeapk,
    'apkfab': apkfab,
    'malavida': malavida,
    'apkgk': apkgk 
}

def runSingleWebsite(website):
    print("Came inside single website")
    try:
        dispatcher[website](db, termsQueue)
    except:
        print("Invalid website name passed into function ->" + website)

def runWebsiteList(websites):
    print("Came inside run website list")
    websiteList = websites.split(",")
    for website in websiteList:
        runSingleWebsite(website)

def getStatistics():
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
            print("Run for all websites from main")
            runAllSupportedWebsites()
        elif args.website:
            print("Running from main with " + args.website)
            runSingleWebsite(args.website)
        elif args.websites:
            print("Running from main with list of websites " + args.websites)
            runWebsiteList(args.websites)
        elif args.statistics:
            print("Calling statistics")
            getStatistics()
        elif args.supportedWebsites:
            print("Listing supported websites")
            listSupportedWebsites()
    elif count == 0:
        print("No args passed. Defaulting to all websites")
        runAllSupportedWebsites()
    sys.exit(0)