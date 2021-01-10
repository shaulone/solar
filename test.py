#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta
import pytz
import smtplib, ssl

USER='shaul123'
PASSWORD='yes1234yes'
API_KEY="d8860d256e03c97ca24c8548c2979be6489add6c2e4a46e1c1964fb5c65bf01a"
URL="https://api.meteocontrol.de/v2"

payload = {'userId': 'shaul123',
           'password': 'yes1234yes'}
headers = {'X-API-KEY': API_KEY}

tz = pytz.timezone('Asia/Jerusalem')

def time_now_str():
    now = time_before_str(15)
    return now

def time_before_str(minutes):
    time = datetime.now(tz) - timedelta(minutes=minutes)
    time = time.replace(microsecond=0).isoformat()
    time = time.replace(':', '%3A')
    time = time.replace('+', '%2B')
    return time

def send_cmd(cmd):
    url = URL+'/' + cmd
    print(url)
    response = requests.get(url, auth=HTTPBasicAuth(USER, PASSWORD), headers=headers)
    return response

def send_mail(message):
    port = 465  # For SSL
    user = "hardufsolar@gmail.com"
    password = "harduf1234"
    receiver = "shaul.one@gmail.com"
    template = """\
Subject: refet A\n
    
%s""" % message

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(user, password)
        # TODO: Send email here
        # Authentication 
        #server.login("sender_email_id", "sender_email_id_password") 

        # sending the mail 
        server.sendmail(user, receiver, template) 
        # terminating the session 
        server.quit() 

def get_inverters(system_id):
    data = send_cmd('systems/' + system_id + '/inverters/bulk/measurements?from='+time_before_str(105) + '&to=' + time_before_str(90))

    return data.json()

def get_inverters_list(system_id):
    data = send_cmd('systems/' + system_id + '/inverters')

    return data.json()

def get_inv_abb(system_id, inv_id, abb):
    data = send_cmd('systems/' + system_id + '/inverters/' + inv_id + '/abbreviations/' + abb + '/measurements?from='+time_before_str(105) + '&to=' + time_before_str(90))

    return data.json()

def get_tech_data(system_id):
    data = send_cmd('systems/' + system_id + '/technical-data')

    return data.json()['data']

response = send_cmd('systems')
systems = response.json()['data']
log = ''

def get_radiance():
    global log

    for system in systems:
        if "A" in system['name']:
            response = send_cmd('systems/' + system['key'] + '/basics/abbreviations/G_M0/measurements?from='+ time_before_str(45) + '&to=' + time_before_str(30))
            log = log + str(response.json()['data'])
            return response.json()['data']['G_M0'][0]['value']

for system in systems:
    if "S.D" in system['name']: continue
    print("Refet %s" % system['name'])
    radiance = get_radiance()
    print(log)
    print(radiance)
    exit(1)
    if "A" in system['name']:
        response = send_cmd('systems/' + system['key'] + '/basics/abbreviations/G_M0/measurements?from='+ time_before_str(645) + '&to=' + time_before_str(630))
        print(response.json()['data'])
    continue
    #data = get_tech_data(system['key'])
    #print("Technical data: %s" % data)

    data = get_inverters_list(system['key'])
    #print("Inv list: %s" % data['data'])

    for inv in data['data']:
        abb_data = get_inv_abb(system['key'], inv['id'], 'I_AC')
        print(abb_data['data'])
    continue
    inverter = get_inverters(system['key'])
    print("inverter data XX %s" % inverter)
    for t in inverter:
        for inver_id in inverter[t]:
            print("INV ID %s" % inver_id)
            print(inverter[t][inver_id])

    #if 'efet A' in system['name']:
    #    refetBinv = send_cmd('systems/' + system['key'] + '/basics/bulk/measurements?from='+time_before_str(45) + '&to=' + time_before_str(30))

    #     send_mail(refetBinv.json())
        # Binver = refetBinv.json()['data']
        # print(Binver)

#    response = send_cmd('%s/calculations/bulk/measurements?from=%s&to%s' % (system['key'], time_before_str(60), time_now_str()))
#    print(response.content)
    #print(response.json())
