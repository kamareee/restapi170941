

# Function for parsing data from second API
import re


def get_new_attributes(serviceid, data):
    content = data;

    # Device host name
    port_info = content.get('responseHeader').get('sessionStatus').get('portInfo')
    new_port_info = port_info.split('-')
    device_hostname = str(new_port_info[0])

    # HSI billing status
    service_status = content.get('responseHeader').get('serviceCategory')[0]['serviceStatus']
    if service_status.lower() == 'active':
        hsi_billing_status = 'Active'
    elif service_status.lower() == 'tos':
        hsi_billing_status = 'Tos'
    else:
        hsi_billing_status = ''

    # Radius Account Status
    radius_status = content.get('responseHeader').get('hsiService').get('radiusStatus')
    if radius_status.lower() == 'active':
        radius_acct_status = 'Active'
    elif radius_status.lower() == 'tos':
        radius_acct_status = 'Tos'
    else:
        radius_acct_status = ''

    radiusUpload = content.get('responseHeader').get('hsiService').get('radiusUpload')
    if str(radiusUpload).__contains__('M'):
        unit = 1000000.0;
    elif str(radiusUpload).__contains__('K'):
        unit = 1000.0;
    radiusUploadVal = float(re.split('M|K',radiusUpload)[0]) * unit;#radiusUpload.split('M')[0]
    radiusDownload = content.get('responseHeader').get('hsiService').get('radiusDownload')
    if str(radiusDownload).__contains__('M'):
        unit = 1000000.0;
    elif str(radiusDownload).__contains__('K'):
        unit = 1000.0;
    radiusDownloadVal = float(re.split('M|K',radiusDownload)[0]) * unit;#radiusDownload.split('M')[0]

    # HSI session
    session_status = content.get('responseHeader').get('sessionStatus').get('state')
    if session_status.lower() == 'online':
        hsi_session = 'Online'
    elif session_status.lower() == 'offline':
        hsi_session = 'Offline'
    else:
        hsi_session = 'Captive'

    # Frequent disconnection
    frequent_disconnect = content.get('responseHeader').get('frequentDisconnect').get('dayCount')

    # Neighbouring session
    dp_sessions = content.get('responseHeader').get('neighbouringSessions').get('dpSessions')
    dp_ss = dp_sessions.split('/')
    dp_numerator = float(dp_ss[0])
    dp_denominator = float(dp_ss[1])
    neighbouring_session = round((float(dp_numerator * 100) / float(dp_denominator)), 2)

    parsed_data = {
        'device_host_name': str(device_hostname),
        'hsi_billing_status': str(hsi_billing_status),
        'radius_account_status': str(radius_acct_status),
        'hsi_session': str(hsi_session),
        'frequent_disconnect': float(frequent_disconnect),
        'neighbouring_session': float(neighbouring_session),
        'radiusUpload':float(radiusUploadVal),
        'radiusDownload':float(radiusDownloadVal)
    }

    return parsed_data