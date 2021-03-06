##
##
## Searching popular apps from google play via keyword.
## Then parsing the meta data of the popular apps and
## output the meta data to file for marketing study.
##
## Author Feiwen Cheng
## Date : 2014/7/22

import urllib,urllib2
import sys
import codecs
import traceback
from bs4 import BeautifulSoup

#Get input and out files
if len(sys.argv)!=3:
	print "Usage",sys.argv[0], "appKeyWord outputFileName"
	sys.exit(2);

#Read input file
#packages = []
#with open(sys.argv[1], 'r+') as inputFile:
#	for line in inputFile:
#		packages.append(line);

#Search apps via key word from google play
searchUrl = "https://play.google.com/store/search"
searchValues = {"q" : sys.argv[1], "c" : "apps"}
searchData = urllib.urlencode(searchValues)
searchReq = urllib2.Request(searchUrl, searchData)
searchPage = urllib2.urlopen(searchReq)
searchSoup = BeautifulSoup(searchPage)

#Get the entries of apps
apps = searchSoup.findAll("div", class_="card no-rationale square-cover apps small")

with codecs.open(sys.argv[2], 'w', 'utf-8-sig') as outputFile:
	outputFile.write("App Package Name")
	outputFile.write(",")
	outputFile.write("App Name")
	outputFile.write(",")
	outputFile.write("App Category")
	outputFile.write(",")
	outputFile.write("Rating Count")
	outputFile.write(",")
	outputFile.write("Download Count")
	outputFile.write(",")
	outputFile.write("Score")
	outputFile.write(",")
	outputFile.write("Vendor")
	outputFile.write("\n")
	#visit the webpage of the app on the google play
	for app in apps:
		appPackage = app["data-docid"]
		outputFile.write(appPackage)
		outputFile.write(",")
		appName = "Unknown"
		appCategory = "Unknown"
		rateCount = "Unknown"
		downloadCount = "Unknown"
		score = "UnKnown"
		vendor = "Unknown"
		try:
			page = urllib2.urlopen("https://play.google.com/store/apps/details?id="+appPackage)
			soup = BeautifulSoup(page)
			appName = soup.find("div", class_="document-title").div.string.replace(","," ")
			appCategory = soup.find("a", class_="document-subtitle category").span.string.replace(","," ")
			rateCount = soup.find("div", class_="reviews-stats").find("span", class_="reviews-num").string.replace(",","")
			downloadCount = soup.find(itemprop="numDownloads").string.replace(",","")
			score = soup.find("div", class_="score").string
			vendor = soup.find("a", class_="document-subtitle primary").span.string.replace(","," ")

		except:
			#print '-'*60
			#traceback.print_exc(file=sys.stdout)
			#print '-'*60
			print "Cannot query app information:" + appPackage
		outputFile.write(appName)
		outputFile.write(",")
		outputFile.write(appCategory)
		outputFile.write(",")
		outputFile.write(rateCount)
		outputFile.write(",")
		outputFile.write(downloadCount)
		outputFile.write(",")
		outputFile.write(score)
		outputFile.write(",")
		outputFile.write(vendor)
		outputFile.write("\n")