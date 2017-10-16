
from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/rest/api/reading', methods=['POST'])
def reading():
    json = request.json
    loginid = json.get('loginid')
    reqParams = json.get('reqParams')#['reqParams']

    output = {
        'loginid': loginid,
        'retCode': 0,
        'retDesc': 'Success',
        'refid': 12345,
        'custAccessPort': {
            'accessPort': 'CBJ_G001-1/2/3.3',
            'src': 'radius'
        },
        'attributes':[
            {
                'name':'ADMIN_STATUS',
                'value':'Up'
            },
            {
                'name': 'OPER_STATUS',
                'value': 'Up'
            },
            {
                'name': 'ONT_TX_POWER',
                'value': '3.13'
            },
            {
                'name': 'ONT_RX_POWER',
                'value': '-12.1'
            },
            {
                'name': 'LASTUPTIME',
                'value': '1479181925843'
            },
        ]
    }
    return jsonify(output)

if __name__ == '__main__':
    app.secret_key = 'mysecret4'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 9001, True)