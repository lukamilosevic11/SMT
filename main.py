#!/usr/bin/python

from datetime import datetime
import sys
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

now = datetime.today()

def SendMail():
    filename = "log.txt"
    try:
        with open(filename,"rb") as f:
            msg = MIMEMultipart()
            fromaddr = "" #from email address you@gmail.com
            toaddr = "" #to email address   someone@gmail.com
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Dnevni izvestaj "+str(now.strftime("%d.%m.%Y. %H:%M:%S"))
            msg.attach(MIMEText("U prilogu se nalazi log fajl."))
            part = MIMEBase("application","octet-stream")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition","attachment; filename = "+filename)
            msg.attach(part)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("username", "password") #user and pass for gmail account
            server.sendmail(fromaddr, toaddr, msg.as_string())
            server.quit()
            print("Mejl je uspesno poslat")
    except IOError as e:
        try:
            with open("logErr.txt","a+") as output:
                output.write("Error while opening log.txt %s\n"%str(now.strftime("%d.%m.%Y. %H:%M:%S")))
        except IOError as e:
            print ("Error while opening logErr.txt closing app...")
            exit()


if __name__ == '__main__':
    SendMail()
