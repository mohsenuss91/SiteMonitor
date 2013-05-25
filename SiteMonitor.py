#!/usr/bin/env python

import urllib
import smtplib
import time
import datetime
import sys

"""
This script will check the status of sites on specified urls in the sites.txt file.
And will send an email to emailaddresses in the email.txt file if a site is down
and will send another email once the site is back up.
This script logs to the status.txt file.
"""

class monitor(object):
    """
    representation of a site up or down monitor
    """
    def __init__(self, sitesFile, emailFile, logFile):
        self.logFile = logFile # log file will be created if does not exist
        self.statusMap = {} # used to keep track of status {url: up or down. etc....}
        try:
            with open(sitesFile) and open(emailFile): pass # check if given files can be opened
        except Exception as e:
            print "Please specify a valid site file and email file :" + str(e)
            self.writeToLog("Please specify a valid site file and email file :" + str(e))
            sys.exit()
        else:
            self.sitesFile = sitesFile
            self.emailFile = emailFile

    def writeToLog(self, logMsg):
        """
        takes in a log message and writes it to status.txt
        """
        try:
            f = open(self.logFile, 'a')
        except Exception as e:
            print 'Unable to open log file: ' + str(e)
        try:
            f.write(str(datetime.datetime.now())[:-7] + " | " + logMsg + "\n")
            f.close()
        except Exception as e:
            print 'Unable to write to log file: ' + str(e)

    def getUrls(self):
        """
        Takes in a file with urls and returns a list of urls
        """
        urlList = []
        try:
            f = open(self.sitesFile, 'r')
            for line in f:
                # ignore empty lines and lines that start with hash / pound sign to allow commenting #
                if line[:1] != '#' and line.strip() != "" and line.strip() != None:
                    urlList.append(line.strip())
            f.close()
        except Exception as e:
            print 'Error on opening the file used by the getUrls function: ' + str(e)
            self.writeToLog('Could not open the file with site urls. Exiting script: ' +str(e))
            self.sendEmail('Could not open the file with site urls. Exiting script: ' +str(e))
            sys.exit()
        return urlList

    def getEmails(self):
        """
        reads in email addresses line by line from a file fileIn
        and returns the addresses in a list
        """
        emailList = []
        try:
            f = open(self.emailFile, 'r')
            for line in f:
                # ignore empty lines and lines that start with hash / pound sign to allow commenting #
                if line[:1] != '#' and line.strip() != "" and line.strip() != None:
                    emailList.append(line.strip())
            f.close()
        except Exception as e:
            self.writeToLog('Error on opening the file used by the getEmails function: ' + str(e))    
        return emailList

    def getStatus(self, url):
        """
        makes a request to an url and returns the header status.
        returns zero if url does not exist.
        """
        try:
            a=urllib.urlopen(url)
            return a.getcode()
        except:
            self.writeToLog(url + ' did not return any header status.')
            return 0

    def sendEmail(self, msg, subject = "Site down / up again message"):
        """
        Sends an email to list of emailasdresses. Takes message string as input
        """
        config = getConfig('config.txt')
        toaddrs  = self.getEmails()
        # configurable vars
        fromaddr = config[4]
        # Credentials
        username = config[2]
        password = config[3]
        # doing some message formatting
        m = "From: %s\r\nTo: %s\r\nSubject: %s\r\nX-Mailer: My-Mail\r\n\r\n" % (fromaddr, ", ".join(toaddrs), subject)
        # The actual mail send
        try:
            server = smtplib.SMTP(config[0]+':'+config[1])
            server.starttls()
            server.login(username,password)
            server.sendmail(fromaddr, toaddrs, m+msg)
            server.quit()
            self.writeToLog('email send')
            print('email send')
        except Exception as e:
            self.writeToLog('email not send: ' + str(e))
            print('email not send')
            print e

    def checkStatus(self, urls):
        Gstatus = self.getStatus('http://www.google.com') #let's see if we ourselves are connected by checking the mighty G.
        if Gstatus != 200:
            print "Google is down ...\nyeah right, probably our monitor lost internet connection.\nSkipping this check."
            self.writeToLog("Google is down ... yeah right, probably our monitor lost internet connection. Skipping this check.")
            print 'done'
            return
        # loop through all sites
        for url in urls:
            print url
            # get the status of the site
            status = self.getStatus(url)
            # if not 200 and statusMap not down
            if status != 200 and self.statusMap.get(url) != 'down':
                self.writeToLog(url[7:] + " is down! Site status is " + str(status))
                # send email(down)
                message = url[7:] + " is down!\nSite status is " + str(status) + "\n" + str(datetime.datetime.now())[:-7]
                subject = url[7:] + " is down!"
                print message
                print 'sending email...'
                self.sendEmail(message, subject)
                # set status in statusMap as down
                print 'changing site status to down'
                self.statusMap[url] = 'down'
            # elif 200 and statusMap is down
            elif status == 200 and self.statusMap.get(url) == 'down':
                self.writeToLog(url[7:] + " is up again!")
                # send email (up again)
                message = url[7:] + " is up again!\n" + str(datetime.datetime.now())[:-7]
                subject = url[7:] + " is up again!"
                print message
                print 'sending email...'
                self.sendEmail(message, subject)
                # set status in statusMap as up
                print 'changing site status to up'
                self.statusMap[url] = 'up'
            print 'done'

def getConfig(fileIn):
    """
    read in a config file
    gets variables - value pairs

    returns a list of [variable, value]
    """
    confList = []
    f = open(fileIn, 'r')
    for line in f:
        # ignore empty lines and lines that start with hash / pound sign to allow commenting #
        if line[:1] != '#' and line.strip() != "" and line.strip() != None and line[:3] != 'MON' and line[:3] != "SIT" and line[:3] != "EMA":
            confList.append(line.strip().split(",")[1])
    f.close()
    return confList
#print getConfig('config.txt')
    
def getMonitors(fileIn):
    """
    reads in the monitor vars from config.txt
    and instantiates monitors
    returns a list of monitor objects
    """
    monList = []
    f = open(fileIn, 'r')
    for line in f:
        # ignore empty lines and lines that start with hash / pound sign to allow commenting #
        if line[:1] != '#' and line.strip() != "" and line.strip() != None:
            if line[:3] == 'MON' or line[:3] == "SIT" or line[:3] == "EMA":
                monList.append(line.strip().split(","))
    f.close()
    monObjs = []
    for i in range(len(monList)):
        if monList[i][0] == "MON":
            print "creating monitor: " + str(monList[i][1])
            monObjs.append(monitor(monList[i+1][1],monList[i+2][1], 'status.txt'))
    #return monList
    return monObjs
#print getMonitors('config.txt')

# let's instantiate a monitor
#mon = monitor('sites.txt', 'email.txt', 'status.txt')

def mainloop():
    monitors = getMonitors('config.txt')
    while True:
        print str(datetime.datetime.now())[:-7]
        print 'checking...'
        for i in range(len(monitors)):
            monitors[i].checkStatus(monitors[i].getUrls())
        time.sleep(int(getConfig('config.txt')[5]))

mainloop()
