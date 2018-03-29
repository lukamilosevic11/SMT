#!/usr/bin/python
import urllib.request,re,json
from datetime import datetime
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

now = datetime.today()

def getIP():
    url = "https://www.iplocation.net/find-ip-address"
    uf = urllib.request.urlopen(url)
    html = uf.read()
    regex = re.compile("Your IP Address is.*?([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)")
    for r in regex.finditer(str(html)):
        return r.group(1)

def checkIP(ip):
    try:
        with open("ip.json","r+") as f:
            fileContent = json.load(f)
            if(ip == fileContent["ip"]):
                return True
            else:
                fileContent["ip"] = ip
                f.seek(0)
                json.dump(fileContent,f)
                return False
    except IOError as e:
        try:
            with open("logErr.txt","a+") as output:
                output.write("Error while opening ip.json %s\n"%str(now.strftime("%d.%m.%Y. %H:%M:%S")))
        except IOError as e:
            print ("Error while opening logErr.txt for ip.json closing app...")
            exit()

def SendMail(ip):
    filename = "data.json"
    try:
        with open(filename,"r") as f:
            contentFile = json.load(f)
            msg = MIMEMultipart()
            fromaddr = contentFile["sender"] #from email address you@gmail.com
            toaddr = contentFile["recipient"] #to email address   someone@gmail.com
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "IP address "+str(now.strftime("%d.%m.%Y. %H:%M:%S"))
            msg.attach(MIMEText(ip))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(contentFile["username"], contentFile["password"]) #user and pass for gmail account
            server.sendmail(fromaddr, toaddr, msg.as_string())
            server.quit()
            print("Email sent successfully!")
    except IOError as e:
        try:
            with open("logErr.txt","a+") as output:
                output.write("Error while opening data.json %s\n"%str(now.strftime("%d.%m.%Y. %H:%M:%S")))
        except IOError as e:
            print ("Error while opening logErr.txt for data.json closing app...")
            exit()
if __name__ == '__main__':
    ip = getIP()
    if(checkIP(ip.strip()) is False):
        SendMail(ip.strip())
