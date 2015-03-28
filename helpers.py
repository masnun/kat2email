import yaml
import requests
import lxml.html
from pymongo import MongoClient
import sys
from jinja2 import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load Configurations and connect to MongoDB
try:
    configs = yaml.load(open("config.yaml"))
    database = MongoClient(configs['mongo']['host'], configs['mongo']['port'])[configs['mongo']['database']]
except Exception as exc:
    print("Error loading configs or connecting to Mongo!")
    sys.exit()


def get_url(type_, page):
    return configs['torrents']['source'] + "/{type}/{page}/".format(type=type_, page=page)


def get_html(url):
    return requests.get(url).text


def insert_torrents(torrent):
    return database[configs['mongo']['collection']].insert(torrent)


def torrent_exists(torrent):
    return database[configs['mongo']['collection']].find_one({'link': torrent['link']}) is not None


def parse_torrents(html):
    tree = lxml.html.fromstring(html)
    rows = tree.cssselect('tr.odd, tr.even')
    torrents = []

    for row in rows:
        anchor = row.cssselect('a.cellMainLink')[0]
        title = anchor.text
        link = configs['torrents']['source'] + anchor.get('href')

        for keyword in configs['torrents']['keywords']:
            if keyword.lower() in title.lower():
                torrent = {
                    'title': title,
                    'link': link
                }

                if not torrent_exists(torrent):
                    torrents.append(torrent)
                    insert_torrents(torrent)

    return torrents


def get_torrents(type_, page):
    url = get_url(type_, page)
    html = get_html(url)
    torrents = parse_torrents(html)

    return torrents


def prepare_template(data):
    html = open(configs['email']['template']).read()
    template = Template(html)
    return template.render(**data)


def send_email(data):
    sender = configs['email']['from']
    to = configs['email']['to']
    msg = MIMEMultipart('alternative')
    msg['Subject'] = configs['email']['subject']
    msg['From'] = sender
    msg['To'] = to

    html = MIMEText(prepare_template(data), 'html')
    msg.attach(html)

    mailer = smtplib.SMTP(configs['email']['smtp']['host'], configs['email']['smtp']['port'])
    # mailer.login(configs['email']['smtp']['username'], configs['email']['smtp']['password'])
    mailer.sendmail(sender, to, msg.as_string())
    mailer.quit()


