
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

    output2 = {"retCode":0,"retDesc":"Success","refId":141494634,"custInfo":{"servicePoint":"HS1016599168","loginId":loginid,"accessPort":"SKT_G003-1/2/3.15","src":"radius"},"attributes":[{"name":"ADMIN_STATUS","value":"Up"},{"name":"BECDOWN","value":0},{"name":"BECUP","value":464},{"name":"BW_IN_UTIL","value":1.4759068936109543},{"name":"BW_OUT_UTIL","value":10.573651045560837},{"name":"CPU","value":None},{"name":"CRC_ERROR","value":0.0},{"name":"LASTDOWNCAUSE","value":"NotSupport"},{"name":"LASTDOWNTIME","value":"NotSupport"},{"name":"LASTUPTIME","value":"NotSupport"},{"name":"MAINSOFTVERSION","value":"NotSupport"},{"name":"MEM","value":24.8046875},{"name":"OLT_RX_POWER","value":-22.58},{"name":"OLT_TX_POWER","value":3.0
},{"name":"ONTID","value":"15"},{"name":"ONTSTAT","value":"NotSupport"},{"name":"ONTVER","value":"NotSupport"},{"name":"ONT_BIAS","value":13.356},{"name":"ONT_TEMP","value":44.0},{"name":"ONT_VOLTS","value":3.3},{"name":"ONU_FIRMWARE","value":"3FE54799BOCI20"},{"name":"OPER_STATUS","value":"Up"},{"name":"PWD","value":"0003072764"},{"name":"RANGING","value":4700.0}
,{"name":"SERNUM","value":"ALCLF9067039"},{"name":"TEMP","value":None},{"name":"UL_BIAS","value":"NotSupport"},{"name":"UL_RX_POWER","value":"NotSupport"},{"name":"UL_TEMP","value":"NotSupport"},{"name":"UL_TX_POWER","value":"NotSupport"},{"name":"UL_VOLTS","value":"NotSupport"}],"lineProfiles":[{"siebelProfile":"UniFi Advance Plus 50Mbps (Thank You Campaign 2017)","lineProfileTx":"n/a","lineProfileRx":"n/a","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-3:IS-NR","vlan":"209","siebelProfileTx":None,"siebelProfileRx":None,"configuredProfileTx":"512K_UP","configuredProfileRx":"512K_DOWN","isSubscribed":False,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:VOIP-1-1-2-3-15-1:IS-NR","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_UP","configuredProfileRx":"256K_DOWN","isSubscribed":True,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-1:IS-NR","vlan":"500","siebelProfileTx":"21M","siebelProfileRx":"55M","configuredProfileTx":"21M_UP","configuredProfileRx":"55M_DOWN","isSubscribed":True,"isConfigured"
:True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-2:IS-NR","vlan":"600","siebelProfileTx":"10M","siebelProfileRx"
:"10M","configuredProfileTx":"10M_UP_IPTV","configuredProfileRx":"10M_DOWN_IPTV","isSubscribed":True,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False}]}
    return jsonify(output)

if __name__ == '__main__':
    app.secret_key = 'mysecret4'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 9001, True)