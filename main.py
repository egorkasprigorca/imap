import imaplib
import email
from email.header import decode_header
import base64
from bs4 import BeautifulSoup
import re
import requests
from redminelib import Redmine

# redmine = Redmine('http://localhost:3000', key="5d6b51e55079fa86c0741123b0378cd9da613d3f")
# project = redmine.project.get('donation-app')

mail = imaplib.IMAP4_SSL('imap.mail.ru')
mail.login("@mail.ru", "")
mail.select("INBOX")
_, mails = mail.search(None, "ALL")
for mail in mails[0].split():
  print(mail, end="\n")

res, msg = mail.fetch(b'1', '(RFC822)')  
res, msg = mail.uid('fetch', b'1', '(RFC822)')
msg = email.message_from_bytes(msg[0][1])

letter_date = email.utils.parsedate_tz(msg["Date"]) # дата получения, приходит в виде строки, дальше надо её парсить в формат datetime
letter_id = msg["Message-ID"] #айди письма
letter_from = msg["Return-path"] # e-mail отправителя

for part in msg.walk():
  if part.get_content_maintype() == 'text' and part.get_content_subtype() == 'plain':
    print(base64.b64decode(part.get_payload()).decode())