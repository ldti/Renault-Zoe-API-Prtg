#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Support Python3 in Python2.
from __future__ import print_function

# All the shared functions are in this package.
from shared.zeservices import ZEServices
from shared.myrenault import MYRenault
from paepy.ChannelDefinition import CustomSensorResult

# This script makes heavy use of JSON parsing.
import json

# We check whether we are running on Windows or not.
import sys

# We play with encodings so it's good to check what we are set to support.
import locale
import time

# Constants.
#kmToMiles  = 0.621371

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

battery = zeServices_json['charge_level']
remaining_range = zeServices_json['remaining_range']
charging = zeServices_json['charging']
pluggedIn = zeServices_json['plugged']
ChargeMode = zeServices_json['charging_point']
updateTime = zeServices_json['last_update']
if charging: remaining_time = zeServices_json['remaining_time'] if 'remaining_time' in zeServices_json else None

# (Optionally) Create a MY Renault object.
if 'MyRenaultEmail' in credentials and 'MyRenaultPassword' in credentials:
 myRenault = MYRenault(credentials['MyRenaultEmail'], credentials['MyRenaultPassword'])

 # MY Renault vehicle status.
 myRenault_json = myRenault.apiCall()

 # We allow the MY Renault section to fail gracefully (if it cannot find our VIN).
 totalMileage     = 0

 # Go looking for the specific VIN we have requested.
 for car in myRenault_json['owned']:
  if car['vin'] == vin:
   totalMileage     = car['mileage']
   if 'MyRenaultMileageOffset' in credentials: totalMileage += credentials['MyRenaultMileageOffset']
   lastMileageRefresh = car['lastMileageRefresh']
   break
else:
 # We allow the MY Renault section to fail gracefully (if we have not set it up).
 totalMileage     = 0

# Check the Windows console can display UTF-8 characters.
#if sys.platform != 'win32' or locale.getpreferredencoding() == 'cp65001':
 # Generate the UTF-8 status (with emojis).
# status  = u'\n?? ' + str(battery) + '%'
# status += u'\n?? ' + str('%.0f' % round(remaining_range)) + ' KM'
# status += u'\n?? ' + ('Plugged in' if pluggedIn else 'Unplugged')
# status += u'\n? ' + ('Charging ' + ('(' + str(remaining_time) + ' minutes remain)' if remaining_time is not None else '') if charging else 'Not charging')
# if totalMileage > 0: status += u'\n??? ' + str(totalMileage) + ' KM (since ' + lastMileageRefresh + ')'
#else:
 # Generate the ASCII standard text status.
# status  = '\nBattery: ' + str(battery) + '%'
# status += '\nRange: ' + str('%.0f' % round(remaining_range)) + ' KM'
# status += '\nPlugged In: ' + ('Plugged in' if pluggedIn else 'Unplugged')
# status += '\nCharging: ' + ('Charging ' + ('(' + str(remaining_time) + ' minutes remain)' if remaining_time is not None else '') if charging else 'Not charging')
# if totalMileage > 0: status += u'\nMileage: ' + str(totalMileage) + ' KM (since ' + lastMileageRefresh + ')'

#print(status)

if __name__ == "__main__":

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