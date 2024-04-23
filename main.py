import datetime
import imaplib
import email
from email.header import decode_header
import base64
import os
from bs4 import BeautifulSoup
import re 
import requests
import logging
import yaml
from redminelib import Redmine

def decode_part(part, enc):
  res = ''
  match enc:
    case "utf-8":
      res = part.decode(enc)
    case _:
      res = part.decode()
  return res

logging.basicConfig(
  format='[%(asctime)s] [%(levelname)-7s] %(message)s', 
  level=logging.DEBUG, 
  filename="./logs/log.log"
)
# logging.debug('This message should appear on the console')
# logging.info('So should this')
# logging.warning('And this, too')

URL = 'http://localhost:3000'
IMAP_HOST = 'imap.mail.ru'

with open('config.yml') as f:
  projects = yaml.safe_load(f)

for project in projects:
  redmine = Redmine(URL, key=project['key'])
# redmine.issue.create(
#   project_id='testapi',
#   subject='Vacation',
#   tracker_id=1,
#   description='foo',
#   status_id=1,
#   priority_id=2,
#   assigned_to_id=1,
#   watcher_user_ids=[1],
#   start_date=datetime.date(2014, 1, 1),
#   due_date=datetime.date(2014, 2, 1),
#   estimated_hours=4,
#   done_ratio=40,
#   uploads=[{'path': './attachments/Курсовая Имитационная модель канала связи OFDM.docx'}]
# )

  mail = imaplib.IMAP4_SSL(IMAP_HOST)
  mail.login(project['login'], project['password'])
  mail.select("INBOX")
  _, ids = mail.search('search', 'ALL', 'ALL')

  detach_dir = "."

  if 'attachments' not in os.listdir(detach_dir):
    os.mkdir('attachments')

  res, msg = mail.uid('fetch', b'7', '(RFC822)')
  msg = email.message_from_bytes(msg[0][1])

  subject = decode_header(msg["Subject"])
  subject_payload = subject[0][0]
  subject_encoding = subject[0][1]
  subject = decode_part(subject_payload, subject_encoding)
  print("Subject =", subject)

  mail_from = msg["Return-path"].replace("<", "").split("@")[0]
  print("From =", mail_from)

  description = ''

  for part in msg.walk():
    type = part.get_content_type()
    print(type)
    # if part.get_content_disposition() == "attachment":
    #   fileName = part.get_filename()
    #   fileName = decode_header(fileName)[0][0].decode()
    #   filePath = os.path.join(detach_dir, 'attachments', fileName)
    #   fp = open(filePath, 'xb')
    #   fp.write(part.get_payload(decode=True))
    #   fp.close()
    match type:
      case "text/plain":
        encoding = part.get_content_charset()
        payload = part.get_payload(decode=True)
        description = decode_part(payload, encoding)
        print("Description =", description)
      # case "text/html":
      #   soup = BeautifulSoup(part.get_payload(), features="html.parser")
      #   print(soup.get_text())