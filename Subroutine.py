

# Function for parsing data from second API
def get_new_attributes(serviceid, upstreamactualrate, downstreamactualrate, data):
    # url = "http://10.45.196.65/IDEAS/ideas.do?serviceID=" + serviceid
    # content = requests.get(url)
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

    # Necessary variable for upload speed profile and download speed profile
    upload_speed_profile = ''
    download_speed_profile = ''

    # Upload speed profile
    service_upload_speed = content.get('responseHeader').get('serviceCategory')[0]['serviceUploadSpeed']
    if len(service_upload_speed) > 2:
        service_upload_speed_to_number = float(service_upload_speed[0:2])
    else:
        service_upload_speed_to_number = float(service_upload_speed[0])

    temp_ratio = upstreamactualrate / service_upload_speed_to_number

    if temp_ratio >= 1:
        upload_speed_profile = 'Good'
    elif temp_ratio < 1:
        upload_speed_profile = 'Bad'

    # Download speed profile
    service_download_speed = content.get('responseHeader').get('serviceCategory')[0]['serviceDownloadSpeed']
    if len(service_download_speed) > 2:
        service_download_speed_to_number = float(service_download_speed[0:2])
    else:
        service_download_speed_to_number = float(service_download_speed[0])

    temp_ratio_download = downstreamactualrate / service_download_speed_to_number

    if temp_ratio_download >= 1:
        download_speed_profile = 'Good'
    elif temp_ratio_download < 1:
        download_speed_profile = 'Bad'

    parsed_data = {
        'device_host_name': str(device_hostname),
        'hsi_billing_status': str(hsi_billing_status),
        'radius_account_status': str(radius_acct_status),
        'hsi_session': str(hsi_session),
        'frequent_disconnect': float(frequent_disconnect),
        'neighbouring_session': float(neighbouring_session),
        'upload_speed_profile': str(upload_speed_profile),
        'download_speed_profile': str(download_speed_profile)
    }

    return parsed_data