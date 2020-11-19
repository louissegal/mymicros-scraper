# mymicros-scraper
## Sript to scrape and email reports from MyMicros/R&A

Fed up of having to log onto the till at EOD, run the reports, scribble them onto a sheet of paper and then trek downstairs to the laptop to send them over to multiple people via email, I devised a solution to extract the reports I needed from the MyMicros reporting system and email them automatically

### How to run

#### Prerequisites

* python3
* sendgrid (pip3 install sendgrid)
* twill (pip3 install twill)
* Sendgrid API key
* Obviously, access to a RES3700/Simphony site with MyMicros/Oracle R&A enabled

### Running

* Replace any dummies with values or ENV variables
* MyMicros login credentials
* Sendgrid API keys
* Email sender
* Email recipient
* Run!
