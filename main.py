import requests
import smtplib
import ssl
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from email.mime.text import MIMEText
from bs4 import BeautifulSoup


def check_handbrake_stock():
    url = 'https://heusinkveld.com/products/shifters-handbrakes/sim-handbrake-2/?q=%2Fproducts%2Fshifters-handbrakes%2Fsim-handbrake-2%2F'
    page = requests.get(url)
    port = 465
    password = os.environ['PASSWORD']
    sender_email = os.environ['SENDER_EMAIL']
    receiver_email = os.environ['RECEIVER_EMAIL']

    print("Fetching store page...")
    soup = BeautifulSoup(page.content, 'html.parser')
    print("Parsing content...")
    product_info = soup.find('p', class_='stock in-stock')

    if product_info is not None:
        print("Handbrake detected as in stock, preparing to send e-mail to {}.".format(receiver_email))
        body_text = "Handbrake has been detected as being restocked.\nhttps://heusinkveld.com/products/shifters-handbrakes/sim-handbrake-2/?q=%2Fproducts%2Fshifters-handbrakes%2Fsim-handbrake-2%2F"
        message = MIMEText(body_text)
        message['subject'] = "Heusinkveld Handbrake Restock"
        message['from'] = sender_email
        message['to'] = receiver_email
        with smtplib.SMTP_SSL('smtp.gmail.com', port) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("E-mail sent.")
    else:
        print("Handbrake has not restocked yet.")


print("Heusinkveld stock checker has started.")

scheduler = BlockingScheduler()
scheduler.add_job(check_handbrake_stock, 'interval', minutes=15)
scheduler.start()
