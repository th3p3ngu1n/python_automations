import enum
import requests  # http requests

from bs4 import BeautifulSoup  # web scraping
# Send the mail
import smtplib
import ssl
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# system date and time manipulation
import datetime

now = datetime.datetime.now()

# email content placeholder
content = ''

# extracting Hacker News Stories

def extract_news(url):
    print('Extracting Hacker News Stories...')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n' + '<br>' + '-' * 50 + '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')    
    for i, tag in enumerate(soup.find_all('td', attrs={'class': 'title', 'valign': ''})):
        next = tag.next
        link = next['href']
        storyText = next.text
        cnt += (
            (str(i + 1) + ' :: ' + storyText + ' (' + link +')' + "\n" + '<br>')
            if tag.text != 'More' else ''
        )
    return (cnt)    

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += '<br><br>End of Message'

print(content)

# lets send the email

print('Composing Email...')

# update your email details
FROM = open("emailFrom.txt", "r").read()  # your from email id
TO = open("emailTo.txt", "r").read()  # your to emails ids # can be a list
appPassword = open("emailPassword.txt", "r").read()

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' ' + \
    str(now.month) + '-' + str(now.day) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
    server.login(FROM, appPassword)
    server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')