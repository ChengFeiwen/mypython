##
## Look TT link via TT ID
##
## Author Feiwen Cheng
## Date : 2014/6/28
 
import urllib, urllib2, sys, base64, urlparse, cookielib, mechanize
from bs4 import BeautifulSoup

ttUrlBase = "http://192.168.88.187/tmtrack/"
def getAuthHeader(userName, password):
	base64string = base64.encodestring('%s:%s' % (userName, password))[:-1]
	return "Basic %s" % base64string

def getBrowser(userName, password):
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_equiv(True)
	br.set_handle_gzip(True)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	br.set_handle_robots(False)
	br.addheaders = [("User-agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36")]
	br.addheaders.append(('Authorization', getAuthHeader(userName, password)))
	return br

def findTTUrl(userName, password, ttId):
	findUrl = ttUrlBase + "tmtrack.dll?FindForm"
	values = {"sid" : "iratfcvh&ReportPage", "Template" : "reports/listframe", "incsub":"1" ,"options":"1", "Target":"QuickIdSearch", "TableId":"1001", "SearchTID":"1001", "SolutionId":"2","Keywords":ttId} 
	data = urllib.urlencode(values)
	req = urllib2.Request(findUrl, data)
	req.add_header("Authorization", getAuthHeader(userName, password))
	page = urllib2.urlopen(req)
	#Parse the result to get tt record id
	soup = BeautifulSoup(page)
	links = soup.find_all("a")
	ttLink = "";
	for link in links:
		if ttId == link.string:
			ttLink = link["href"]
	formUrl = ttUrlBase + ttLink
	return formUrl

def updateTT(userName, password, ttId, updateInfo):
	ttUrl = findTTUrl(userName, password, ttId)
	#Use mechanize to emulate browser behavior
	br = getBrowser(userName, password)
	#response = br.response()
	br.select_form(name="ViewForm")
	#<input class="roundedbutton" type="submit" name="TransitionId.1" value="Update" onclick="onClickButton(this)" style="">
	br.submit(name="TransitionId.1", label="Update")
	submitLink = br.geturl()
	sid = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["sid"][0]
	recordLockId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["RecordLockId"][0]
	projectId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["ProjectId"][0]
	recordId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["RecordId"][0]
	if recordLockId == "0":
		#Might consider to berak lock automatically later
		print "The issue is locked by other browser"
		#Consider to add function to break the lock
	else:
		#Update TT
		updateUrl = "%s/tmtrack.dll?sid=%s&TransitionForm" % (ttUrlBase,sid)
		#http://192.168.88.187/tmtrack/tmtrack.dll?sid=owgdqrth&TransitionPage&Template=form&ProjectId=796&RecordId=360033&TableId=1001&TransitionId=19&Action=Verify%20Bug%20Fix&RecordLockId=33683569
		updateValues = {"TransitionPage":"","Template":"form","ProjectId":projectId,"RecordId":recordId, "TableId":"1001", "TransitionId":"1", "Action":"Update", "RecordLockId":recordLockId, "H1112":updateInfo}
		updateData = urllib.urlencode(updateValues)
		updateReq = urllib2.Request(updateUrl, updateData)
		updateReq.add_header("Authorization", getAuthHeader(userName, password))
		updatePage = urllib2.urlopen(updateReq)

def resolveTT(userName, password, ttId, versionInfo):
	ttUrl = findTTUrl(userName, password, ttId)
	#Use mechanize to emulate browser behavior
	br = getBrowser(userName, password)
	br.select_form(name="ViewForm")
	#<input class="roundedbutton" type="submit" name="TransitionId.19" value="Verify Bug Fix" onclick="onClickButton(this)" style="">
	br.submit(name="TransitionId.19", label="Verify Bug Fix")
	submitLink = br.geturl()
	sid = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["sid"][0]
	recordLockId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["RecordLockId"][0]
	projectId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["ProjectId"][0]
	recordId = urlparse.parse_qs(urlparse.urlparse(submitLink).query)["RecordId"][0]
	if recordLockId == "0":
		#Might consider to berak lock automatically later
		print "The issue is locked by other browser"
		#Consider to add function to break the lock
	else:
		#Resolve TT
		resolveUrl = "%s/tmtrack.dll?sid=%s&TransitionForm" % (ttUrlBase,sid)
		#http://192.168.88.187/tmtrack/tmtrack.dll?sid=owgdqrth&TransitionPage&Template=form&ProjectId=796&RecordId=360033&TableId=1001&TransitionId=19&Action=Verify%20Bug%20Fix&RecordLockId=33683569
		resolveValues = {"TransitionPage":"","Template":"form","ProjectId":projectId,"RecordId":recordId, "TableId":"1001", "TransitionId":"19", "Action":"Verify Bug Fix", "RecordLockId":recordLockId, "F317":versionInfo}
		resolveData = urllib.urlencode(resolveValues)
		resolveReq = urllib2.Request(resolveUrl, resolveData)
		resolveReq.add_header("Authorization", getAuthHeader(userName, password))
		resolvePage = urllib2.urlopen(resolveReq)		

def dispathTT2CorrectOwner(userName, password):
	reportUrl = "http://192.168.88.187/tmtrack/tmtrack.dll?ReportPage&reportid=29498&template=reports%2flist&RptKey=1408016805&Recno=-1"
	req = urllib2.Request(reportUrl)
	req.add_header("Authorization", getAuthHeader(userName, password))
	page = urllib2.urlopen(req)
	#Parse the result to get tt record id
	soup = BeautifulSoup(page)
	itemList = soup.findAll("a", class_="nounderline")
	ttList = []
	for item in itemList:
		try:
			id = item.string
			int(id)
			ttList.append(id)
		except ValueError:
			pass
    # not an integer
	return ttList

def assignTT(userName, password, ttId):
	reportUrl = "http://192.168.88.187/tmtrack/tmtrack.dll?ReportPage&reportid=29498&template=reports%2flist&RptKey=1408016805&Recno=-1"
	#Use mechanize to emulate browser behavior
	br = getBrowser(userName, password)
	br.open(ttUrl)
	#response = br.response()
	br.select_form(name="ViewForm")
	pass

if __name__ == "__main__":
	#if len(sys.argv)!=3:
	#	print "Usage",sys.argv[0], "ttID updateMessage"
	#	sys.exit(0);
	#ttId = sys.argv[1]
	#updateMessage = sys.argv[2]
	userName = "test"
	password = "test"
	print dispathTT2CorrectOwner(userName,password)
	#updateTT(userName, password, ttId, updateMessage)
	#resolveTT(userName, password, ttId, updateMessage)
