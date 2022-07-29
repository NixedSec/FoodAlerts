#!/usr/bin/env python3
import requests, json, re, datetime
from sys import argv

since = ""
searchTerm = ""
base_url = "https://data.food.gov.uk/food-alerts/id"
FAver = "1.0"


def help():
    print('''FoodAlerts is a tool to output food recalls in the UK using an API from FSA.
The API provides food product recalls from January 2018 issued by the FSA.

    Search quickly from the previous month or year (-m, -y)
    Search for a phrase or from a specific date (-s, -f)
    Combine the phrase and from searches (-c)

    Rather be asked for the responses individually? Use an interactive mode (-fi, -si, -ci)


Switches:
-h: display this help message
-m: a quick find starting from the 1st of the previous month.
-y: a quick find starting from the previous year.
-f: find recalls from a specific date. Must provide date after switch "-f YYYY-MM-DD"
-fi: find the same as -f but you prefer to be asked by the program. Date is not required until asked.
-s: search for a specific term. A single word. "-s chocolate" "-s tesco" "-c peanuts".
-si: search the same as -s but you prefer to be asked by the program. Word is not required until asked.
-c: combine both find and search to narrow the query. "-c 2022-01-01 asda" "-c 2018-01-01 metal"
-ci: combine the same as -c but you prefer to be asked by the program. Word is not required until asked.
-v: display the version.''')
    

def parseFlags(flag):
    match flag:
        case "-f":
            searchFrom("")
            query("from")
        case "-fi":
            searchFrom("interactive")
            query("from")
        case "-s":
            search("")
            query("word")
        case "-si":
            search("interactive")
            query("word")
        case "-c":
            searchFrom("combine")
            search("combine")
            query("combine")
        case "-ci":
            searchFrom("interactive")
            search("interactive")
            query("combine")
        case "-m":
            timeShift("month")
            query("from")
        case "-y":
            timeShift("year")
            query("from")
        case "-h":
            help()
        case "-v":
            FAversion()
        case _:
            print ("no flag provided")

def searchFrom(mode):
    global since 
    if (mode == "interactive"):
        since += checkDate(input("Enter date to search from(YYYY-MM-DD): ").strip())

        if (since == ""):
            print ("---No date provided---\n")
    else:
        try:
            since += checkDate(argv[2].strip())
        except:
            print ("---No date provided---\n")

def search(mode):

    global searchTerm 
    if (mode == "interactive"):
        searchTerm = checkSearch(input("Enter a single word to search for: ").strip())

        if (searchTerm == ""):
            print ("---No word provided---\n")
    else:
        try:
            if (mode == "combine"):
                searchTerm += checkSearch(argv[3].strip())
            else:
                searchTerm += checkSearch(argv[2].strip())
        except:
            print ("---No word provided---\n")

def checkDate(since): #replace any forward slashes to meet criteria
        since = since.replace("/", "-")

        #date only needs to be from 2018 onwards. This should restrict to 2010, close enough.
        dateRe = re.compile("[2]{1}[0]{1}[1-9]{1}[0-9]{1}\-[0-1]{1}[0-9]{1}\-[0-3]{1}[0-9]{1}")

        if (re.match(dateRe, since)):
            return since
        else:
            print ("Date supplied is an invalid format")
            print ("Please supply a date from 2018 onwards YYYY-MM-DD")
            return ""

def checkSearch(term):
    #match a single word
    wordRe = re.compile("\A[\w-]+\Z")

    if (re.match(wordRe, term)):
        return term
    else:
        print ("---Invalid word provided---")
        return ""

def timeShift(mode):
    global since
    nowDay = str(datetime.date.today().day)
    nowMon = str(datetime.date.today().month)
    nowYear = str(datetime.date.today().year)

    if (len(nowDay) < 2):
        nowDay = "0" + nowDay

    if (len(nowMon) < 2):
        nowMon = "0" + nowMon


    if (mode == "month"):
        nowMon = str(int(nowMon) -1)
        if (len(nowMon) < 2):
            nowMon = "0" + nowMon
        since = (nowYear + "-" + nowMon + "-01")

    elif (mode == "year"):
        since = (str(int(nowYear) -1) + "-" + nowMon + "-" + nowDay)

def query(mode):
    global base_url
    global since
    global searchTerm
    url = ""
    if (mode == "from"):
        url = base_url + "?since=" + since

    elif (mode == "word"):
        url = base_url + "?search=" + searchTerm
    
    elif (mode == "combine"):
        url = base_url + "?since=" + since + "&search=" + searchTerm

    if not (url.endswith("=") | url.endswith("&")): #if either of these match, a term was not provided.
        response = requests.get(url)
        answer = json.loads(response.text)

        for i in range (len(answer['items'])):
            print('\n---Recall---   ' + answer['items'][i]['created'])
            print(answer['items'][i]['title'])
            try:
                print('REASON: ' + answer['items'][i]['problem'][0]['riskStatement'])
            except:
                print('No risk statement included')

            try:
                for j in range (len(answer['items'][i]['productDetails'])):
                    print('>> ' + answer['items'][i]['productDetails'][j]['productName'])
            except:
                print('No product details included')

def FAversion():
    global FAver
    print ("FoodAlerts: v" + FAver)

def start():
    print ('Food Alerts based on the FSA API. UK Food recalls.\n')

    try:
        parseFlags(argv[1])
    except:
        help()
        raise SystemExit

start()
