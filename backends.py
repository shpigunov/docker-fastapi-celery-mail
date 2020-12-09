import requests
import json

# These keys are from free testing accounts, they are severely limited in
# the scope of possible senders and/or recipients
MAILGUN_KEY = ''
SENDGRID_KEY = ''


def send_mailgun(msg):
    return requests.post(
        "https://api.mailgun.net/v3/almaschool.com.ua/messages",
        auth=("api", MAILGUN_KEY),
        data={"from": f"{msg['from_name']} <{msg['from_addr']}>",
              "to": [f"{msg['to']}"],
              "subject": msg['subject'],
              "text": msg['body']})


def send_sendgrid(msg):
    return requests.post(
        "https://api.sendgrid.com/v3/mail/send",
        json={"personalizations": [
            {
                "to": [
                    {
                        "email": msg['to'],
                        "name": msg['to_name']
                    }
                ],
                "subject": msg['subject']
            }
        ],
            "content": [
            {
                "type": "text/plain",
                "value": msg['body']
            }
        ],
            "from": {
                "email": msg['from_addr'],
                "name": msg['from_name']
        },
            "reply_to": {
                "email": msg['from_addr'],
                "name": msg['from_name']
        }},
        headers={"Authorization": f'Bearer {SENDGRID_KEY}',
                 "Content-Type": "application/json"}
    )


backend_list = [send_mailgun, send_sendgrid]
