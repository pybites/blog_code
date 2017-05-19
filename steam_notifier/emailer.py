#!python3
#emailer.py is a simple script for sending emails using smtplib

import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_list import EMAILS

DATA_FILE = 'steam_games.db'
from_addr = 'your-email@gmail.com'
to_addr = EMAILS
msg = MIMEMultipart()
msg['From'] = from_addr
msg['To'] = ", ".join(to_addr)
msg['Subject'] = 'New Releases and Sales on Steam'

body = ''

with sqlite3.connect(DATA_FILE) as connection:
    c = connection.cursor()
    c.execute("SELECT Name, Link FROM new_steam_games WHERE Emailed='0'")
    for item in c.fetchall():
	    body += item[0] + ': ' + item[1] + '\n'
    c.execute("UPDATE new_steam_games SET Emailed='1'")

msg.attach(MIMEText(body, 'plain'))

smtp_server = smtplib.SMTP('smtp.gmail.com', 587) #Specify Gmail Mail server

smtp_server.ehlo() #Send mandatory 'hello' message to SMTP server

smtp_server.starttls() #Start TLS Encryption as we're not using SSL.

#Login to gmail: Account | Password
smtp_server.login(' your-email@gmail.com ', ' GMAIL-APP-ID-HERE ')

text = msg.as_string()

#Compile email list: From, To, Email body
smtp_server.sendmail(from_addr, to_addr, text)

#Close connection to SMTP server
smtp_server.quit()

#Test Message to verify all passes
print('Email sent successfully')
