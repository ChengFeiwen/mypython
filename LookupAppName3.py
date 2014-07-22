##
## Look up application name via package name
##
## Searching app name other metadata by package name
## The input file contains app package names which are separated by \n
## ex:
## com.asus.email
## com.asus.todo
## com.asus.launcher
##
## Author Feiwen Cheng
## Date : 2014/7/22

import urllib,urllib2,sys,codecs,traceback
from bs4 import BeautifulSoup

#Get input and out files
if len(sys.argv)!=3:
	print "Usage",sys.argv[0], "inputFile outputFileName"
	sys.exit(2);

#Read input file
packages = []
with open(sys.argv[1], 'r+') as inputFile:
	for line in inputFile:
		packages.append(line);

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
	outputFile.write("Vendor")
	outputFile.write("\n")
	#visit the webpage of the app on the google play
	for appPackage in packages:
		appPackage = appPackage.strip("\n")
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
		try:
			#page = urllib2.urlopen("https://play.google.com/store/apps/details?id=com.asus.email")
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
			outputFile.write(vendor)
			outputFile.write("\n")
		except:
			#print '-'*60
			#traceback.print_exc(file=sys.stdout)
			#print '-'*60
			appSearchFromWDJ.append(appPackage)

if len(appSearchFromWDJ) > 0 :
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