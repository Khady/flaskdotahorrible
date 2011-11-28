#!/usr/bin/env python2
#-*- encoding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

SEND_ACCOUNT = 'mail@exemple.com'
USERNAME = 'username'  
PASSWORD = 'password'  

def send(destinataire, sujet, contenu):
    msg = MIMEText(contenu)
    msg['Subject'] = sujet
    msg['From'] = SEND_ACCOUNT
    msg['To'] = destinataire
    server = smtplib.SMTP('smtp.gmail.com:587')  
    server.starttls()  
    server.login(USERNAME,PASSWORD)
    server.sendmail(SEND_ACCOUNT, destinataire, msg.as_string())  
    server.quit()
