import os
import requests
from twill.commands import *
from twill import *
from datetime import date, datetime
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from pathlib import Path


### Script to extract two reports from our company's
### configuration of Oracle MyMicros, and then email
### them to multiple recipients

## healthchecks.io monitoring

URL = "https://hc-ping.com/UUID"

## URL for your version of MyMicros/Simphony R&A
## Your url might be different depending on org
## other examples could be:
## https://www.mymicros.net
## https://YOURORG.simphony.eu
## https://YOURORG.hospitality.oracleindustry.com/login.jsp
myMicrosURL = "https://www.mymicroseu2.net/login.jsp"

def do_work():
    # Requires environment variables *2 to be set:-
    # MYMICROS_PW - password for MyMicros/R&A
    # SENDGRID_API_kEY - self-explanatory!

    ## Using Twill to open the webpage and scrape the data

    debug('http',1)
    go(myMicrosURL)
    showforms()

    # Logs into the MyMicros portal
    # POSTing the login form

    fv('login','action','login')
    fv('login', 'usr','***username***')
    fv('login', 'cpny','***company***')
    fv('login', 'pwd', os.environ.get('MYMICROS_PW'))
    fv('login','LOGIN','')

    submit()
    info()

    # set the names for the reports
    # as in this case they will also be
    # saved to disk
    global date
    date = date.today().strftime('%d-%m-%Y')
    report1=(str(date+'-report1'+'.html'))
    report2=(str(date+'-report2'+'.html'))

    # get the reports and save to current dir on disk
    # in this instance you must visit the first site to run the report
    # and then the second and third will be the reports only in html
    # 
    # to get these, you will be best loggin into myMicros with a web browser
    # and opening dev tools, network inspector. Perform a request (open a report)
    # and copy the URLs where the response is the HTML of report you desire
    go("https://www.mymicroseu2.net/finengine/reportAction.do?method=run&reportID=1")
    go('https://www.mymicroseu2.net/finengine/reportRunAction.do?rptroot=1&reportID=EAME_DailyOpsReport_VAT&method=run')
    save_html(report1)
    go("https://www.mymicroseu2.net/finengine/reportRunAction.do?method=run&reportID=ReceiptsDailyDetail&rptroot=1")
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
    with open(reportWhole, 'r') as fp:
        messageContent = fp.read()

    # preparing email subject
    # in the format 'Sales report for dd-mm-yyyy'
    sub = 'Sales report for ' + date

    # preparing message payload
    message = Mail(
        from_email=('foo@bar.com'),
        to_emails=('bar@foo.com'),
        subject=sub,
        html_content=messageContent
        )

    # send email
    try:
        print("Sending email to bar@foo.com)
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))        
        response = sg.send(message)
        print("Response Status Code: " , response.status_code)
        print("Response Body: " , response.body)
        print("Response Headers:  " , response.headers)
    except Exception as e:
        print(e)


    return True

success = False

try:
    success = do_work()
finally:
    requests.get(URL if success else URL + "/fail")
