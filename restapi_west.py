
import requests
import datetime
import json
from flask import Flask, render_template, make_response
from flask_restful import Api, Resource, reqparse
from requests import Timeout, ConnectionError, HTTPError

app = Flask(__name__)
api = Api(app)

class BarAPI(Resource):
    def get(self):
        print 'start'
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        serviceID = json.get('serviceID')#__getitem__('serviceID')
        # payload = {'serviceID': serviceID}
        a = datetime.datetime.now()
        print a
        r = requests.get('http://localhost:5001/getParam', params=json)
        # try:
        #     r = requests.get('http://localhost:5001/getParam',params=json,timeout=140)
        #     r.raise_for_status()
        # except Timeout:
        #     print ("WBI:Timeout Error:")
        #     return "WBI:Timeout Error:"
        # except HTTPError:
        #     print ("WBI:HTTPError Error:")
        #     return "WBI:HTTPError Error:"
        # except ConnectionError:
        #     print ("WBI:ConnectionError Error:")
        #     return "WBI:ConnectionError Error:"

        headers = {'Content-Type': 'text/xml'}
        Return_description = r.json().get('Return_description')

        if str(Return_description).__eq__('Failed'):
            # return r.content
            print r.content
            msg = r.json().get('Message')
            code = r.json().get('Return_code')
            tSouth_Respond = r.json().get('tSouthRespond')
            if code == 40000:
                return make_response(render_template('error40000.xml'), 200, headers)
            elif code == 40001:
                return make_response(render_template('error40001.xml'), 200, headers)
            elif code == 40002:
                return make_response(render_template('error40002.xml'), 200, headers)
            elif code == 40003:
                return make_response(render_template('error40003.xml'), 200, headers)
            elif code == 40004:
                return make_response(render_template('error40004.xml'), 200, headers)
            elif code == 40005:
                return make_response(render_template('error40005.xml'), 200, headers)
            elif code == 40006:
                return make_response(render_template('error40006.xml'), 200, headers)
            elif code == 40007:
                return make_response(render_template('error40007.xml'), 200, headers)
            elif code == 40008:
                return make_response(render_template('error40008.xml'), 200, headers)
            elif code == 40009:
                return make_response(render_template('error40009b.xml'), 200, headers)
            else:
                return make_response(render_template('error.xml', msg = msg, error_msg = r.content), 200, headers)


        try:
            predictedClass = r.json().get('PredictedClass')
            advisory_action = r.json().get('Action')
            advisory_summary = r.json().get('Summary')
            advisory_prompt = r.json().get('Prompt')
            advisory_inbound = r.json().get('Inbound')
            advisory_escalation = r.json().get('NextEscalation')
            expertmatrix = r.json().get('ExpertMatrix')
            matchedmatrix = r.json().get('MatchMatrix')
            t2Respond = r.json().get('tEngineRespond')
            tSouth_Respond = r.json().get('tSouthRespond')
            tEngine_South_Respond = r.json().get('tEngineSouthRespond')
        except:
            data = r.content
            return data
        headers = {'Content-Type': 'text/xml'}
        b = datetime.datetime.now()
        delta = b - a
        print delta
        print 'finish'
        t1Respond = int(delta.total_seconds() * 1000) #miliseconds
        # return parser.parse_args()
        return make_response(render_template('testxml.xml', summary=advisory_summary, predictedclass=predictedClass,
                                             action=advisory_action, tRespond=t1Respond, tEngineRespond=t2Respond,
                                             prompt=advisory_prompt, inbound=advisory_inbound,
                                             nextescalation=advisory_escalation,
                                             expertmtx=expertmatrix, matchmtx=matchedmatrix), 200, headers)
        # return make_response(render_template('testxml.xml', summary=advisory_summary, predictedclass=predictedClass,
        #                                      action=advisory_action, tRespond=t1Respond,tEngineSouthRespond=tEngine_South_Respond,tEngineRespond=t2Respond,tSouthRespond=tSouth_Respond,
        #                                      prompt=advisory_prompt, inbound=advisory_inbound,
        #                                      nextescalation=advisory_escalation,
        #                                      expertmtx=expertmatrix, matchmtx=matchedmatrix), 200, headers)


api.add_resource(BarAPI, '/expert.do', endpoint='expert.do')
api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    # app.run('127.0.0.1', 5000, True)
    # app.run(debug=True)
    app.run('0.0.0.0', 5000, False, threaded=True)
