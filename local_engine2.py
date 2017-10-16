
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

# @app.route('/getParam', methods=['GET'])
class BarAPI(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('serviceID', type=str)
        json = parser.parse_args()
        r = requests.get('http://localhost:5002/getParam', params=json)
        print('i got CONTENT='+r.content)
        return r.content

api.add_resource(BarAPI, '/getParam', endpoint='getParam')

if __name__ == '__main__':
    app.secret_key = 'mysecret2'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 5001, True)