import os
import requests
from twill.commands import *
from twill import *
from datetime import date, datetime
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from pathlib import Path

### Script to extract two reports from our company's
### configuration of Oracle MyMicros, and then email
### them to multiple recipients 

# Requires environment variables *2 to be set:-
# MYMICROS_PW - password for MyMicros/R&A
# SENDGRID_API_kEY - self-explanatory! 

## Using Twill to open the webpage and scrape the data

debug('http',1)
go("https://caffenero.simphony.eu/login.jsp")
showforms()

# Logs into the MyMicros portal 
# POSTing the login form 

fv('login','action','login')
fv('login', 'usr','***username***')
fv('login', 'cpny','***company***')
fv('login', 'pwd', os.environ.get('MYMICROS_PW'))
fv('login','LOGIN','')

submit()
info()

# set the names for the reports
# as in this case they will also be
# saved to disk
date = date.today().strftime('%d-%m-%Y')

report1=(str(date+'-report1'+'.html'))
report2=(str(date+'-report2'+'.html'))

# get the reports and save to current dir on disk
# in this instance you must visit the first site to run the report
# and then the second and third will be the reports only in html 
go("https://caffenero.simphony.eu/finengine/reportAction.do?method=run&reportID=3")
go('https://caffenero.simphony.eu/finengine/reportRunAction.do?rptroot=3&reportID=EAME_CurrentOpsReport_VAT&method=run')
save_html(report1)
go("https://caffenero.simphony.eu/finengine/reportRunAction.do?method=run&reportID=CurrentReceiptsDetail&rptroot=3")
save_html(report2)

## merge two html files together
## to form single message body

with open(report1) as fp: 
    data = fp.read() 
  
with open(report2) as fp: 
    data2 = fp.read() 
  
# Merging the two reports from next line 
data += "\n"
data += data2 

reportWhole =(str(date+'-reportWhole'+'.html'))

# write two reports to disk
with open (reportWhole, 'w') as fp: 
    fp.write(data) 

## Send emails

# this script sends two emails, one containing
# both reports merged together, and another
# sending just the second report to a different
# recipient who refuses to move to c21.

# prepare email for me
with open(reportWhole, 'r') as fp:
    messageContent = fp.read()

# preparing email subject
# in the format 'Sales report for dd-mm-yyyy'
sub = 'Sales report for ' + date

# preparing message payload
message = Mail(
    from_email=('***from_email***'),
    to_emails=('***to_email***'),
    subject=sub,
    html_content=messageContent
    )

# send email
try:
    print("Sending email...")
    sg = SendGridAPIClient(
        os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print("Response Status Code: " + response.status_code)
    print("Response Body: " + response.body)
    print("Response Headers:  " + response.headers)
except Exception as e:
    print(e)


# email to recipient from c20.

with open(report2, 'r') as fp:
    messageContent = fp.read()
# preparing message payload
message = Mail(
    from_email=('***from_email***'),
    to_emails=('***to_email***'),
    subject=sub,
    html_content=messageContent
    )

# send email
try:
    print("Sending email...")
    sg = SendGridAPIClient(
        os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print("Response Status Code: " + response.status_code)
    print("Response Body: " + response.body)
    print("Response Headers:  " + response.headers)
except Exception as e:
    print(e)


