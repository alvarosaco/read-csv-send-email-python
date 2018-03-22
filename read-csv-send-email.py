#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
from email import Charset
import time
import os
from email.Header import Header
import sys
import urllib2

num_abstracts = 0
num_emails = 0

file_path = './data.csv'

with open(file_path, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    #writer = csv.DictWriter(tempfile)
    #Form_id,Form_date,Status,Title,Menu-topic,Author-name,Author-Email,Organization,G-recaptcha-response,File-abstractfile,Evaluator,Recomendation,Comments
    for row in reader:
        num_abstracts+=1
        form_id = row['Form_id']
        form_date = row['Form_date']
        status = row['Status']
        title = row['Title']
        topic = row['Menu-topic']
        author = row['Author-name']
        email = row['Author-Email']
        org = row['Organization']
        file_url = row['File-abstractfile']

        print "---"
        print("Title: " + title)
        print("Author: " + author)
        print("Email: " + email)
        print("Organization: " + org)

        body = """
Dear friend,

​​​​We are pleased to inform you that your presentation, “​{PRESENTATION}​”, has been accepted.

Sincerely,

​​The organizing Committee

"""
        body = body.format(PRESENTATION = title)

        html = """\
<html>
<head></head>
<body>
<p>Dear friend,</p>

<p>​​​​We are pleased to inform you that your presentation, <strong><i>“​​{PRESENTATION}​”</i></strong>, has been <strong>accepted</strong>.

<p>Sincerely,</p>

<p>​​The organizing Committee</p>
</body>
</html>
"""
        body = body.format(PRESENTATION = title)

        body = html.format(PRESENTATION = title)

        #enviar email
        msg = MIMEMultipart()
        msg['Subject'] = 'Your submission has been acepted'
        msg['From'] = 'info@org.org'
        #msg['To'] = ''
        msg['To'] = email
        msg['Bcc'] = 'web@org.org'
        msg['Reply-To'] = ''

        #msg.attach(MIMEText(body, 'plain', 'UTF-8'))
        msg.attach(MIMEText(body, 'html', 'UTF-8'))

        #espera de 15 segundos
        time.sleep(15)

        try:
            server = smtplib.SMTP('host.domain.net', 587)
            server.starttls()
            server.login('email@org.org', '***')
            server.sendmail(msg['From'], [ msg['To'], msg['Bcc'] ] , msg.as_string())
            server.quit()
            print("Successfully sent email: " + form_id)
            num_emails+=1
        except:
            print("Error: unable to send email")

    print "---"
print "Total emails enviados: ", num_emails
print "Total papers:", num_abstracts
