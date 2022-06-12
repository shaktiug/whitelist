#!/usr/bin/python3
import sys
import os
from pprint import pprint

import adal
import json
import requests
from requests import get

from colorama import init
init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('WHITELIST!', font='slant'))


import argparse

parser = argparse.ArgumentParser(description='Whitelist Tool')
parser.add_argument("-e", "--env", help="Runs script on the selected env. Possible values are: dev/qa/qa1/uat.", required=True )
parser.add_argument("-n", "--name", help="Please provide your firstname in lowercase. Sets rule name.", required=True)
args = parser.parse_args()


if args.name not in [ "shakti", "mayur", "prabhjot" ,"garima" ]:
    print("Sorry! You are not authorized to run this tool.\nPlease get your access from Shakti\n")
    sys.exit(1)

user_ip = get('https://api.ipify.org').content.decode('utf8')

if user_ip == '14.140.116.145':
     print(f"................IP {user_ip} is already whitelisted. Please disconnect the VPN and try again..................")
     sys.exit(1)

env = {"dev": "beoecomdevfewa", "qa": "beoecomqafewa", "qa1": "beoecomqa1fewa", "uat": "beoecomuatnginxbocomfewa", "stage": "beoecomstagenginxbocomfewa"}
#env = { "dev" : "beoecomdevcachemanagerbewa" }

for k, v in env.items():
    if k == args.env:
        env = env[k]

tenant = ""
authority_url = 'https://login.microsoftonline.com/' + tenant
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
resource = 'https://management.azure.com/'
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(resource, client_id, client_secret)
headers = {'Authorization': 'Bearer ' + token['accessToken'], 'Content-Type': 'application/json'}
params = {'api-version': '2018-02-01'}
if args.env == "stage":
    url = 'YOURSUBSCRIPTIONURL' + str(
    env) + '/config/web'
else:
    print("else block")
    url = 'YOURSUBSCRIPTIONURL' + str(
    env) + '/config/web'

r = requests.get(url, headers=headers, params=params)
result = r.json()
#pprint(result)

c_payload = (result['properties']['ipSecurityRestrictions'])
#pprint(c_payload)

list_of_all_ip = [value for elem in c_payload
                      for value in elem.values()]

if user_ip + '/32' in list_of_all_ip:
    print(f"IPAddress : '{user_ip}' already exists.")
    sys.exit(1)

for i in range(len(c_payload)):
    if c_payload[i]['name'] in args.name:
        print(f"Rule : {args.name} already exists. Checking IP Address if not already present, new ip address will be updated")
        del c_payload[i]
        break

payload = {"properties": {"ipSecurityRestrictions": []}}

for i in c_payload:
    payload["properties"]["ipSecurityRestrictions"].append(i)

def fill_ipinfo():
    ip = {}
    ip["ipAddress"] = user_ip + "/32"
    ip["action"] = "Allow"
    ip["tag"] = "Default"
    ip["priority"] = "90"
    ip["name"] = args.name
    add_ip(ip)


def add_ip(ip):
    payload["properties"]["ipSecurityRestrictions"].append(ip)

fill_ipinfo()
payload = json.dumps(payload)
#print(payload)

set_ip = requests.patch(url, data=payload, headers=headers, params=params)
#print(set_ip.json())
print(f"Rule with name {args.name} and IPAddress: {user_ip} updated.\nThanks for using Whitelist tool")
