
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
        # delta = a - a1;
        # print delta
        # tLinkEngineSouth = int(delta.total_seconds() * 1000)  # miliseconds

        attributes = r.json().get('attributes')
        for attr in attributes:
            print attr
            if attr.get('tSouthRespond') != None:
                tSouthRespond = attr.get('tSouthRespond')
                print tSouthRespond

        if returnDescription == 'Success':
            login_id = r.json().get('custInfo').get('loginId')
            access_port = str(r.json().get('custInfo').get('accessPort'))
            # Package name and Access type
            temp_prt = access_port.split('-')
            new_access_port = temp_prt[0]
            rec = r.json().get('lineProfiles')
            if rec:
                pp = rec[0]
                package_name = pp['siebelProfile']
            else:
                package_name = 'No Package Name available.'

            if new_access_port[4:6] == 'V1':
                access_type = 'VDSL'
            else:
                access_type = 'FTTH'

            # Parsing for VLAN data and attributes
            traffic_rec = r.json().get('trafficProfiles')
            attr_rec = r.json().get('attributes')

            # Declaring necessary variables for VLAN
            stat_vlan209 = ''
            stat_vlan400 = ''
            stat_vlan500 = ''
            stat_vlan600 = ''

            # OLT_TX_POWER and OLT_RX_POWER
            olt_tx_pr = attr_rec[13]['value']
            olt_rx_pr = attr_rec[12]['value']

            # UPSTREAM_ACTUAL_RATE and DOWNSTREAM_ACTUAL_RATE
            upstream_act_rate = 10  # change later
            downstream_act_rate = 20  # change later

            # Calling the second API and retrieving the data
            rec_data = get_new_attributes(service_id, upstream_act_rate, downstream_act_rate, api2_data)

            if len(traffic_rec) is 4:
                # VLAN209
                vln1 = traffic_rec[0]
                stat_vlan209 = vln1['isConfigured']

                # VLAN400
                vln2 = traffic_rec[1]
                stat_vlan400 = vln2['isConfigured']

                # VLAN500
                vln3 = traffic_rec[2]
                stat_vlan500 = vln3['isConfigured']

                # VLAN600
                vln4 = traffic_rec[3]
                stat_vlan600 = vln4['isConfigured']

            elif len(traffic_rec) is 3:
                # VLAN209
                vln1 = traffic_rec[0]
                stat_vlan209 = vln1['isConfigured']

                # VLAN400
                vln2 = traffic_rec[1]
                stat_vlan400 = vln2['isConfigured']

                # VLAN500
                vln3 = traffic_rec[2]
                stat_vlan500 = vln3['isConfigured']

            if access_type == 'FTTH' and (olt_tx_pr is None or olt_rx_pr is None):
                final_data = {
                    'Login_id': str(login_id),
                    'Package_name': str(package_name),
                    'Access_type': str(access_type),
                    'Message': str('Missing physical uplink or downlink data'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                }

                return jsonify(final_data)
            elif access_type == 'FTTH' and len(traffic_rec) == 0:

                # Physical up-link status
                if olt_tx_pr >= -28:
                    dt1 = str('Good')
                else:
                    dt1 = str('Bad')

                # Physical down-link status
                if olt_rx_pr >= -28:
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
                    'Upload_speed_profile': '',
                    'Download_speed_profile': '',
                    'Physical_uplink_status': str(dt1),
                    'Physical_downlink_status': str(dt2),
                    'Message': str('No VLAN data'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                    'No_of_variable': 9
                }
                return jsonify(final_data)

            elif access_type == 'VDSL' and len(traffic_rec) == 0:
                upstream_attn = attr_rec[20]['value']
                upstream_snr = attr_rec[23]['value']
                downstream_attn = attr_rec[5]['value']
                downstream_snr = attr_rec[9]['value']

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
                        'Upload_speed_profile': '',
                        'Download_speed_profile': '',
                        'Physical_uplink_status': str(dt1),
                        'Physical_downlink_status': str(dt2),
                        'Message': str('No VLAN data'),
                        'tPreProc': calculate_response_time(),
                        'tSouthRespond': tSouthRespond,
                        'No_of_attributes': 9
                    }

                    return jsonify(final_data)

            elif access_type == 'VDSL' and len(traffic_rec) == 4:
                upstream_attn = attr_rec[20]['value']
                upstream_snr = attr_rec[23]['value']
                downstream_attn = attr_rec[5]['value']
                downstream_snr = attr_rec[9]['value']

                # vlan209_ccs
                if bool(stat_vlan209):
                    dt1 = str('Enabled')
                else:
                    dt1 = str('Disabled')

                # vlan400_vobb
                if bool(stat_vlan400):
                    dt2 = str('Enabled')
                else:
                    dt2 = str('Disabled')

                # vlan500_hsi
                if bool(stat_vlan500):
                    dt3 = str('Enabled')
                else:
                    dt3 = str('Disabled')

                # vlan600_iptv
                if bool(stat_vlan600):
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
                    'Upload_speed_profile': '',
                    'Download_speed_profile': '',
                    'Vlan_209': str(dt1),
                    'Vlan_400': str(dt2),
                    'Vlan_500': str(dt3),
                    'Vlan_600': str(dt4),
                    'Physical_uplink_status': str(dt5),
                    'Physical_downlink_status': str(dt6),
                    'Message': str('OK'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                    'No_of_attributes': 13
                }

                return jsonify(final_data)

            elif access_type == 'FTTH' and len(traffic_rec) == 4:

                # vlan209_ccs
                if bool(stat_vlan209):
                    dt1 = str('Enabled')
                else:
                    dt1 = str('Disabled')

                # vlan400_vobb
                if bool(stat_vlan400):
                    dt2 = str('Enabled')
                else:
                    dt2 = str('Disabled')

                # vlan500_hsi
                if bool(stat_vlan500):
                    dt3 = str('Enabled')
                else:
                    dt3 = str('Disabled')

                # vlan600_iptv
                if bool(stat_vlan600):
                    dt4 = str('Enabled')
                else:
                    dt4 = str('Disabled')

                # Physical up-link status
                if olt_tx_pr >= -28:
                    dt5 = str('Good')
                else:
                    dt5 = str('Bad')

                # Physical down-link status
                if olt_rx_pr >= -28:
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
                    'Upload_speed_profile': '',
                    'Download_speed_profile': '',
                    'Vlan_209': str(dt1),
                    'Vlan_400': str(dt2),
                    'Vlan_500': str(dt3),
                    'Vlan_600': str(dt4),
                    'Physical_uplink_status': str(dt5),
                    'Physical_downlink_status': str(dt6),
                    'Message': str('OK'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                    'No_of_attributes': 13
                }

                return jsonify(final_data)


            elif access_type == 'VDSL' and len(traffic_rec) == 3:
                upstream_attn = attr_rec[20]['value']
                upstream_snr = attr_rec[23]['value']
                downstream_attn = attr_rec[5]['value']
                downstream_snr = attr_rec[9]['value']

                # vlan209_ccs
                if bool(stat_vlan209):
                    dt1 = str('Enabled')
                else:
                    dt1 = str('Disabled')

                # vlan400_vobb
                if bool(stat_vlan400):
                    dt2 = str('Enabled')
                else:
                    dt2 = str('Disabled')

                # vlan500_hsi
                if bool(stat_vlan500):
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
                    'Upload_speed_profile': '',
                    'Download_speed_profile': '',
                    'Vlan_209': str(dt1),
                    'Vlan_400': str(dt2),
                    'Vlan_500': str(dt3),
                    'Physical_uplink_status': str(dt4),
                    'Physical_downlink_status': str(dt5),
                    'Message': str('No VLAN600 data'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                    'No_of_attributes': 12
                }

                return jsonify(final_data)

            else:

                # vlan209_ccs
                if bool(stat_vlan209):
                    dt1 = str('Enabled')
                else:
                    dt1 = str('Disabled')

                # vlan400_vobb
                if bool(stat_vlan400):
                    dt2 = str('Enabled')
                else:
                    dt2 = str('Disabled')

                # vlan500_hsi
                if bool(stat_vlan500):
                    dt3 = str('Enabled')
                else:
                    dt3 = str('Disabled')

                # Physical uplink status
                if olt_tx_pr >= -28:
                    dt4 = str('Good')
                else:
                    dt4 = str('Bad')

                # Physical downlink status
                if olt_rx_pr >= -28:
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
                    'Upload_speed_profile': '',
                    'Download_speed_profile': '',
                    'Vlan_209': str(dt1),
                    'Vlan_400': str(dt2),
                    'Vlan_500': str(dt3),
                    'Physical_uplink_status': str(dt4),
                    'Physical_downlink_status': str(dt5),
                    'Message': str('OK'),
                    'tPreProc': calculate_response_time(),
                    'tSouthRespond': tSouthRespond,
                    'No_of_attributes': 12
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