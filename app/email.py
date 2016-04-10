# -*- encoding=utf-8 -*-
# from flask.ext.mail import Message
from threading import Thread
from flask import render_template, current_app
import requests

# def send_async_email(app, msg):
# with app.app_context():
#     mail.send(msg)

def send_async_email(app, auth, data):
        url = "https://api.mailgun.net/v3/"+app.config['MAIL_DOMAIN_NAME']+"/messages"
        mail_post = requests.post(url, auth=auth, data=data)
        return mail_post

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    # msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                    # sender = app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    # msg.html = render_template(template + '.html', **kwargs)
    # thr = Thread(target=send_async_email, args=[app, msg])
    auth=("api", app.config['MAIL_API_KEY'])
    data={
            "from": app.config["FLASKY_MAIL_SENDER"],
            "to": [ to ],
            "subject": "轻翰",
        "text": render_template(template + '.txt', **kwargs)
        }
    thr = Thread(target=send_async_email, args=[app, auth, data])
    thr.start()
    return thr
