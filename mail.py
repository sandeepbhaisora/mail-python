import email
import imaplib
import re

pattern_uid = re.compile('\d+ \(UID (?P<uid>\d+)\)')


def disconnect(mail):
    mail.logout()


def check_inbox(mail):
    mail.select("inbox")
    _, search_data = mail.search(None, 'UNSEEN')
    # print(search_data)
    for index in search_data[0].split():
        _, data = mail.fetch(index, '(RFC822)')
        _, b = data[0]
        email_message = email.message_from_bytes(b)

        for header in ['subject', 'to', 'from', 'data']:
            print(f'{header} : {email_message[header]}')
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True)
                if (body):
                    print(body.decode())
            elif part.get_content_type() == 'text/html':
                html_body = part.get_payload(decode=True)
                if html_body:
                    print(html_body.decode())


def parse_uid(data):
    if (data):
        data = data.decode('utf-8')
        match = pattern_uid.match(data)
        return match.group('uid')


def mark_all_as_seen(obj):
    obj.select('Inbox')
    status, data = obj.search(None, 'UnSeen')
    unread_msg_nums = data[0].split()
    for e_id in unread_msg_nums:
        obj.store(e_id, '+FLAGS', '\Seen')


def copy_mail(username, password):
    success = False
    mail = connect(username=username, password=password)
    mail.select(mailbox='"[Gmail]/Spam"')
    resp, items = mail.search(None, 'UNSEEN')
    email_ids = items[0].split()
    print(email_ids)
    for latest_email_id in email_ids:
        print(latest_email_id)
        resp, data = mail.fetch(latest_email_id, "(UID)")
        print(data[0])
        msg_uid = parse_uid(data[0])
        print(msg_uid)
        if msg_uid:
            result = mail.uid('COPY', msg_uid, 'Inbox')
            if result[0] == 'OK':
                mov, data = mail.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')
                mail.expunge()
                mark_all_as_seen(mail)
                success = True
    disconnect(mail)
    return success


def connect(username, password):
    host = 'smtp.gmail.com'
    mail = imaplib.IMAP4_SSL(host=host)
    mail.login(username, password=password)
    return mail
