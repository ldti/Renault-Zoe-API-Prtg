#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Support Python3 in Python2.
from __future__ import print_function

# All the shared functions are in this package.
from shared.zeservices import ZEServices
from paepy.ChannelDefinition import CustomSensorResult

# This script makes heavy use of JSON parsing.
import json

# We check whether we are running on Windows or not.
import sys

# We play with encodings so it's good to check what we are set to support.
import locale
import time

# Load credentials.
in_file = open('C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python\credentials.json', 'r')
credentials = json.load(in_file)
in_file.close()

# Get the VIN.
vin = credentials['VIN']

# Create a ZE Services object.
zeServices = ZEServices(credentials['ZEServicesUsername'], credentials['ZEServicesPassword'])

# ZE Services vehicle status.
zeServices_json = zeServices.apiCall('/api/vehicle/' + vin + '/battery')

battery          = zeServices_json['charge_level']
remaining_range  = zeServices_json['remaining_range']
charging         = zeServices_json['charging']
pluggedIn        = zeServices_json['plugged']
updateTime       = zeServices_json['last_update']
if charging: remaining_time = zeServices_json['remaining_time'] if 'remaining_time' in zeServices_json else None

result = CustomSensorResult()

    # add primary channel
result.add_channel(channel_name="Battery Percentage", unit="Percent", value=battery , primary_channel=True)
    # add additional channel
result.add_channel(channel_name="Range", unit="KM" , value=remaining_range)
    # add additional channel
result.add_channel(channel_name="Charging", value=charging)
    # add additional channel
result.add_channel(channel_name="Plugged In", value=pluggedIn)
    # print sensor result to std
print(result.get_json_result())