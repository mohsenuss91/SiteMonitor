Application name: Site Monitor
Application version: 0.1
Author: Dave Tromp, dave @ davetromp dot nl

This application is a very basic site monitor. It will check urls from one or more lists of sites one by one. If the site at a url does not return headerstatus 200 an email will be send out. Once the site is back up again another email will be send out.

File structure
Following files are included in the program folder

SiteMonitor
   SiteMonitor.exe
   SiteMonitor.py
   _hashlib.pyd
   _socket.pyd
   _ssl.pyd
   bz2.pyd
   config.txt
   email.txt
   python27.dll
   readme.txt
   sites.txt
   unicodedata.pyd
  
All actions are logged to the file status.txt. This file will be created if it does not yet exist.

Configuration
There are 3 configuration files. The file config.txt is used to setup the monitor(s) and setup email sending via an external smtp service, like gmail or your ISP's mail server. The default monitor is configured to use urls and send-to email addresses located in the sites.txt and email.txt files. You can add additional monitors in the config.txt file and have them reference different sites and email addresses located in different files. This way it is possible to have different monitors for different (groups) of sites that report to different email addresses.

Execution
On windows you can click on the SiteMonitor.exe executable to start running the monitor. On mac or linux you use the SiteMonitor.py python script file to do the same. MacOSX and most linux distro's have python 2.7 installed by default, so you should be able to run it.