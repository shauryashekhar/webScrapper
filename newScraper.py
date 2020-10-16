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
    return count

def runAllSupportedWebsites(termsQueue):
    db = databaseStartUp()
    # apksupport(db, termsQueue)
    # apkdl(db, termsQueue)
    # apkpure(db, termsQueue)
    apkplz(db, termsQueue)
    # apktada(db, termsQueue)
    # allfreeapk(db, termsQueue)
    # apkfab(db, termsQueue)
    # malavida(db, termsQueue)
    # apkgk(db, termsQueue)
    print("Finished Processing for all supported websites")

def runSingleWebsite(website, termsQueue):
    print("")

def runWebsiteList(websites, termsQueue):
    print("")

def getStatistics():
    db = databaseStartUp()
    getStats(db)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="run for all websites", action="store_true")
    parser.add_argument("-w","--website", help="run for one particular website")
    parser.add_argument("-ws", "--websites", help="run for list of webistes")
    parser.add_argument("-s", "--statisticss", help="get statistics", action="store_true")
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
            runSingleWebsite(args.website, termsQueue)
        elif args.websites:
            print("Running with list of websites " + args.websites)
            runWebsiteList(args.websites, termsQueue)
        elif args.stats:
            print("Add function to call statistics")
    elif count == 0:
        print("No args passed. Defaulting to all websites")
        termsQueue = readTermsAndCreateQueue()
        runAllSupportedWebsites(termsQueue)
    sys.exit(0)