#!/usr/bin/env python

# Third party library; "pip install requests" if getting import errors.
import requests

# We use JSON to parse tokens and our token file storage.
import json

# We read JWT tokens which are base64 encoded.
import base64

# We check the token expiry time.
import time

class ZEServices:

 # API Gateway.
 servicesHost = 'https://www.services.renault-ze.com'

 # This prevents the requests module from creating its own user-agent.
 #stealthyHeaders = {'User-Agent': None, 'DNT':'1'}

 def __init__(self, user, password):
  # Generate the ZE Services token.
  self.accessToken = self.getAccessToken(user, password)

 def getAccessToken(self, user, password):
   url = ZEServices.servicesHost + '/api/user/login'
   payload = {'username':user, 'password':password}
   api_json = requests.post(url,  json=payload).json()

   # We do not want to save all the user data returned on login, so we create a smaller file of just the mandatory information.
   tokenData = {'token' : api_json['token']}
   # The script will just want the token.
   return api_json['token']

 def apiCall(self, path):
  url = ZEServices.servicesHost + path
  headers = {'Authorization': 'Bearer ' + self.accessToken, 'User-Agent': None}
  return requests.get(url, headers=headers).json()