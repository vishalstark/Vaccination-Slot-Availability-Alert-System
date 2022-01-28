import datetime
from datetime import date
import json
import pandas as pd
import requests
import smtplib
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pretty_html_table import build_table
import time

pincode = 452001

tommorow_date = date.today() + datetime.timedelta(days=1)
tommorow_date = tommorow_date.strftime("%d-%m-%Y")

baseUrl = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode={pincode}&date={tommorow_date}'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


def send_mail(body):
    message = MIMEMultipart()
    message['Subject'] = 'Alert! Slot Available'
    message['From'] = 'SENDER EMAIL ADDRESS'
    message['To'] = 'RECEIVER''S EMAIL'

    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()

    server = SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(message['From'], "SENDERS EMAIL ADDRESS PASSWORD COMES HERE")
    server.sendmail(message['From'], message['To'], msg_body)
    print("####################################")
    print('\n Alert! Slot Available, Mail Sent \n')
    print("####################################")
    server.quit()

while True:
    # print("Checking")

    try:
        response = requests.get(baseUrl, headers=headers)
        res = json.loads(response.text)

        centers = res['centers']

        center_name = []
        address = []
        available_capacity = []
        vaccine = []
        age_limit = []

        for i in range(len(centers)):
            center_name.append(centers[i]['name'])
            address.append(centers[i]['address'])
            available_capacity.append(centers[i]['sessions'][0]['available_capacity'])
            vaccine.append(centers[i]['sessions'][0]['vaccine'])
            age_limit.append(centers[i]['sessions'][0]['min_age_limit'])
        
        df = pd.DataFrame()
        df['center_name'] = center_name
        df['address'] = address
        df['available_capacity'] = available_capacity
        df['vaccine'] = vaccine
        df['age_limit'] = age_limit

        available_slots = df[df['available_capacity'] == 1]
        available_slots = available_slots.applymap(str)

        if len(available_slots)>1:
            output = build_table(available_slots, 'blue_light')
            send_mail(output)
            break
    except:
        print('Failed to fetch data')

    time.sleep(60)
    