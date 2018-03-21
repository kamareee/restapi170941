
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
            r = requests.get('http://localhost:5003/getParam', params=json, timeout=120)
            r.raise_for_status()
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
        def calculate_response_time():
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
            data = r.content
            return data

        a = datetime.datetime.now()

        attributes = r.json().get('attributes')
        ONT_TX_POWER = None
        ONT_RX_POWER = None
        for attr in attributes:
            print attr
            if attr.get('tSouthRespond') != None:
                tSouthRespond = attr.get('tSouthRespond')
                print "tSouthRespond " + str(tSouthRespond)
                continue
            if str(attr.get('name')).__eq__('UPSTREAM_ACTUAL_RATE'):
                UPSTREAM_ACTUAL_RATE = attr.get('value') * 1000.0
                continue
            if str(attr.get('name')).__eq__('DOWNSTREAM_ACTUAL_RATE'):
                DOWNSTREAM_ACTUAL_RATE = attr.get('value') * 1000.0
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


        if returnDescription == 'Success':
            # Calling the second API and retrieving the data
            rec_data = get_new_attributes(service_id, api2_data)
            login_id = r.json().get('custInfo').get('loginId')
            access_port = str(r.json().get('custInfo').get('accessPort'))
            # Package name and Access type
            temp_prt = access_port.split('-')
            new_access_port = temp_prt[0]
            if new_access_port.__contains__('V1'):#new_access_port[4:6] == 'V1':
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
            vlan209_isConfigured = ''
            vlan400_isConfigured = ''
            vlan500_isConfigured = ''
            vlan600_isConfigured = ''
            if trafficProfiles != None:
                for profile in trafficProfiles:
                    if str(profile.get('vlan')).__eq__('209'):
                        # VLAN209
                        vln209 = profile
                        vlan209_isConfigured = vln209['isConfigured']
                        continue
                    if str(profile.get('vlan')).__eq__('400'):
                        # VLAN400
                        vln400 = profile
                        vlan400_isConfigured = vln400['isConfigured']
                        continue
                    if str(profile.get('vlan')).__eq__('500'):
                        # VLAN500
                        vln500 = profile
                        vlan500_isConfigured = vln500['isConfigured']
                        continue
                    if str(profile.get('vlan')).__eq__('600'):
                        # VLAN600
                        vln600 = profile
                        vlan600_isConfigured = vln600['isConfigured']
                        continue
            else:
                vlan209_isConfigured = True
                vlan400_isConfigured = True
                vlan500_isConfigured = True
                vlan600_isConfigured = True


            # ONT_TX_POWER and ONT_RX_POWER
            ont_tx_pr = ONT_TX_POWER#attr_rec[13]['value']
            ont_rx_pr = ONT_RX_POWER#attr_rec[12]['value']



            if access_type == 'FTTH':
                configuredProfileTx = vln500.get('configuredProfileTx')
                configuredProfileTx_unit = configuredProfileTx.split('_')[0]
                if str(configuredProfileTx_unit).__contains__('M'):
                    unit = 1000000.0;
                elif str(configuredProfileTx_unit).__contains__('K'):
                    unit = 1000.0;
                configuredProfileTxVal = float(re.split('M|K', configuredProfileTx_unit)[0]) * unit;#float(configuredProfileTx.split('_')[0].split('M')[0])

                configuredProfileRx = vln500.get('configuredProfileRx')
                configuredProfileRx_unit = configuredProfileRx.split('_')[0]
                if str(configuredProfileRx_unit).__contains__('M'):
                    unit = 1000000.0;
                elif str(configuredProfileRx_unit).__contains__('K'):
                    unit = 1000.0;
                configuredProfileRxVal = float(re.split('M|K', configuredProfileRx_unit)[0]) * unit;#float(configuredProfileRx.split('_')[0].split('M')[0])

                radiusUploadVal = rec_data.get('radiusUpload')
                radiusDownloadVal = rec_data.get('radiusDownload')
                uploadSpeedProfileVal = configuredProfileTxVal/radiusUploadVal
                downloadSpeedProfileVal = configuredProfileRxVal/radiusDownloadVal
                if uploadSpeedProfileVal >= 1:
                    uploadSpeedProfileStatus = 'Good'
                else:
                    uploadSpeedProfileStatus = 'Bad'

                if downloadSpeedProfileVal >= 1:
                    downloadSpeedProfileStatus = 'Good'
                else:
                    downloadSpeedProfileStatus = 'Bad'

                if (ont_tx_pr is None or ont_rx_pr is None):
                    final_data = {
                        'Login_id': str(login_id),
                        'Package_name': str(package_name),
                        'Access_type': str(access_type),
                        'Message': str('Missing physical uplink or downlink data'),
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond,
                    }
                    return jsonify(final_data)
                elif trafficProfiles == None:

                    # Physical up-link status
                    if ont_tx_pr >= -28:
                        dt1 = str('Good')
                    else:
                        dt1 = str('Bad')

                    # Physical down-link status
                    if ont_rx_pr >= -28:
                        dt2 = str('Good')
                    else:
                        dt2 = str('Bad')
                    final_data = {
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
                        'Vlan_209': "Enabled",
                        'Vlan_400': "Enabled",
                        'Vlan_500': "Enabled",
                        'Vlan_600': "Enabled",
                        'Physical_uplink_status': str(dt1),
                        'Physical_downlink_status': str(dt2),
                        'Message': "13 attributes",
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond
                    }
                    return jsonify(final_data)
                elif len(trafficProfiles) == 4:

                    # vlan209_ccs
                    if bool(vlan209_isConfigured):
                        dt1 = str('Enabled')
                    else:
                        dt1 = str('Disabled')

                    # vlan400_vobb
                    if bool(vlan400_isConfigured):
                        dt2 = str('Enabled')
                    else:
                        dt2 = str('Disabled')

                    # vlan500_hsi
                    if bool(vlan500_isConfigured):
                        dt3 = str('Enabled')
                    else:
                        dt3 = str('Disabled')

                    # vlan600_iptv
                    if bool(vlan600_isConfigured):
                        dt4 = str('Enabled')
                    else:
                        dt4 = str('Disabled')

                    # Physical up-link status
                    if ont_tx_pr >= -28:
                        dt5 = str('Good')
                    else:
                        dt5 = str('Bad')

                    # Physical down-link status
                    if ont_rx_pr >= -28:
                        dt6 = str('Good')
                    else:
                        dt6 = str('Bad')

                    # Final data to send to ML API (local_engine2)
                    final_data = {
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
                        'Vlan_209': str(dt1),
                        'Vlan_400': str(dt2),
                        'Vlan_500': str(dt3),
                        'Vlan_600': str(dt4),
                        'Physical_uplink_status': str(dt5),
                        'Physical_downlink_status': str(dt6),
                        'Message': "13 attributes",
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond
                    }

                    return jsonify(final_data)
                elif len(trafficProfiles)==3:
                    # vlan209_ccs
                    if bool(vlan209_isConfigured):
                        dt1 = str('Enabled')
                    else:
                        dt1 = str('Disabled')

                    # vlan400_vobb
                    if bool(vlan400_isConfigured):
                        dt2 = str('Enabled')
                    else:
                        dt2 = str('Disabled')

                    # vlan500_hsi
                    if bool(vlan500_isConfigured):
                        dt3 = str('Enabled')
                    else:
                        dt3 = str('Disabled')

                    # Physical uplink status
                    if ont_tx_pr >= -28:
                        dt4 = str('Good')
                    else:
                        dt4 = str('Bad')

                    # Physical downlink status
                    if ont_rx_pr >= -28:
                        dt5 = str('Good')
                    else:
                        dt5 = str('Bad')

                    # Final data to send to ML API (local_engine2)
                    final_data = {
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
                        'Vlan_209': str(dt1),
                        'Vlan_400': str(dt2),
                        'Vlan_500': str(dt3),
                        'Physical_uplink_status': str(dt4),
                        'Physical_downlink_status': str(dt5),
                        'Message': "13 attributes",
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond
                    }

                    return jsonify(final_data)
            elif access_type == 'VDSL':
                serviceCategory = responseHeader.get("serviceCategory") #responseHeader is from 2nd api
                for service in serviceCategory:
                    productName = service.get("productName")
                    if str(productName).__contains__("Residential High Speed Internet"):
                        serviceUploadSpeedValUnit = service.get("serviceUploadSpeed")
                        if str(serviceUploadSpeedValUnit).__contains__('M'):
                            unit = 1000000.0;
                        elif str(serviceUploadSpeedValUnit).__contains__('K'):
                            unit = 1000.0;
                        serviceUploadSpeedVal = float(re.split('M|K', serviceUploadSpeedValUnit)[0]) * unit

                        serviceDownloadSpeedValUnit = service.get("serviceDownloadSpeed")
                        if str(serviceDownloadSpeedValUnit).__contains__('M'):
                            unit = 1000000.0;
                        elif str(serviceDownloadSpeedValUnit).__contains__('K'):
                            unit = 1000.0;
                        serviceDownloadSpeedVal = float(re.split('M|K', serviceDownloadSpeedValUnit)[0]) * unit
                        break

                uploadSpeedProfileVal = UPSTREAM_ACTUAL_RATE / serviceUploadSpeedVal
                downloadSpeedProfileVal = DOWNSTREAM_ACTUAL_RATE / serviceDownloadSpeedVal
                if uploadSpeedProfileVal >= 1:
                    uploadSpeedProfileStatus = 'Good'
                else:
                    uploadSpeedProfileStatus = 'Bad'

                if downloadSpeedProfileVal >= 1:
                    downloadSpeedProfileStatus = 'Good'
                else:
                    downloadSpeedProfileStatus = 'Bad'

                if trafficProfiles == None:  # len(traffic_rec) == 0:
                    upstream_attn = UPSTREAM_ATTENUATION  # attr_rec[20]['value']
                    upstream_snr = UPSTREAM_SNR  # attr_rec[24]['value']
                    downstream_attn = DOWNSTREAM_ATTENUATION  # attr_rec[5]['value']
                    downstream_snr = DOWNSTREAM_SNR  # attr_rec[9]['value']

                    # Physical up-link status
                    if upstream_attn <= 20 or upstream_attn is None:
                        if upstream_snr >= 8 or upstream_snr is None:
                            dt1 = str('Good')
                        else:
                            dt1 = str('Bad')
                    else:
                        dt1 = str('Bad')

                    # Physical down-link status
                    if downstream_attn <= 20 or downstream_attn is None:
                        if downstream_snr >= 8 or downstream_snr is None:
                            dt2 = str('Good')
                        else:
                            dt2 = str('Bad')
                    else:
                        dt2 = str('Bad')
                        # Final data to send to ML API (local_engine2)
                        final_data = {
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
                            'Vlan_209': "Enabled",
                            'Vlan_400': "Enabled",
                            'Vlan_500': "Enabled",
                            'Vlan_600': "Enabled",
                            'Physical_uplink_status': str(dt1),
                            'Physical_downlink_status': str(dt2),
                            'Message': "13 attributes",
                            'tPreProc': calculate_response_time(),
                            'tSouthRespond': tSouthRespond
                        }

                        return jsonify(final_data)

                elif len(trafficProfiles) == 4:
                    upstream_attn = UPSTREAM_ATTENUATION  # attr_rec[20]['value']
                    upstream_snr = UPSTREAM_SNR  # attr_rec[24]['value']
                    downstream_attn = DOWNSTREAM_ATTENUATION  # attr_rec[5]['value']
                    downstream_snr = DOWNSTREAM_SNR  # attr_rec[9]['value']

                    # vlan209_ccs
                    if bool(vlan209_isConfigured):
                        dt1 = str('Enabled')
                    else:
                        dt1 = str('Disabled')

                    # vlan400_vobb
                    if bool(vlan400_isConfigured):
                        dt2 = str('Enabled')
                    else:
                        dt2 = str('Disabled')

                    # vlan500_hsi
                    if bool(vlan500_isConfigured):
                        dt3 = str('Enabled')
                    else:
                        dt3 = str('Disabled')

                    # vlan600_iptv
                    if bool(vlan600_isConfigured):
                        dt4 = str('Enabled')
                    else:
                        dt4 = str('Disabled')

                    # Physical up-link status
                    if upstream_attn <= 20 or upstream_attn is None:
                        if upstream_snr >= 8 or upstream_snr is None:
                            dt5 = str('Good')
                        else:
                            dt5 = str('Bad')
                    else:
                        dt5 = str('Bad')

                    # Physical down-link status
                    if downstream_attn <= 20 or downstream_attn is None:
                        if downstream_snr >= 8 or downstream_snr is None:
                            dt6 = str('Good')
                        else:
                            dt6 = str('Bad')
                    else:
                        dt6 = str('Bad')

                    # Final data to send to ML API (local_engine2)
                    final_data = {
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
                        'Vlan_209': str(dt1),
                        'Vlan_400': str(dt2),
                        'Vlan_500': str(dt3),
                        'Vlan_600': str(dt4),
                        'Physical_uplink_status': str(dt5),
                        'Physical_downlink_status': str(dt6),
                        'Message': "13 attributes",
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond
                    }

                    return jsonify(final_data)
                elif len(trafficProfiles) == 3:
                    upstream_attn = UPSTREAM_ATTENUATION  # attr_rec[20]['value']
                    upstream_snr = UPSTREAM_SNR  # attr_rec[24]['value']
                    downstream_attn = DOWNSTREAM_ATTENUATION  # attr_rec[5]['value']
                    downstream_snr = DOWNSTREAM_SNR  # attr_rec[9]['value']

                    # vlan209_ccs
                    if bool(vlan209_isConfigured):
                        dt1 = str('Enabled')
                    else:
                        dt1 = str('Disabled')

                    # vlan400_vobb
                    if bool(vlan400_isConfigured):
                        dt2 = str('Enabled')
                    else:
                        dt2 = str('Disabled')

                    # vlan500_hsi
                    if bool(vlan500_isConfigured):
                        dt3 = str('Enabled')
                    else:
                        dt3 = str('Disabled')

                    # Physical up-link status
                    if upstream_attn <= 20 or upstream_attn is None:
                        if upstream_snr >= 8 or upstream_snr is None:
                            dt4 = str('Good')
                        else:
                            dt4 = str('Bad')
                    else:
                        dt4 = str('Bad')

                    # Physical down-link status
                    if downstream_attn <= 20 or downstream_attn is None:
                        if downstream_snr >= 8 or downstream_snr is None:
                            dt5 = str('Good')
                        else:
                            dt5 = str('Bad')
                    else:
                        dt5 = str('Bad')
                    # Final data to send to ML API (local_engine2)
                    final_data = {
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
                        'Vlan_209': "Enabled",
                        'Vlan_400': "Enabled",
                        'Vlan_500': "Enabled",
                        'Vlan_600': "Enabled",
                        'Physical_uplink_status': str(dt4),
                        'Physical_downlink_status': str(dt5),
                        'Message': "13 attributes",
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond
                    }

                    return jsonify(final_data)




        # If SPANMS return is unsuccessful this part of the code will execute
        else:
            tPreProc = calculate_response_time()
            data = r.json()
            data['attributes'].append({u'tPreProc': tPreProc})
            return jsonify(data)



api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret2a'
    # app.run('127.0.0.1', 5003, True)
    app.run('0.0.0.0', 5002, True, threaded=True)