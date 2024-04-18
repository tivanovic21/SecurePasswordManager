import smtplib
import random
import string
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from backend.authentification import Authentication

load_dotenv()

class Email:
    @staticmethod
    def sendPasswordResetEmail(email):
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=32)) # random token for pass reset
        expiration = datetime.now() + timedelta(hours=1) # expiration time
        Email.saveToken(email, token, expiration) # save to DB

        sender_email = 'zaspam1234@gmail.com'
        sender_password = os.getenv("SENDER_PASSWORD") # SMTP key value
        receiver_email = email
        subject = 'Password Reset Request'
        body = f'Hello, you have requested a password reset.\n To reset the password use this token {token} in the application!'

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp-relay.brevo.com', 587) as smtp_server:
            smtp_server.login(sender_email, sender_password)
            smtp_server.sendmail(sender_email, receiver_email, message.as_string())

    @staticmethod
    def saveToken(email, token, expiration):
        Authentication.saveTokenExpiration(email, token, expiration)