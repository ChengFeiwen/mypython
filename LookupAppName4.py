##
## Look up application name via package name
##
## 0. Searching app name other metadata by package name
## ex:python LookUPAppName 0 packageName.txt output.csv
## The input file contains app package names which are separated by \n
## com.asus.email
## com.asus.todo
## com.asus.launcher
##
## 1. Searching popular apps' metadata from google play via keyword.
## ex:python LookUPAppName 1 email output.csv
## Author Feiwen Cheng
## Date : 2014/7/28

import urllib,urllib2,sys,codecs,traceback
from bs4 import BeautifulSoup

def loadPackageFromFile(fileName):
	packageName = []
	with open(fileName, 'r+') as inputFile:
		for line in inputFile:
			packages.append(line.strip("\n"));
	return packageName

def searchPackageNameViaKeyword(keyword):
	packageName = []
	#Search apps via key word from google play
	searchUrl = "https://play.google.com/store/search"
	searchValues = {"q" : sys.argv[1], "c" : "apps"}
	searchData = urllib.urlencode(searchValues)
	searchReq = urllib2.Request(searchUrl, searchData)
	searchPage = urllib2.urlopen(searchReq)
	searchSoup = BeautifulSoup(searchPage)

	#Get the entries of apps
	apps = searchSoup.findAll("div", class_="card no-rationale square-cover apps small")
	for app in apps:
		appPackage = app["data-docid"]
		packageName.append(appPackage);
	return packageName
	

#Check arg
if len(sys.argv)!=4:
	print "Usage",sys.argv[0], "0 inputFile outputFileName"
	print "Usage",sys.argv[0], "1 keyword outputFileName"
	sys.exit(0);

#Get package name through inputfile or keyword
packages = []
if(sys.argv[1] == "0"):
	packages = loadPackageFromFile(sys.argv[1])
else:
	packages = searchPackageNameViaKeyword(sys.argv[1])

appSearchFromWDJ =[]

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
	outputFile.write("S5")
	outputFile.write(",")
	outputFile.write("S4")
	outputFile.write(",")
	outputFile.write("S3")
	outputFile.write(",")
	outputFile.write("S2")
	outputFile.write(",")
	outputFile.write("S1")
	outputFile.write(",")
	outputFile.write("Price")	
	outputFile.write(",")
	outputFile.write("Vendor")
	outputFile.write("\n")
	#visit the webpage of the app on the google play
	for appPackage in packages:

		appName = "Unknown"
		appCategory = "Unknown"
		rateCount = "Unknown"
		downloadCount = "Unknown"
		score = "UnKnown"
		s5 ="Unknown"
		s4 ="Unknown"
		s3 ="Unknown"
		s2 ="Unknown"
		s1 ="Unknown"
		vendor = "Unknown"
		price = "0"
		try:
			#page = urllib2.urlopen("https://play.google.com/store/apps/details?id=com.square_enix.android_googleplay.FFIV_GP")
			page = urllib2.urlopen("https://play.google.com/store/apps/details?id="+appPackage)
			soup = BeautifulSoup(page)
			appName = soup.find("div", class_="document-title").div.string.replace(","," ")
			appCategory = soup.find("a", class_="document-subtitle category").span.string.replace(","," ")
			rateCount = soup.find("div", class_="reviews-stats").find("span", class_="reviews-num").string.replace(",","")
			s5 = soup.find("div", class_="rating-bar-container five").find("span", class_="bar-number").string.replace(",","")
			s4 = soup.find("div", class_="rating-bar-container four").find("span", class_="bar-number").string.replace(",","")
			s3 = soup.find("div", class_="rating-bar-container three").find("span", class_="bar-number").string.replace(",","")
			s2 = soup.find("div", class_="rating-bar-container two").find("span", class_="bar-number").string.replace(",","")
			s1 = soup.find("div", class_="rating-bar-container one").find("span", class_="bar-number").string.replace(",","")
			downloadCount = soup.find(itemprop="numDownloads").string.replace(",","")
			score = soup.find("div", class_="score").string
			try:
				price = soup.find(itemprop="price")["content"].replace(",","")
			except:
				pass
			vendor = soup.find("a", class_="document-subtitle primary").span.string.replace(","," ")
			outputFile.write(appPackage)
			outputFile.write(",")
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
			outputFile.write(s5)
			outputFile.write(",")
			outputFile.write(s4)
			outputFile.write(",")
			outputFile.write(s3)
			outputFile.write(",")
			outputFile.write(s2)
			outputFile.write(",")
			outputFile.write(s1)
			outputFile.write(",")			
			outputFile.write(price)			
			outputFile.write(",")			
			outputFile.write(vendor)
			outputFile.write("\n")
		except:
			#print '-'*60
			#traceback.print_exc(file=sys.stdout)
			#print '-'*60
			appSearchFromWDJ.append(appPackage)

if len(appSearchFromWDJ) > 0 and sys.argv[1] == "0" :
	print "Some app need to look up from Wandouja"
	with codecs.open("wandouja_" + sys.argv[2], 'w', 'utf-8-sig') as outputFile:
		outputFile.write("App Package Name")
		outputFile.write(",")
		outputFile.write("App Name")
		outputFile.write(",")
		outputFile.write("App Category")
		outputFile.write(",")
		outputFile.write("Rating Count")
		outputFile.write("\n")
		for appPackage in appSearchFromWDJ:
			try:
				page = urllib2.urlopen("http://www.wandoujia.com/apps/"+appPackage)
				soup = BeautifulSoup(page)
				appName = soup.body["data-title"]
				appCategory = soup.find("dd", class_="tag-box").a.string
				score = soup.find("span", class_="item love").i.string
				outputFile.write(appPackage)
				outputFile.write(",")
				outputFile.write(appName)
				outputFile.write(",")
				outputFile.write(appCategory)
				outputFile.write(",")
				outputFile.write(score)
			except:
				print "Cannot query app information:" + appPackage