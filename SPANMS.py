from time import sleep

from flask import Flask, request, jsonify
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

@app.route('/rest/api/reading', methods=['POST'])
def reading():
    print 'Engine start...'
    json = request.json
    loginid = json.get('loginId')
    reqParams = json.get('reqParams')#['reqParams']

    output = {
        'loginid': loginid,
        'retCode': 0,
        'retDesc': 'Failed',
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

    outputFTTH = {"retCode":0,"retDesc":"Success","refId":141494634,"custInfo":{"servicePoint":"HS1016599168","loginId":loginid,"accessPort":"SKT_G003-1/2/3.15","src":"radius"},"attributes":[{"name":"ADMIN_STATUS","value":"Up"},{"name":"BECDOWN","value":0},{"name":"BECUP","value":464},{"name":"BW_IN_UTIL","value":1.4759068936109543},{"name":"BW_OUT_UTIL","value":10.573651045560837},{"name":"CPU","value":None},{"name":"CRC_ERROR","value":0.0},{"name":"LASTDOWNCAUSE","value":"NotSupport"},{"name":"LASTDOWNTIME","value":"NotSupport"},{"name":"LASTUPTIME","value":"NotSupport"},{"name":"MAINSOFTVERSION","value":"NotSupport"},{"name":"MEM","value":24.8046875},{"name":"ONT_RX_POWER","value":-22.58},{"name":"ONT_TX_POWER","value":3.0
                },{"name":"ONTID","value":"15"},{"name":"ONTSTAT","value":"NotSupport"},{"name":"ONTVER","value":"NotSupport"},{"name":"ONT_BIAS","value":13.356},{"name":"ONT_TEMP","value":44.0},{"name":"ONT_VOLTS","value":3.3},{"name":"ONU_FIRMWARE","value":"3FE54799BOCI20"},{"name":"OPER_STATUS","value":"Up"},{"name":"PWD","value":"0003072764"},{"name":"RANGING","value":4700.0}
                ,{"name":"SERNUM","value":"ALCLF9067039"},{"name":"TEMP","value":None},{"name":"UL_BIAS","value":"NotSupport"},{"name":"UL_RX_POWER","value":"NotSupport"},{"name":"UL_TEMP","value":"NotSupport"},{"name":"UL_TX_POWER","value":"NotSupport"},{"name":"UL_VOLTS","value":"NotSupport"}],"lineProfiles":[{"siebelProfile":"UniFi Advance Plus 50Mbps (Thank You Campaign 2017)","lineProfileTx":"n/a","lineProfileRx":"n/a","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-3:IS-NR","vlan":"209","siebelProfileTx":None,"siebelProfileRx":None,"configuredProfileTx":"512K_UP","configuredProfileRx":"512K_DOWN","isSubscribed":False,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:VOIP-1-1-2-3-15-1:IS-NR","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_UP","configuredProfileRx":"256K_DOWN","isSubscribed":True,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-1:IS-NR","vlan":"500","siebelProfileTx":"21M","siebelProfileRx":"55M","configuredProfileTx":"21M_UP","configuredProfileRx":"55M_DOWN","isSubscribed":True,"isConfigured"
                :True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False},{"objId":"SKT_G003:FLOW-1-1-2-3-15-1-1-2:IS-NR","vlan":"600","siebelProfileTx":"10M","siebelProfileRx"
                :"10M","configuredProfileTx":"10M_UP_IPTV","configuredProfileRx":"10M_DOWN_IPTV","isSubscribed":True,"isConfigured":True,"isMissing":False,"isProfileTxMismatch":False,"isProfileRxMismatch":False}]}

    outputVDSL = '{"retDesc": "Success", "attributes": [{"name": "ADMIN_STATUS", "value": "Up"}, {"name": "CPU", "value": 6}, {"name": "CRC_ERROR", "value": "NotSupport"}, {"name": "DOWNSTREAM_ACTUAL_RATE", "value": 17000}, {"name": "DOWNSTREAM_ATTAINABLERATE", "value": 30667}, {"name": "DOWNSTREAM_ATTENUATION", "value": 26}, {"name": "DOWNSTREAM_MAX_CONFIG", "value": null}, {"name": "DOWNSTREAM_MIN_CONFIG", "value": null}, {"name": "DOWNSTREAM_POWER", "value": 11.7}, {"name": "DOWNSTREAM_SNR", "value": 11.6}, {"name": "LASTDOWNTIME", "value": "NotSupport"}, {"name": "LASTUPTIME", "value": 1502105096000}, {"name": "LINK_RETRAIN", "value": 44}, {"name": "MEM", "value": 74}, {"name": "OPER_STATUS", "value": "Up"}, {"name": "OPTION82", "value": null}, {"name": "PPOE", "value": null}, {"name": "TEMP", "value": "NotSupport"}, {"name": "UPSTREAM_ACTUAL_RATE", "value": 4999}, {"name": "UPSTREAM_ATTAINABLERATE", "value": 10606}, {"name": "UPSTREAM_ATTENUATION", "value": 27.8}, {"name": "UPSTREAM_MAX_CONFIG", "value": null}, {"name": "UPSTREAM_MIN_CONFIG", "value": null}, {"name": "UPSTREAM_POWER", "value": 13.6}, {"name": "UPSTREAM_SNR", "value": 8.9}, {"name": "UPTIME", "value": "217 days, 22 hours, 50 minutes"}], "custInfo": {"src": "radius", "servicePoint": "HS1001142952", "accessPort": "SDG_V1061-2/3/11", "loginId": "sida313@unifi"}, "retCode": 0, "refId": 164746955}'
    outputVDSLOriginalsida313 = '{"retCode":0,"retDesc":"Success","refId":166441329,"custInfo":{"servicePoint":"HS1001142952","loginId":"sida313@unifi","accessPort":"SDG_V1061-2/3/11","src":"radius"},"attributes":[{"name":"ADMIN_STATUS","value":"Up"},{"name":"CPU","value":6.0},{"name":"CRC_ERROR","value":"NotSupport"},{"name":"DOWNSTREAM_ACTUAL_RATE","value":17000.0},{"name":"DOWNSTREAM_ATTAINABLERATE","value":29919.0},{"name":"DOWNSTREAM_ATTENUATION","value":25.8},{"name":"DOWNSTREAM_MAX_CONFIG","value":17000.0},{"name":"DOWNSTREAM_MIN_CONFIG","value":128.0},{"name":"DOWNSTREAM_POWER","value":11.6},{"name":"DOWNSTREAM_SNR","value":11.3},{"name":"LASTDOWNTIME","value":"NotSupport"},{"name":"LASTUPTIME","value":1502105142000},{"name":"LINK_RETRAIN","value":48},{"name":"MEM","value":74.0},{"name":"OPER_STATUS","value":"Up"},{"name":"OPTION82","value":"enable"},{"name":"PPOE","value":"enable"},{"name":"TEMP","value":"NotSupport"},{"name":"UPSTREAM_ACTUAL_RATE","value":4999.0},{"name":"UPSTREAM_ATTAINABLERATE","value":9887.0},{"name":"UPSTREAM_ATTENUATION","value":27.7},{"name":"UPSTREAM_MIN_CONFIG","value":128.0},{"name":"UPSTREAM_POWER","value":13.6},{"name":"UPSTREAM_SNR","value":8.8},{"name":"UPTIME","value":"225 days, 23 hours, 58 minutes"}],"lineProfiles":[{"siebelProfile":"UniFi Lite 10Mbps (Thank You Campaign 2017)","lineProfileTx":"ASSIA_Z_17_05_2_2.PRF","lineProfileRx":"ASSIA_Z_17_05_2_2.PRF","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"SDG_V1061-2/3/11","vlan":"209","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"n/a","configuredProfileRx":"n/a","isSubscribed":false,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"SDG_V1061-2/3/11","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_VOBB","configuredProfileRx":"256K_VOBB","isSubscribed":True,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"SDG_V1061-2/3/11","vlan":"500","siebelProfileTx":"5M","siebelProfileRx":"10M","configuredProfileTx":"5M","configuredProfileRx":"10M","isSubscribed":True,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"SDG_V1061-2/3/11","vlan":"600","siebelProfileTx":"10M","siebelProfileRx":"10M","configuredProfileTx":"10M","configuredProfileRx":"10M","isSubscribed":True,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false}]}'
    outputVDSLOriginalsida313NonString = {
                                   "retCode":0,
                                   "retDesc":"Success",
                                   "refId":166441329,
                                   "custInfo":{
                                      "servicePoint":"HS1001142952",
                                      "loginId":"sida313@unifi",
                                      "accessPort":"SDG_V1061-2/3/11",
                                      "src":"radius"
                                   },
                                   "attributes":[
                                      {
                                         "name":"ADMIN_STATUS",
                                         "value":"Up"
                                      },
                                      {
                                         "name":"CPU",
                                         "value":6.0
                                      },
                                      {
                                         "name":"CRC_ERROR",
                                         "value":"NotSupport"
                                      },
                                      {
                                         "name":"DOWNSTREAM_ACTUAL_RATE",
                                         "value":17000.0
                                      },
                                      {
                                         "name":"DOWNSTREAM_ATTAINABLERATE",
                                         "value":29919.0
                                      },
                                      {
                                         "name":"DOWNSTREAM_ATTENUATION",
                                         "value":25.8
                                      },
                                      {
                                         "name":"DOWNSTREAM_MAX_CONFIG",
                                         "value":17000.0
                                      },
                                      {
                                         "name":"DOWNSTREAM_MIN_CONFIG",
                                         "value":128.0
                                      },
                                      {
                                         "name":"DOWNSTREAM_POWER",
                                         "value":11.6
                                      },
                                      {
                                         "name":"DOWNSTREAM_SNR",
                                         "value":11.3
                                      },
                                      {
                                         "name":"LASTDOWNTIME",
                                         "value":"NotSupport"
                                      },
                                      {
                                         "name":"LASTUPTIME",
                                         "value":1502105142000
                                      },
                                      {
                                         "name":"LINK_RETRAIN",
                                         "value":48
                                      },
                                      {
                                         "name":"MEM",
                                         "value":74.0
                                      },
                                      {
                                         "name":"OPER_STATUS",
                                         "value":"Up"
                                      },
                                      {
                                         "name":"OPTION82",
                                         "value":"enable"
                                      },
                                      {
                                         "name":"PPOE",
                                         "value":"enable"
                                      },
                                      {
                                         "name":"TEMP",
                                         "value":"NotSupport"
                                      },
                                      {
                                         "name":"UPSTREAM_ACTUAL_RATE",
                                         "value":4999.0
                                      },
                                      {
                                         "name":"UPSTREAM_ATTAINABLERATE",
                                         "value":9887.0
                                      },
                                      {
                                         "name":"UPSTREAM_ATTENUATION",
                                         "value":27.7
                                      },
                                      {
                                         "name":"UPSTREAM_MIN_CONFIG",
                                         "value":128.0
                                      },
                                      {
                                         "name":"UPSTREAM_POWER",
                                         "value":13.6
                                      },
                                      {
                                         "name":"UPSTREAM_SNR",
                                         "value":8.8
                                      },
                                      {
                                         "name":"UPTIME",
                                         "value":"225 days, 23 hours, 58 minutes"
                                      }
                                   ],
                                   "lineProfiles":[
                                      {
                                         "siebelProfile":"UniFi Lite 10Mbps (Thank You Campaign 2017)",
                                         "lineProfileTx":"ASSIA_Z_17_05_2_2.PRF",
                                         "lineProfileRx":"ASSIA_Z_17_05_2_2.PRF",
                                         "serviceProfileTx":"NotSupport",
                                         "serviceProfileRx":"NotSupport"
                                      }
                                   ],
                                   "trafficProfiles":[
                                      {
                                         "objId":"SDG_V1061-2/3/11",
                                         "vlan":"209",
                                         "siebelProfileTx":None,
                                         "siebelProfileRx":None,
                                         "configuredProfileTx":"n/a",
                                         "configuredProfileRx":"n/a",
                                         "isSubscribed":False,
                                         "isConfigured":True,
                                         "isMissing":False,
                                         "isProfileTxMismatch":False,
                                         "isProfileRxMismatch":False
                                      },
                                      {
                                         "objId":"SDG_V1061-2/3/11",
                                         "vlan":"400",
                                         "siebelProfileTx":"256K",
                                         "siebelProfileRx":"256K",
                                         "configuredProfileTx":"256K_VOBB",
                                         "configuredProfileRx":"256K_VOBB",
                                         "isSubscribed":True,
                                         "isConfigured":True,
                                         "isMissing":False,
                                         "isProfileTxMismatch":False,
                                         "isProfileRxMismatch":False
                                      },
                                      {
                                         "objId":"SDG_V1061-2/3/11",
                                         "vlan":"500",
                                         "siebelProfileTx":"5M",
                                         "siebelProfileRx":"10M",
                                         "configuredProfileTx":"5M",
                                         "configuredProfileRx":"10M",
                                         "isSubscribed":True,
                                         "isConfigured":True,
                                         "isMissing":False,
                                         "isProfileTxMismatch":False,
                                         "isProfileRxMismatch":False
                                      },
                                      {
                                         "objId":"SDG_V1061-2/3/11",
                                         "vlan":"600",
                                         "siebelProfileTx":"10M",
                                         "siebelProfileRx":"10M",
                                         "configuredProfileTx":"10M",
                                         "configuredProfileRx":"10M",
                                         "isSubscribed":True,
                                         "isConfigured":True,
                                         "isMissing":False,
                                         "isProfileTxMismatch":False,
                                         "isProfileRxMismatch":False
                                      }
                                   ]
                                }

    outputVDSLNonString = {
        "retCode": 0,
        "retDesc": "Success",
        "refId": 164746955,
        "custInfo": {
            "servicePoint": "HS1001142952",
            "loginId": "sida313@unifi",
            "accessPort": "SDG_V1061-2/3/11",
            "src": "radius"
        },
        "attributes": [
            {
                "name": "ADMIN_STATUS",
                "value": "Up"
            },
            {
                "name": "CPU",
                "value": 6
            },
            {
                "name": "CRC_ERROR",
                "value": "NotSupport"
            },
            {
                "name": "DOWNSTREAM_ACTUAL_RATE",
                "value": 17000
            },
            {
                "name": "DOWNSTREAM_ATTAINABLERATE",
                "value": 30667
            },
            {
                "name": "DOWNSTREAM_ATTENUATION",
                "value": 26
            },
            {
                "name": "DOWNSTREAM_MAX_CONFIG",
                "value": None
            },
            {
                "name": "DOWNSTREAM_MIN_CONFIG",
                "value": None
            },
            {
                "name": "DOWNSTREAM_POWER",
                "value": 11.7
            },
            {
                "name": "DOWNSTREAM_SNR",
                "value": 11.6
            },
            {
                "name": "LASTDOWNTIME",
                "value": "NotSupport"
            },
            {
                "name": "LASTUPTIME",
                "value": 1502105096000
            },
            {
                "name": "LINK_RETRAIN",
                "value": 44
            },
            {
                "name": "MEM",
                "value": 74
            },
            {
                "name": "OPER_STATUS",
                "value": "Up"
            },
            {
                "name": "OPTION82",
                "value": None
            },
            {
                "name": "PPOE",
                "value": None
            },
            {
                "name": "TEMP",
                "value": "NotSupport"
            },
            {
                "name": "UPSTREAM_ACTUAL_RATE",
                "value": 4999
            },
            {
                "name": "UPSTREAM_ATTAINABLERATE",
                "value": 10606
            },
            {
                "name": "UPSTREAM_ATTENUATION",
                "value": 27.8
            },
            {
                "name": "UPSTREAM_MAX_CONFIG",
                "value": None
            },
            {
                "name": "UPSTREAM_MIN_CONFIG",
                "value": None
            },
            {
                "name": "UPSTREAM_POWER",
                "value": 13.6
            },
            {
                "name": "UPSTREAM_SNR",
                "value": 8.9
            },
            {
                "name": "UPTIME",
                "value": "217 days, 22 hours, 50 minutes"
            }
        ]
    }
    #zizigreen84
    outputFTTHNoTrafficProfile = {
           "retCode":0,
           "retDesc":"Success",
           "refId":167734886,
           "custInfo":{
              "servicePoint":"HS1002818571",
              "loginId":"zizigreen84@unifi",
              "accessPort":"TDI_G007-1/5/3.24",
              "src":"radius"
           },
           "attributes":[
              {
                 "name":"ONT_RX_POWER",
                 "value":-20.75
              },
              {
                 "name":"ONT_TX_POWER",
                 "value":2.68
              }
           ],
           "lineProfiles":[
              {
                 "siebelProfile":"VIP 10",
                 "lineProfileTx":"n/a",
                 "lineProfileRx":"n/a",
                 "serviceProfileTx":"NotSupport",
                 "serviceProfileRx":"NotSupport"
              }
           ],
           "trafficProfiles":[

           ]
        }

    outAswadiUnifi = '{"retCode":0,"retDesc":"Success","refId":168146011,"custInfo":{"servicePoint":"HS1030462045","loginId":"aswadiunifi@unifi","accessPort":"JLT_G005-1/8/1.16","src":"radius"},"attributes":[{"name":"ONT_RX_POWER","value":-18.116},{"name":"ONT_TX_POWER","value":3.0}],"lineProfiles":[{"siebelProfile":"UniFi Advance 30Mbps - Bonanza Campaign","lineProfileTx":"n/a","lineProfileRx":"n/a","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"JLT_G005:VOIP-1-1-8-1-16-1:IS-NR","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_UP","configuredProfileRx":"256K_DOWN","isSubscribed":True,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":null,"vlan":"500","siebelProfileTx":"11M","siebelProfileRx":"35M","configuredProfileTx":null,"configuredProfileRx":null,"isSubscribed":True,"isConfigured":false,"isMissing":True,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":null,"vlan":"600","siebelProfileTx":"10M","siebelProfileRx":"10M","configuredProfileTx":null,"configuredProfileRx":null,"isSubscribed":True,"isConfigured":false,"isMissing":True,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"JLT_G005:FLOW-1-1-8-1-16-1-2-1:OOS-AU","vlan":"621","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"10M_UP","configuredProfileRx":"10M_DOWN","isSubscribed":false,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"JLT_G005:FLOW-1-1-8-1-16-1-2-5:OOS-AU","vlan":"821","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"128K_UP","configuredProfileRx":"128K_DOWN","isSubscribed":false,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"JLT_G005:FLOW-1-1-8-1-16-1-2-3:OOS-AU","vlan":"823","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"50M_UP_IPTV","configuredProfileRx":"50M_DOWN_IPTV","isSubscribed":false,"isConfigured":True,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false}]}'

    afaideen80 = '{"retCode":0,"retDesc":"Success","refId":168322100,"custInfo":{"servicePoint":"HS1025171053","loginId":"afaideen80@unifi","accessPort":"SDG_G026-1/7/4.7","src":"radius"},"attributes":[{"name":"ONT_RX_POWER","value":-18.082},{"name":"ONT_TX_POWER","value":3.0}],"lineProfiles":[{"siebelProfile":"UniFi Advance Plus 50Mbps (Thank You Campaign 2017)","lineProfileTx":"n/a","lineProfileRx":"n/a","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"1/1/7/4/7/1/1","vlan":"209","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"512K_UP","configuredProfileRx":"512K_DOWN","isSubscribed":false,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"SDG_G026:VOIP-1-1-7-4-7-1:IS-NR","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_UP","configuredProfileRx":"256K_DOWN","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"1/1/7/4/7/1/1","vlan":"500","siebelProfileTx":"21M","siebelProfileRx":"55M","configuredProfileTx":"21M_UP","configuredProfileRx":"55M_DOWN","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"1/1/7/4/7/1/1","vlan":"600","siebelProfileTx":"10M","siebelProfileRx":"10M","configuredProfileTx":"10M_UP_IPTV","configuredProfileRx":"10M_DOWN_IPTV","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false}]}'
    afaideen80Offline = '{"retCode":0,"retDesc":"Success","refId":168322100,"custInfo":{"servicePoint":"HS1025171053","loginId":"afaideen80@unifi","accessPort":"SDG_G026-1/7/4.7","src":"radius"},"attributes":[{"name":"ONT_RX_POWER","value":null},{"name":"ONT_TX_POWER","value":null}],"lineProfiles":[{"siebelProfile":"UniFi Advance Plus 50Mbps (Thank You Campaign 2017)","lineProfileTx":"n/a","lineProfileRx":"n/a","serviceProfileTx":"NotSupport","serviceProfileRx":"NotSupport"}],"trafficProfiles":[{"objId":"1/1/7/4/7/1/1","vlan":"209","siebelProfileTx":null,"siebelProfileRx":null,"configuredProfileTx":"512K_UP","configuredProfileRx":"512K_DOWN","isSubscribed":false,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"SDG_G026:VOIP-1-1-7-4-7-1:IS-NR","vlan":"400","siebelProfileTx":"256K","siebelProfileRx":"256K","configuredProfileTx":"256K_UP","configuredProfileRx":"256K_DOWN","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"1/1/7/4/7/1/1","vlan":"500","siebelProfileTx":"21M","siebelProfileRx":"55M","configuredProfileTx":"21M_UP","configuredProfileRx":"55M_DOWN","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false},{"objId":"1/1/7/4/7/1/1","vlan":"600","siebelProfileTx":"10M","siebelProfileRx":"10M","configuredProfileTx":"10M_UP_IPTV","configuredProfileRx":"10M_DOWN_IPTV","isSubscribed":true,"isConfigured":true,"isMissing":false,"isProfileTxMismatch":false,"isProfileRxMismatch":false}]}'
    kwong4564 ={
                  "attributes": [
                    {
                      "name": "DOWNSTREAM_ACTUAL_RATE",
                      "value": None
                    },
                    {
                      "name": "DOWNSTREAM_ATTENUATION",
                      "value": None
                    },
                    {
                      "name": "DOWNSTREAM_SNR",
                      "value": None
                    },
                    {
                      "name": "UPSTREAM_ACTUAL_RATE",
                      "value": None
                    },
                    {
                      "name": "UPSTREAM_ATTENUATION",
                      "value": None
                    },
                    {
                      "name": "UPSTREAM_SNR",
                      "value": None
                    },
                    {
                      "tSouthRespond": 3205
                    }
                  ],
                  "custInfo": {
                    "accessPort": "BAT_V1076-0/1/44",
                    "loginId": "kwong4564@unifi",
                    "servicePoint": "HS1027654220",
                    "src": "radius"
                  },
                  "lineProfiles": [
                    {
                      "lineProfileRx": "ASSIA_MA_44_10_1_2",
                      "lineProfileTx": "ASSIA_MA_44_10_1_2",
                      "serviceProfileRx": "NotSupport",
                      "serviceProfileTx": "NotSupport",
                      "siebelProfile": "UniFi Advance 30Mbps + Ruby (MU 2017 Campaign)"
                    }
                  ],
                  "refId": 172499017,
                  "retCode": 0,
                  "retDesc": "Success",
                  "trafficProfiles": [
                    {
                      "configuredProfileRx": None,
                      "configuredProfileTx": None,
                      "isConfigured": False,
                      "isMissing": True,
                      "isProfileRxMismatch": False,
                      "isProfileTxMismatch": False,
                      "isSubscribed": True,
                      "objId": None,
                      "siebelProfileRx": "256K",
                      "siebelProfileTx": "256K",
                      "vlan": "400"
                    },
                    {
                      "configuredProfileRx": None,
                      "configuredProfileTx": None,
                      "isConfigured": False,
                      "isMissing": True,
                      "isProfileRxMismatch": False,
                      "isProfileTxMismatch": False,
                      "isSubscribed": True,
                      "objId": None,
                      "siebelProfileRx": "35M",
                      "siebelProfileTx": "11M",
                      "vlan": "500"
                    },
                    {
                      "configuredProfileRx": None,
                      "configuredProfileTx": None,
                      "isConfigured": False,
                      "isMissing": True,
                      "isProfileRxMismatch": False,
                      "isProfileTxMismatch": False,
                      "isSubscribed": True,
                      "objId": None,
                      "siebelProfileRx": "10M",
                      "siebelProfileTx": "10M",
                      "vlan": "600"
                    }
                  ]
                }
    venicefun1117 = {
                        "attributes": [
                            {
                              "name": "DOWNSTREAM_ACTUAL_RATE",
                              "value": 43998.0
                            },
                            {
                              "name": "DOWNSTREAM_ATTENUATION",
                              "value": 11.6
                            },
                            {
                              "name": "DOWNSTREAM_SNR",
                              "value": 22.1
                            },
                            {
                              "name": "UPSTREAM_ACTUAL_RATE",
                              "value": 10000.0
                            },
                            {
                              "name": "UPSTREAM_ATTENUATION",
                              "value": 6.1
                            },
                            {
                              "name": "UPSTREAM_SNR",
                              "value": 23.1
                            },
                            {
                              "tSouthRespond": 7603
                            }
                          ],
                          "custInfo": {
                            "accessPort": "MDH_V1022-2/8/6",
                            "loginId": "venicefun1117@unifi",
                            "servicePoint": "HS1003637118",
                            "src": "radius"
                          },
                          "lineProfiles": [
                            {
                              "lineProfileRx": "ASSIA_Z_44_10_2_2.PRF",
                              "lineProfileTx": "ASSIA_Z_44_10_2_2.PRF",
                              "serviceProfileRx": "NotSupport",
                              "serviceProfileTx": "NotSupport",
                              "siebelProfile": "UniFi 30 Mbps"
                            }
                          ],
                          "refId": 172532423,
                          "retCode": 0,
                          "retDesc": "Success",
                          "trafficProfiles": [
                            {
                              "configuredProfileRx": "n/a",
                              "configuredProfileTx": "n/a",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": False,
                              "objId": "MDH_V1022-2/8/6",
                              "siebelProfileRx": None,
                              "siebelProfileTx": None,
                              "vlan": "1"
                            },
                            {
                              "configuredProfileRx": "n/a",
                              "configuredProfileTx": "n/a",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": False,
                              "objId": "MDH_V1022-2/8/6",
                              "siebelProfileRx": None,
                              "siebelProfileTx": None,
                              "vlan": "209"
                            },
                            {
                              "configuredProfileRx": "n/a",
                              "configuredProfileTx": "n/a",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": True,
                              "isProfileTxMismatch": True,
                              "isSubscribed": True,
                              "objId": "MDH_V1022-2/8/6",
                              "siebelProfileRx": "256K",
                              "siebelProfileTx": "256K",
                              "vlan": "400"
                            },
                            {
                              "configuredProfileRx": "n/a",
                              "configuredProfileTx": "n/a",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": True,
                              "isProfileTxMismatch": True,
                              "isSubscribed": True,
                              "objId": "MDH_V1022-2/8/6",
                              "siebelProfileRx": "35M",
                              "siebelProfileTx": "11M",
                              "vlan": "500"
                            },
                            {
                              "configuredProfileRx": "10M",
                              "configuredProfileTx": "10M",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True,
                              "objId": "MDH_V1022-2/8/6",
                              "siebelProfileRx": "10M",
                              "siebelProfileTx": "10M",
                              "vlan": "600"
                            }
                          ]
                    }
    inbatchaOffline = {   
                          "attributes": [
                            {
                              "name": "DOWNSTREAM_ACTUAL_RATE", 
                              "value": None
                            }, 
                            {
                              "name": "DOWNSTREAM_ATTENUATION", 
                              "value": None
                            }, 
                            {
                              "name": "DOWNSTREAM_SNR", 
                              "value": None
                            }, 
                            {
                              "name": "UPSTREAM_ACTUAL_RATE", 
                              "value": None
                            }, 
                            {
                              "name": "UPSTREAM_ATTENUATION", 
                              "value": None
                            }, 
                            {
                              "name": "UPSTREAM_SNR", 
                              "value": None
                            }, 
                            {
                              "tSouthRespond": 3085
                            }
                          ], 
                          "custInfo": {
                            "accessPort": "MTI_V1041-0/7/44", 
                            "loginId": "inbatcha@unifi", 
                            "servicePoint": "HS1016002236", 
                            "src": "radius"
                          }, 
                          "lineProfiles": [
                            {
                              "lineProfileRx": "ASSIA_MA_22_05_2_2", 
                              "lineProfileTx": "ASSIA_MA_22_05_2_2", 
                              "serviceProfileRx": "NotSupport", 
                              "serviceProfileTx": "NotSupport", 
                              "siebelProfile": "UniFi Lite 10Mbps (Thank You Campaign 2017)"
                            }
                          ], 
                          "refId": 172730236, 
                          "retCode": 0, 
                          "retDesc": "Success", 
                          "trafficProfiles": [
                            {
                              "configuredProfileRx": "ip-traffic-table_2", 
                              "configuredProfileTx": "ip-traffic-table_2", 
                              "isConfigured": True, 
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": False,
                              "objId": "MTI_V1041:MTI_V1041-0/7/44:,,", 
                              "siebelProfileRx": None, 
                              "siebelProfileTx": None, 
                              "vlan": "209"
                            }, 
                            {
                              "configuredProfileRx": "256K_DOWN_VOBB", 
                              "configuredProfileTx": "256K_UP_VOBB", 
                              "isConfigured": True, 
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True, 
                              "objId": "MTI_V1041:MTI_V1041-0/7/44:,,", 
                              "siebelProfileRx": "256K", 
                              "siebelProfileTx": "256K", 
                              "vlan": "400"
                            }, 
                            {
                              "configuredProfileRx": "10M_DOWN", 
                              "configuredProfileTx": "5M_UP", 
                              "isConfigured": True, 
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True, 
                              "objId": "MTI_V1041:MTI_V1041-0/7/44:,,", 
                              "siebelProfileRx": "10M", 
                              "siebelProfileTx": "5M", 
                              "vlan": "500"
                            }, 
                            {
                              "configuredProfileRx": "10M_DOWN_IPTV", 
                              "configuredProfileTx": "10M_UP_IPTV", 
                              "isConfigured": True, 
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True, 
                              "objId": "MTI_V1041:MTI_V1041-0/7/44:,,", 
                              "siebelProfileRx": "10M", 
                              "siebelProfileTx": "10M", 
                              "vlan": "600"
                            }
                          ]
                        }
    arifendiOffline = {
                          "attributes": [
                            {
                              "name": "ONT_RX_POWER",
                              "value": None
                            },
                            {
                              "name": "ONT_TX_POWER",
                              "value": None
                            },
                            {
                              "tSouthRespond": 9662
                            }
                          ],
                          "custInfo": {
                            "accessPort": "BGI_G008-0/3/4.17",
                            "loginId": "arifendi@unifi",
                            "servicePoint": "HS1002973248",
                            "src": "radius"
                          },
                          "lineProfiles": [
                            {
                              "lineProfileRx": "tm_huawei_lineprofile",
                              "lineProfileTx": "tm_huawei_lineprofile",
                              "serviceProfileRx": "tm_huawei_serviceprofile",
                              "serviceProfileTx": "tm_huawei_serviceprofile",
                              "siebelProfile": "UniFi Lite 10Mbps (Thank You Campaign 2017)"
                            }
                          ],
                          "refId": 173532407,
                          "retCode": 0,
                          "retDesc": "Success",
                          "trafficProfiles": [
                            {
                              "configuredProfileRx": "512K_DOWNP04",
                              "configuredProfileTx": "512K_UPP04",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": False,
                              "objId": "BGI_G008:BGI_G008-0/3/4.17:4,,",
                              "siebelProfileRx": None,
                              "siebelProfileTx": None,
                              "vlan": "209"
                            },
                            {
                              "configuredProfileRx": "256K_DOWN_VOBB",
                              "configuredProfileTx": "256K_UP_VOBB",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True,
                              "objId": "BGI_G008:BGI_G008-0/3/4.17:2,,",
                              "siebelProfileRx": "256K",
                              "siebelProfileTx": "256K",
                              "vlan": "400"
                            },
                            {
                              "configuredProfileRx": "35M_DOWN",
                              "configuredProfileTx": "11M_UP",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True,
                              "objId": "BGI_G008:BGI_G008-0/3/4.17:1,,",
                              "siebelProfileRx": "35M",
                              "siebelProfileTx": "11M",
                              "vlan": "500"
                            },
                            {
                              "configuredProfileRx": "10M_DOWN_IPTV",
                              "configuredProfileTx": "10M_UP_IPTV",
                              "isConfigured": True,
                              "isMissing": False,
                              "isProfileRxMismatch": False,
                              "isProfileTxMismatch": False,
                              "isSubscribed": True,
                              "objId": "BGI_G008:BGI_G008-0/3/4.17:3,,",
                              "siebelProfileRx": "10M",
                              "siebelProfileTx": "10M",
                              "vlan": "600"
                            }
                          ]
                        }
    error = {"retCode":200,"retDesc":"Error Can't query to EMS/NE","custInfo":{"servicePoint":"HS1025171053","loginId":loginid,"accessPort":"SDG_G026-1/7/4.7","src":"radius"},"attributes":[]}
    # sleep(15)#in seconds
    print 'Engine finish...'
    # return jsonify(output)
    # return outputVDSLOriginalsida313       #don't use jsonify() if input arguments already type string
    # return jsonify(outputVDSLOriginalsida313NonString)
    # return outAswadiUnifi
    return afaideen80
    # return afaideen80Offline
    # return jsonify(arifendiOffline)
    # return jsonify(inbatchaOffline)
    # return jsonify(venicefun1117)
    # return jsonify(kwong4564)
    # return jsonify(outputVDSLOriginalNonString)
    # return jsonify(outputFTTHNoTrafficProfile)
    # return jsonify(outputFTTH)
    # return jsonify(outputVDSLNonString)

    # return jsonify(error)


if __name__ == '__main__':
    app.secret_key = 'mysecret4'
    # app.run('127.0.0.1', 5001, True)
    app.run('0.0.0.0', 9001, True, threaded=True)
