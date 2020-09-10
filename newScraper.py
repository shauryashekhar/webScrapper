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

if __name__ == "__main__":

    # print("Hello! This is the new script which uses the dataset package")
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="run for all websites", action="store_true")
    parser.add_argument("-w","--website", help="run for one particular website")
    parser.add_argument("-ws", "--websites", help="run for list of webistes")
    args = parser.parse_args()
    count = countArgumentsPassed(args)
    if count > 1:
        print("Please choose one of the flags available (-a, -w, -ws). Run script with '-h' flag to see how to run it")
        sys.exit(0)
    if args.all:
        print("Run for all websites")
    elif args.website:
        print("Running with " + args.website)
    elif args.websites:
        print("Running with list of websites " + args.websites)
    sys.exit(0)