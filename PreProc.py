
import requests
from flask import Flask, jsonify, make_response
from flask_restful import Api, Resource, reqparse
import csv
import random
import math
import operator
import itertools
import json
from json import dumps
import psycopg2
import psycopg2.extras
from psycopg2._psycopg import DatabaseError
import sys
import datetime
import re

from requests import Timeout, HTTPError, ConnectionError
from Subroutine import get_new_attributes

app = Flask(__name__)
api = Api(app)



class BarAPI(Resource):


    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        # a1 = datetime.datetime.now()
        try:
            r = requests.get('http://localhost:5004/getParam', params=json, timeout=120)
            r.raise_for_status()
            a = datetime.datetime.now()
        except Timeout:
            print ("Timeout Error:")
            return "Timeout Error:"
        except HTTPError:
            print ("HTTPError Error:")
            return "HTTPError Error:"
        except ConnectionError:
            print ("ConnectionError Error:")
            return "ConnectionError Error:"

        # Function for calculating South API response time
        def calculate_response_time(a):
            b = datetime.datetime.now()
            delta = b - a
            time = int(delta.total_seconds() * 1000)
            print("tPreProc %d ms" %time)
            return time  # milliseconds

        try:
            api2_data = r.json().get('@api2')
            responseHeader = api2_data.get('responseHeader')
            returnDescription = r.json().get('retDesc')
            service_id = json.get('serviceID')
        except :
            tPreProc = calculate_response_time(a)
            content = r.content
            if content.__contains__('HTTPError'):
                code = content.split(" ")[1]
            else:
                code = None
            data = {
                'Return_description': 'Failed',
                'Message': r.content,
                'Return_code': code,
            }
            return jsonify(data)
            # data = r.content
            # return data

        if returnDescription == 'Success':

            login_id = r.json().get('custInfo').get('loginId')
            access_port = str(r.json().get('custInfo').get('accessPort'))
            # Package name and Access type
            temp_prt = access_port.split('-')
            new_access_port = temp_prt[0]
            if new_access_port.__contains__('_V'):#new_access_port[4:6] == 'V1':
                access_type = 'VDSL'
            else:
                access_type = 'FTTH'

            rec = r.json().get('lineProfiles')
            if rec:
                pp = rec[0]
                package_name = pp['siebelProfile']
            else:
                package_name = 'No Package Name available.'

            # Parsing for VLAN data and attributes
            trafficProfiles = r.json().get('trafficProfiles')
            attr_rec = r.json().get('attributes')
            # Declaring necessary variables for VLAN
            vlan209_isConfigured = None
            vlan400_isConfigured = None
            vlan500_isConfigured = None
            vlan600_isConfigured = None
            vlan209_isMissing = None
            vlan400_isMissing = None
            vlan500_isMissing = None
            vlan600_isMissing = None
            vln209 = None
            vln400 = None
            vln500 = None
            vln600 = None
            Vlan_209 = ""
            Vlan_400 = ""
            Vlan_500 = ""
            Vlan_600 = ""
            siebelProfileTx = None
            siebelProfileRx = None
            isProfileTxMismatch = False
            isProfileRxMismatch = False
            uploadSpeedProfileStatus = 'Good'
            downloadSpeedProfileStatus = 'Good'

            attributes = r.json().get('attributes')
            ONT_TX_POWER = None
            ONT_RX_POWER = None



            if attributes != None:
                for attr in attributes:
                    print attr
                    if attr.get('tSouthRespond') != None:
                        tSouthRespond = attr.get('tSouthRespond')
                        print "tSouthRespond " + str(tSouthRespond)
                        continue
                    if str(attr.get('name')).__eq__('UPSTREAM_ACTUAL_RATE'):
                        if attr.get('value') != None:
                            UPSTREAM_ACTUAL_RATE = attr.get('value') * 1000.0
                        else:
                            UPSTREAM_ACTUAL_RATE = None
                        continue
                    if str(attr.get('name')).__eq__('DOWNSTREAM_ACTUAL_RATE'):
                        if attr.get('value')!=None:
                            DOWNSTREAM_ACTUAL_RATE = attr.get('value') * 1000.0
                        else:
                            DOWNSTREAM_ACTUAL_RATE = None
                        continue
                    if str(attr.get('name')).__eq__('UPSTREAM_ATTENUATION'):
                        UPSTREAM_ATTENUATION = attr.get('value')
                        continue
                    if str(attr.get('name')).__eq__('DOWNSTREAM_ATTENUATION'):
                        DOWNSTREAM_ATTENUATION = attr.get('value')
                        continue
                    if str(attr.get('name')).__eq__('UPSTREAM_SNR'):
                        UPSTREAM_SNR = attr.get('value')
                        continue
                    if str(attr.get('name')).__eq__('DOWNSTREAM_SNR'):
                        DOWNSTREAM_SNR = attr.get('value')
                        continue
                    if str(attr.get('name')).__eq__('ONT_RX_POWER'):
                        ONT_RX_POWER = attr.get('value')
                        continue
                    if str(attr.get('name')).__eq__('ONT_TX_POWER'):
                        ONT_TX_POWER = attr.get('value')
                        continue
            else:
                # if access_type.__eq__('FTTH'):
                msg = 'Next Best Action (NBA)'
                # else:
                #     msg = 'One or more attributes value missing.'

                final_data = {
                    'Return_description': 'Failed',
                    'Login_id': str(login_id),
                    'Package_name': str(package_name),
                    'Access_type': str(access_type),
                    'Message': msg,
                    'Return_code': 400,
                    'tPreProc': calculate_response_time(a),
                    'tSouthRespond': tSouthRespond,
                }
                return jsonify(final_data)

            if trafficProfiles != None:
                for profile in trafficProfiles:
                    if str(profile.get('vlan')).__eq__('209'):
                        # VLAN209
                        vln209 = profile
                        vlan209_isConfigured = vln209['isConfigured']
                        vlan209_isMissing = vln209['isMissing']
                        continue
                    if str(profile.get('vlan')).__eq__('400'):
                        # VLAN400
                        vln400 = profile
                        vlan400_isConfigured = vln400['isConfigured']
                        vlan400_isMissing = vln400['isMissing']
                        continue
                    if str(profile.get('vlan')).__eq__('500'):
                        # VLAN500
                        vln500 = profile
                        vlan500_isConfigured = vln500['isConfigured']
                        vlan500_isMissing = vln500['isMissing']
                        isProfileTxMismatch = vln500['isProfileTxMismatch']
                        isProfileRxMismatch = vln500['isProfileRxMismatch']

                        siebelProfileTx = vln500['siebelProfileTx']
                        if siebelProfileTx != None:
                            if str(siebelProfileTx).__contains__('M'):
                                unit = 1000000.0;
                            elif str(siebelProfileTx).__contains__('K'):
                                unit = 1000.0;
                            siebelProfileTxVal = float(re.split('M|K', siebelProfileTx)[0]) * unit;

                        configuredProfileTx = vln500['configuredProfileTx']
                        val = str(configuredProfileTx).__contains__('n/a')
                        if configuredProfileTx != None and not(val) :
                            if str(configuredProfileTx).__contains__('M'):
                                unit = 1000000.0;
                            elif str(configuredProfileTx).__contains__('K'):
                                unit = 1000.0;
                            configuredProfileTxVal = float(re.split('M|K', configuredProfileTx)[0]) * unit;

                        siebelProfileRx = vln500['siebelProfileRx']
                        if siebelProfileRx != None:
                            if str(siebelProfileRx).__contains__('M'):
                                unit = 1000000.0;
                            elif str(siebelProfileRx).__contains__('K'):
                                unit = 1000.0;
                            siebelProfileRxVal = float(re.split('M|K', siebelProfileRx)[0]) * unit;

                        configuredProfileRx = vln500['configuredProfileRx']
                        val = str(configuredProfileRx).__contains__('n/a')
                        if configuredProfileRx != None and not(val):
                            if str(configuredProfileRx).__contains__('M'):
                                unit = 1000000.0;
                            elif str(configuredProfileRx).__contains__('K'):
                                unit = 1000.0;
                            configuredProfileRxVal = float(re.split('M|K', configuredProfileRx)[0]) * unit;
                        continue
                    if str(profile.get('vlan')).__eq__('600'):
                        # VLAN600
                        vln600 = profile
                        vlan600_isConfigured = vln600['isConfigured']
                        vlan600_isMissing = vln600['isMissing']
                        continue

            # vlan209_ccs
            if vlan209_isConfigured != None:
                if vlan209_isConfigured:
                    Vlan_209 = str('Enabled')
                elif vlan209_isConfigured == False and vlan209_isMissing == True:
                    Vlan_209 = str('Disabled')
                elif vlan209_isConfigured == False and vlan209_isMissing == False:
                    Vlan_209 = str('Enabled')
            else:
                Vlan_209 = "Enabled"

            # vlan400_vobb
            if vlan400_isConfigured != None:
                if vlan400_isConfigured:
                    Vlan_400 = str('Enabled')
                elif vlan400_isConfigured == False and vlan400_isMissing == True:
                    Vlan_400 = str('Disabled')
                elif vlan400_isConfigured == False and vlan400_isMissing == False:
                    Vlan_400 = str('Enabled')
            else:
                Vlan_400 = "Enabled"

            # vlan500_hsi
            if vlan500_isConfigured != None:
                if vlan500_isConfigured:
                    Vlan_500 = str('Enabled')
                elif vlan500_isConfigured == False and vlan500_isMissing == True:
                    Vlan_500 = str('Disabled')
                    uploadSpeedProfileStatus = 'Bad'
                    downloadSpeedProfileStatus = 'Bad'
                elif vlan500_isConfigured == False and vlan500_isMissing == False:
                    Vlan_500 = str('Enabled')
                    uploadSpeedProfileStatus = 'Good'
                    downloadSpeedProfileStatus = 'Good'

            else:
                Vlan_500 = "Enabled"

            # vlan600_hsi
            if vlan600_isConfigured != None:
                if vlan600_isConfigured:
                    Vlan_600 = str('Enabled')
                elif vlan600_isConfigured == False and vlan600_isMissing == True:
                    Vlan_600 = str('Disabled')
                elif vlan600_isConfigured == False and vlan600_isMissing == False:
                    Vlan_600 = str('Enabled')
            else:
                Vlan_600 = "Enabled"

            print access_type
            print "Vlan_209: " + Vlan_209
            print "Vlan_400: " + Vlan_400
            print "Vlan_500: " + Vlan_500
            print "Vlan_600: " + Vlan_600

            radiusUpload = None
            radiusDownload = None

            if responseHeader.get('hsiService') != None:
                radiusUpload = responseHeader.get('hsiService').get('radiusUpload')
                radiusDownload = responseHeader.get('hsiService').get('radiusDownload')

            if radiusDownload==None or radiusUpload==None or (access_type == 'VDSL' and (UPSTREAM_ACTUAL_RATE==None or DOWNSTREAM_ACTUAL_RATE==None)):
                msg = 'One or more attributes value missing.'
                final_data = {
                    'Return_description': 'Failed',
                    'Login_id': str(login_id),
                    'Package_name': str(package_name),
                    'Access_type': str(access_type),
                    'Message': msg,
                    'Return_code': 400,
                    'tPreProc': calculate_response_time(a),
                    'tSouthRespond': tSouthRespond,
                }

                return jsonify(final_data)


            # Calling the second API and retrieving the data
            rec_data = get_new_attributes(service_id, api2_data)

            if access_type == 'FTTH':

                # Decide Upload and Download Speed Profile
                if vln500 != None and Vlan_500.__eq__('Enabled') :
                    # configuredProfileTx = vln500.get('configuredProfileTx')
                    if configuredProfileTx != None:
                        print "Calculating configuredProfileTx..."
                        if isProfileTxMismatch == False:
                            radiusUploadVal = rec_data.get('radiusUpload')
                            uploadSpeedProfileVal = configuredProfileTxVal / radiusUploadVal
                        else:
                            uploadSpeedProfileVal = siebelProfileTxVal / configuredProfileTxVal
                        if uploadSpeedProfileVal >= 1:
                            uploadSpeedProfileStatus = 'Good'
                        else:
                            uploadSpeedProfileStatus = 'Bad'


                    # configuredProfileRx = vln500.get('configuredProfileRx')
                    if configuredProfileRx != None:
                        print "Calculating configuredProfileRx..."
                        if isProfileRxMismatch == False:
                            radiusDownloadVal = rec_data.get('radiusDownload')
                            downloadSpeedProfileVal = configuredProfileRxVal / radiusDownloadVal

                        else:
                            downloadSpeedProfileVal = siebelProfileRxVal / configuredProfileRxVal

                        if downloadSpeedProfileVal >= 1:
                            downloadSpeedProfileStatus = 'Good'
                        else:
                            downloadSpeedProfileStatus = 'Bad'
                elif vln500 != None and Vlan_500.__eq__('Disabled') :
                    uploadSpeedProfileStatus = 'Bad'
                    downloadSpeedProfileStatus = 'Bad'

                #Decide Physical Uplink and Downlink Status
                # ONT_TX_POWER and ONT_RX_POWER
                # ont_tx_pr = ONT_TX_POWER
                ont_rx_pr = ONT_RX_POWER
                if ont_rx_pr != None:
                    # Physical uplink status
                    if ont_rx_pr >= -28:
                        Physical_uplink_status = str('Good')
                    else:
                        Physical_uplink_status = str('Bad')

                    # Physical downlink status
                    if ont_rx_pr >= -28:
                        Physical_downlink_status = str('Good')
                    else:
                        Physical_downlink_status = str('Bad')

                else:
                    msg = 'One or more attributes value missing.'
                    final_data = {
                        'Return_description': 'Failed',
                        'Login_id': str(login_id),
                        'Package_name': str(package_name),
                        'Access_type': str(access_type),
                        'Message': msg,
                        'Return_code': 400,
                        'tPreProc': calculate_response_time(a),
                        'tSouthRespond': tSouthRespond,
                    }

                    return jsonify(final_data)


            elif access_type == 'VDSL':
                serviceCategory = responseHeader.get("serviceCategory") #responseHeader is from 2nd api
                for service in serviceCategory:
                    productName = service.get("productName")
                    if str(productName).__contains__("Residential High Speed Internet"):
                        serviceUploadSpeedValUnit = service.get("serviceUploadSpeed")
                        if serviceUploadSpeedValUnit != None:
                            print "Calculating serviceUploadSpeed..."
                            if str(serviceUploadSpeedValUnit).__contains__('M'):
                                unit = 1000000.0;
                            elif str(serviceUploadSpeedValUnit).__contains__('K'):
                                unit = 1000.0;
                            serviceUploadSpeedVal = float(re.split('M|K', serviceUploadSpeedValUnit)[0]) * unit
                            uploadSpeedProfileVal = UPSTREAM_ACTUAL_RATE / serviceUploadSpeedVal
                            if uploadSpeedProfileVal >= 1:
                                uploadSpeedProfileStatus = 'Good'
                            else:
                                uploadSpeedProfileStatus = 'Bad'

                        serviceDownloadSpeedValUnit = service.get("serviceDownloadSpeed")
                        if serviceDownloadSpeedValUnit != None:
                            print "Calculating serviceDownloadSpeed..."
                            if str(serviceDownloadSpeedValUnit).__contains__('M'):
                                unit = 1000000.0;
                            elif str(serviceDownloadSpeedValUnit).__contains__('K'):
                                unit = 1000.0;
                            serviceDownloadSpeedVal = float(re.split('M|K', serviceDownloadSpeedValUnit)[0]) * unit
                            downloadSpeedProfileVal = DOWNSTREAM_ACTUAL_RATE / serviceDownloadSpeedVal
                            if downloadSpeedProfileVal >= 1:
                                downloadSpeedProfileStatus = 'Good'
                            else:
                                downloadSpeedProfileStatus = 'Bad'
                        break

                upstream_attn = UPSTREAM_ATTENUATION  # attr_rec[20]['value']
                upstream_snr = UPSTREAM_SNR  # attr_rec[24]['value']
                downstream_attn = DOWNSTREAM_ATTENUATION  # attr_rec[5]['value']
                downstream_snr = DOWNSTREAM_SNR  # attr_rec[9]['value']

                # Physical up-link status
                if upstream_attn != None and upstream_snr !=None:
                    if upstream_attn <= 20 and upstream_snr >= 8:
                        Physical_uplink_status = 'Good'
                    else:
                        Physical_uplink_status = 'Bad'
                elif upstream_attn != None or upstream_snr !=None:
                    if upstream_snr !=None:
                        if upstream_snr >= 8:
                            Physical_uplink_status = 'Good'
                        else:
                            Physical_uplink_status = 'Bad'
                    elif upstream_attn != None:
                        if upstream_attn <= 20:
                            Physical_uplink_status = 'Good'
                        else:
                            Physical_uplink_status = 'Bad'

                else:
                    Physical_uplink_status = 'Good'

                # Physical down-link status
                if downstream_attn != None and downstream_snr !=None:
                    if downstream_attn <= 20 and downstream_snr >= 8:
                        Physical_downlink_status = 'Good'
                    else:
                        Physical_downlink_status = 'Bad'
                elif downstream_attn != None or downstream_snr !=None:
                    if downstream_snr !=None:
                        if downstream_snr >= 8:
                            Physical_downlink_status = 'Good'
                        else:
                            Physical_downlink_status = 'Bad'
                    elif downstream_attn != None:
                        if downstream_attn <= 20:
                            Physical_downlink_status = 'Good'
                        else:
                            Physical_downlink_status = 'Bad'

                else:
                    Physical_downlink_status = 'Good'

            # Final data to send to ML API (local_engine2)
            final_data = {
                'Return_description': 'Success',
                'Login_id': str(login_id),
                'Package_name': str(package_name),
                'Access_type': str(access_type),
                'Device_host_name': str(rec_data['device_host_name']),
                'HSI_billing_status': str(rec_data['hsi_billing_status']),
                'Radius_account_status': str(rec_data['radius_account_status']),
                'HSI_session': str(rec_data['hsi_session']),
                'Frequent_disconnect': rec_data['frequent_disconnect'],
                'Neighbouring_session': rec_data['neighbouring_session'],
                'Upload_speed_profile': uploadSpeedProfileStatus,
                'Download_speed_profile': downloadSpeedProfileStatus,
                'Vlan_209': Vlan_209,
                'Vlan_400': Vlan_400,
                'Vlan_500': Vlan_500,
                'Vlan_600': Vlan_600,
                'Physical_uplink_status': Physical_uplink_status,
                'Physical_downlink_status': Physical_downlink_status,
                'Message': "13 attributes",
                'tPreProc': calculate_response_time(a),
                'tSouthRespond': tSouthRespond
            }

            print 'Upload_speed_profile: ' + uploadSpeedProfileStatus
            print 'Download_speed_profile: ' + downloadSpeedProfileStatus
            print 'Physical_uplink_status:' + Physical_uplink_status
            print 'Physical_downlink_status:' + Physical_downlink_status
            print final_data

            return jsonify(final_data)
        # If SPANMS return is unsuccessful this part of the code will execute
        else:
            tPreProc = calculate_response_time(a)
            data = r.json()
            data['attributes'].append({'tPreProc': tPreProc})
            data['Return_description'] = 'Failed'
            data['Message'] = r.json().get('retDesc')
            return jsonify(data)



api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret2a'
    # app.run('127.0.0.1', 5003, True)
    app.run('0.0.0.0', 5002, True, threaded=True)