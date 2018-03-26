
# KNN Machine learning Engine for IDEAS
# Author: Mohammad Kamar Uddin
# Version            Comments
# 1.2             Modified to predict with 13 attributes (mixed data)

import requests
from flask import Flask, jsonify, make_response, request
from flask_restful import Api, Resource, reqparse
from datetime import datetime
from knn_function import knn
import psycopg2
import psycopg2.extras
import logging
from logging.handlers import RotatingFileHandler
from requests import Timeout, HTTPError, ConnectionError

app = Flask(__name__)
api = Api(app)


# @app.route('/getParam', methods=['GET'])
class BarAPI(Resource):
    TABLE_NAME = 'ideas_testing_system_integration'

    def get(self):

        a1 = datetime.now()
        app.logger.debug("Process started at: %s", a1)
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        app.logger.debug("Parsed json: %s", json)

        try:
            r = requests.get('http://localhost:5002/getParam', params=json, timeout=120)
            r.raise_for_status()
        except Timeout:
            resp = self.calculate_response_time(a1)
            app.logger.debug("Process finished")
            app.logger.info("------------------------")
            return {"Message": "Timeout Error", "Response_time": resp, "Return_code": 408}
        except HTTPError:
            resp = self.calculate_response_time(a1)
            app.logger.debug("Process finished")
            app.logger.info("------------------------")
            return {"Message": "HTTPError Error", "Response_time": resp, "Return_code": 505}
        except ConnectionError:
            resp = self.calculate_response_time(a1)
            app.logger.info("Process finished")
            app.logger.info("------------------------")
            return {"Message": "ConnectionError Error", "Response_time": resp, "Return_code": 503}

        if r.json().get('Return_description') == 'Failed':
            content = r.json()
            resp = self.calculate_response_time(a1)
            app.logger.debug("Content from HTTP response: %s", content)
            app.logger.info("Process finished")
            app.logger.info("------------------------")
            return {"Return_code": 400,
                    "Message": content['Message'],
                    "Return_description": content['Return_description'],
                    "Response_time": resp}

        # Declaring necessary variables
        training_data_filename = 'training_data.csv'
        min_max_filename = 'min_max.csv'
        test_instance = []

        # Creating test instance from South API/PreProc response
        data = [r.json().get('HSI_billing_status'), r.json().get('Radius_account_status'), r.json().get('HSI_session'),
                r.json().get('Frequent_disconnect'), r.json().get('Neighbouring_session'), r.json().get('Vlan_209'),
                r.json().get('Vlan_500'), r.json().get('Vlan_400'), r.json().get('Vlan_600'),
                r.json().get('Upload_speed_profile'), r.json().get('Download_speed_profile'),
                r.json().get('Physical_uplink_status'), r.json().get('Physical_downlink_status')]

        app.logger.debug("Data parsed from South API response: %s", data)

        # Converting test data for KNN classifier
        for rec in range(len(data)):

            if data[rec] == 'Active':
                test_instance.append(float(1))
            elif data[rec] == 'Tos':
                test_instance.append(float(0))
            elif data[rec] == 'Online':
                test_instance.append(float(1))
            elif data[rec] == 'Offline':
                test_instance.append(float(2))
            elif data[rec] == 'Captive':
                test_instance.append(float(3))
            elif data[rec] == 'Enabled':
                test_instance.append(float(1))
            elif data[rec] == 'Disabled':
                test_instance.append(float(2))
            elif data[rec] == 'Good':
                test_instance.append(float(1))
            elif data[rec] == 'Bad':
                test_instance.append(float(2))
            else:
                test_instance.append(float(data[rec]))

        app.logger.debug("Final test instance: %s", test_instance)

        # Predicting using KNN Classifier
        classifier_knn_result = knn(test_instance, training_data_filename, min_max_filename)
        app.logger.debug("Result from KNN classifier: %s", classifier_knn_result)

        # Parsing predictive class from 'KNN' function and another necessary variable
        result = classifier_knn_result['result']  # Predicted class
        res_neighbours = classifier_knn_result['neighbours']

        app.logger.debug("Predicted class by KNN: %s", result)
        app.logger.debug("Neighbours: %s", res_neighbours)

        south_api_data = {'login': r.json().get('Login_id'),
                          'access_type': r.json().get('Access_type'),
                          'device_host_name': r.json().get('Device_host_name'),
                          'package_name': r.json().get('Package_name'),
                          'hsi_billing_status': data[0],
                          'radius_acct_status': data[1],
                          'hsi_session': data[2],
                          'frequent_disconnection': data[3],
                          'neighbouring_sessions': data[4],
                          'vlan_209': data[5],
                          'vlan_400': data[7],
                          'vlan_500': data[6],
                          'vlan_600': data[8],
                          'upload_speed_profile': data[9],
                          'download_speed_profile': data[10],
                          'physical_uplink_status': data[11],
                          'physical_downlink_status': data[12]
                          }

        app.logger.debug("South API data for database insertion function: %s", south_api_data)

        try:
            advisory_result = self.find_by_advisory_class(result, south_api_data)

            # Preparing ExpertMatrix and MatchedMatrix for sending data to west api
            exp_matrix = ''

            for i in range(len(test_instance)):
                if i == 3:
                    exp_matrix += '-'+str(test_instance[i])
                elif i == 4:
                    exp_matrix += '-'+str(test_instance[i])
                else:
                    exp_matrix += '-'+str(int(test_instance[i]))

            final_exp_matrix = exp_matrix[1:]

            match_matrix = ''

            for i in range(len(res_neighbours)):
                if i == 3:
                    match_matrix += '-'+str(res_neighbours[i])
                elif i == 4:
                    match_matrix += '-'+str(res_neighbours[i])
                else:
                    match_matrix += '-'+str(int(res_neighbours[i]))

            final_match_matrix = match_matrix[1:]

            t_engine_respond = self.calculate_response_time(a1)

            app.logger.debug("Database output: %s", advisory_result)
            app.logger.debug("Expert Matrix: %s", final_exp_matrix)
            app.logger.debug("Matched Matrix: %s", final_match_matrix)
            app.logger.info("Process finished")
            app.logger.info("------------------------")

            return {"PredictedClass": str(result),
                    "ExpertMatrix": str(final_exp_matrix),
                    "MatchMatrix": str(final_match_matrix),
                    "Summary": str(advisory_result['summary']),
                    "Prompt": str(advisory_result['symptom']),
                    "Action": str(advisory_result['next_action_update']),
                    "NextEscalation": str(advisory_result['next_escalation']),
                    "tEngineRespond": t_engine_respond,
                    "Return_code": 200,
                    "Return_description": 'Success'
                    }
        except Exception as err:
            resp = self.calculate_response_time(a1)
            app.logger.debug("Following database error occurred: %s", err)
            app.logger.info("------------------------")
            return {"Message": "An error occurred during database operation",
                    "Error": str(err), "Response_time": resp, "Return_code": 500}

    # Function to calculate time difference
    @classmethod
    def calculate_response_time(cls, start_time):
        b = datetime.now()
        delta = b - start_time
        time = int(delta.total_seconds() * 1000)
        return time  # milliseconds

    @classmethod
    def find_by_advisory_class(cls, advisory, data):
        conn = psycopg2.connect(host="10.44.28.80", database="ideas_ori", user="ideas_api", password="ideas")
        conn.set_session(autocommit=True)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        advisory_output_qry = "SELECT * FROM advisory_output WHERE advisory_class=%s"
        cur.execute(advisory_output_qry, (str(advisory),))
        advisory_result = cur.fetchone()

        if advisory_result:
            connectivity_summary = advisory_result['advisory_connectivity_summary'],
            symptom = advisory_result['advisory_symptom'],
            next_action_update = advisory_result['advisory_next_action_update'],
            next_escalation = advisory_result['advisory_next_escalation']

            update_query = """ INSERT INTO {table} (login, created_date, access_type, device_host_name, package_name,
                      hsi_billing_status, radius_acct_status, hsi_session, frequent_disconnection, 
                      neighbouring_sessions, vlan_209_ccs, vlan400_vobb, vlan500_hsi, vlan600_iptv, 
                      upload_speed_profile, download_speed_profile, physical_uplink_status, physical_downlink_status, 
                      advisory_connectivity_summary, advisory_symptom, advisory_next_action_update, 
                      advisory_next_escalation, advisory_class) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
                      %s,%s,%s,%s,%s,%s,%s)""".format(table=cls.TABLE_NAME)

            cur.execute(update_query, (str(data['login']), datetime.now(), str(data['access_type']),
                                       str(data['device_host_name']), str(data['package_name']),
                                       str(data['hsi_billing_status']), str(data['radius_acct_status']),
                                       str(data['hsi_session']), str(data['frequent_disconnection']),
                                       str(data['neighbouring_sessions']), str(data['vlan_209']), str(data['vlan_400']),
                                       str(data['vlan_500']), str(data['vlan_600']), str(data['upload_speed_profile']),
                                       str(data['download_speed_profile']), str(data['physical_uplink_status']),
                                       str(data['physical_downlink_status']), str(connectivity_summary), str(symptom),
                                       str(next_action_update), str(next_escalation), str(advisory)))

            conn.close()

            return {"summary": str(connectivity_summary),
                    "symptom": str(symptom),
                    "next_action_update": str(next_action_update),
                    "next_escalation": str(next_escalation),
                    "Message": "All database query executed successfully."
                    }


api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    logHandler = RotatingFileHandler('local_engine2.log', maxBytes=5000000, backupCount=1)
    logHandler.setLevel(logging.INFO)
    logHandler.setLevel(logging.DEBUG)
    app.logger.setLevel(logging.INFO)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(logHandler)
    app.secret_key = 'mysecret2'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 5001, True, threaded=True)
