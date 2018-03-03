import requests
import datetime

from concurrent.futures import TimeoutError
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from requests import ConnectionError, Timeout, HTTPError
from requests_futures.sessions import FuturesSession

app = Flask(__name__)
api = Api(app)

# @app.route('/getParam', methods=['GET'])
class BarAPI(Resource):
    def get(self):
        a = datetime.datetime.now()
        print a
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        serviceID = json.get('serviceID')
        # payload = {'loginId': serviceID, "reqParams": ["ADMIN_STATUS","OPER_STATUS",'ONT_TX_POWER','ONT_RX_POWER','LASTUPTIME']}
        payload = {"loginId":serviceID,"trafficProfile":"true","lineProfile":"true",
                   "reqParams":["ADMIN_STATUS","OPER_STATUS","OLT_RX_POWER","OLT_TX_POWER","ONT_TEMP","ONT_VOLTS",
                    "ONT_BIAS","RANGING","CPU","MEM","TEMP","BECUP","BECDOWN","UL_RX_POWER","UL_TX_POWER","UL_BIAS",
                    "UL_TEMP","UL_VOLTS","CRC_ERROR","BW_IN_UTIL","BW_OUT_UTIL","SERNUM","PWD","ONTID","ONU_FIRMWARE",
                    "LASTUPTIME","LASTDOWNTIME","LASTDOWNCAUSE","ONTSTAT","ONTVER","MAINSOFTVERSION","UPSTREAM_SNR","DOWNSTREAM_SNR",
                    "UPSTREAM_POWER","DOWNSTREAM_POWER","UPSTREAM_ATTENUATION","DOWNSTREAM_ATTENUATION","UPSTREAM_ATTAINABLERATE",
                    "DOWNSTREAM_ATTAINABLERATE","UPSTREAM_ACTUAL_RATE","DOWNSTREAM_ACTUAL_RATE","UPSTREAM_MIN_CONFIG","DOWNSTREAM_MAX_CONFIG",
                    "DOWNSTREAM_MIN_CONFIG","DOWNSTREAM_MAX_CONFIG","PPOE","OPTION82","UPTIME","LINK_RETRAIN"]}
        print(payload)
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        # r = requests.post('http://localhost:9001/rest/api/reading', json=payload, headers=headers)
        # r = requests.post('http://10.41.56.90:9001/rest/api/reading', json = payload, headers = headers)
        session = FuturesSession()
        api_one = session.post('http://localhost:9001/rest/api/reading', json=payload, headers=headers, timeout=120)
        api_two = session.get('http://10.45.196.65/IDEAS/ideas.do?serviceID=' + serviceID)
        try:
            r = api_one.result()
            r2 = api_two.result()
        except ConnectionError as e:
            print(e.message)
            return str(e.message)
        except Timeout as e:
            print(e.message)
            return str(e.message)
        except HTTPError as e:
            print(e.message)
            return str(e.message)

        b = datetime.datetime.now()
        delta = b - a
        print delta
        tSouthRespond = int(delta.total_seconds() * 1000)  # miliseconds
        try:
            data = r.json()#r.content
            data2 = r2.json()
            data['attributes'].append({'tSouthRespond': tSouthRespond})
            data['@api2'] = data2
            print(data)
        except ValueError:
            data = r.content
        return data

api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret3'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 5002, True, threaded=True)