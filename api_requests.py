import configparser
import requests
from datetime import datetime, timezone, timedelta


config = configparser.ConfigParser()
config.read('ttlock_admin_panel\\config.ini')
client_secret = config['ttlock_admin_panel']['client_secret']
client_id = config['ttlock_admin_panel']['client_id']
redirect_uri = config['ttlock_admin_panel']['redirect_uri']
time = int(datetime.now().replace(tzinfo=timezone.utc).timestamp() * 1e3)
header = {'Content-Type': 'application/x-www-form-urlencoded'}


def get_token(email, password):
    payload = {
        'grant_type': 'password',
        'client_secret': client_secret,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'username': email,
        'password': password}
    url = 'https://api.ttlock.com/oauth2/token'
    response = requests.request("POST", url, headers=header, data=payload)
    return(response)


def refresh_tocken(refresh_token):
    payload = {
        'grant_type': 'refresh_token',
        'client_secret': client_secret,
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'refresh_token': refresh_token}
    url = 'https://api.ttlock.com/oauth2/token'
    response = requests.request("POST", url, headers=header, data=payload)
    return(response)


def lock_list(accessToken, pageNo):
    url = 'https://api.ttlock.com/v3/lock/list'
    response = requests.request("POST", url, headers=header, data={
        'clientId': client_id,
        'accessToken': accessToken,
        'pageNo': pageNo,
        'pageSize': 50,
        'date': int(datetime.now().timestamp() * 1e3)})
    return(response)


def unlock_records(accessToken, lockId, pageNo):
    url = 'https://api.ttlock.com/v3/lockRecord/list'
    response = requests.request("POST", url, headers=header, data={
        'clientId': client_id,
        'accessToken': accessToken,
        'lockId': lockId,
        'startDate': int((datetime.now() - timedelta(days=7)).timestamp() * 1e3),
        'endDate': int(datetime.now().timestamp() * 1e3),
        'pageNo': pageNo,
        'pageSize': 100,
        'date': int(datetime.now().timestamp() * 1e3)})
    return(response)


def unlock_records_one_day(accessToken, lockId, pageNo):
    url = 'https://api.ttlock.com/v3/lockRecord/list'
    response = requests.request("POST", url, headers=header, data={
        'clientId': client_id,
        'accessToken': accessToken,
        'lockId': lockId,
        'startDate': int((datetime.now() - timedelta(days=1)).timestamp() * 1e3),
        'endDate': int(datetime.now().timestamp() * 1e3),
        'pageNo': pageNo,
        'pageSize': 100,
        'date': int(datetime.now().timestamp() * 1e3)})
    return(response)


def list_passwords(accessToken, lockId, pageNo):
    url = 'https://api.ttlock.com/v3/lock/listKeyboardPwd'
    response = requests.request("POST", url, headers=header, data={
        'clientId': client_id,
        'accessToken': accessToken,
        'lockId': lockId,
        'pageNo': pageNo,
        'pageSize': 50,
        'date': int(datetime.now().timestamp() * 1e3)})
    return(response)


def get_all_unlock_records(accessToken):
    locks = lock_list(accessToken, 1)
    all_locks_id = []
    for i in range(len(locks.json()["list"])):
        all_locks_id.append(locks.json()["list"][i]["lockId"])
    all_unlock_records = []
    for i in range(len(all_locks_id)):
        unlock_record = unlock_records_one_day(accessToken, all_locks_id[i], 1)
        if unlock_record.json()['total'] != 0:
            [all_unlock_records.append(unlock_record.json()["list"][x]) for x in range(len(unlock_record.json()["list"]))]
    return all_unlock_records


def create_password(accessToken, lockId, keyboardPwd, keyboardPwdName, startDate, endDate):
    url = 'https://api.ttlock.com/v3/keyboardPwd/add'
    response = requests.request("POST", url, headers=header, data={
        'clientId': client_id,
        'accessToken': accessToken,
        'lockId': lockId,
        'keyboardPwd': keyboardPwd,
        'keyboardPwdName': keyboardPwdName,
        'startDate': startDate,
        'endDate': endDate,
        'addType': 2,
        'date': int(datetime.now().timestamp() * 1e3)})
    return(response)
