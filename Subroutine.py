

# Function for parsing data from second API
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
    else:
        hsi_billing_status = 'Tos'

    # Radius Account Status
    radius_status = content.get('responseHeader').get('hsiService').get('radiusStatus')
    if radius_status.lower() == 'active':
        radius_acct_status = 'Active'
    else:
        radius_acct_status = 'Tos'

    radiusUpload = content.get('responseHeader').get('hsiService').get('radiusUpload')
    radiusUploadVal = radiusUpload.split('M')[0]
    radiusDownload = content.get('responseHeader').get('hsiService').get('radiusDownload')
    radiusDownloadVal = radiusDownload.split('M')[0]

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