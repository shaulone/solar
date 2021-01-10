#!/usr/bin/python3

import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime, timedelta
import pytz

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
# time = datetime.now(tz).replace(microsecond=0).isoformat()
#     time = time.replace(':', '%3A')
#     time = time.replace('+', '%2B')
#     return time

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

# time = time_now_str()
# print(time)
# time = time.replace(':', '%3A')
# time = time.replace('+', '%2B')
# print(time)
# exit()

response = send_cmd('systems')
systems = response.json()['data']
print("111")
print(systems)
print("2222")

for system in systems:
    print("system = %s" % system)
    if 'efet A' in system['name']:
        print('333')
        refetBinv = send_cmd('systems/' + system['key'] + '/basics/abbreviations')
        abbr = refetBinv.json()
        for x in abbr['data']:
            refetBinv = send_cmd('systems/' + system['key'] + '/basics/abbreviations/%s' % x)
            print(refetBinv.json()['data'])

        refetBinv = send_cmd('systems/' + system['key'] + '/basics/bulk/measurements?from='+time_before_str(45) + '&to=' + time_before_str(30))

        print(refetBinv.json())
        # Binver = refetBinv.json()['data']
        # print(Binver)

#    response = send_cmd('%s/calculations/bulk/measurements?from=%s&to%s' % (system['key'], time_before_str(60), time_now_str()))
#    print(response.content)
    #print(response.json())
