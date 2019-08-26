import requests
import json

username = ""
base_URL = "http://35.203.115.88/"
session = requests
password = ""
access_token = ""

def login(username_l, password_l):
    global password
    password = password_l
    global username
    username = username_l
    data = json.dumps({'username': username, 'password': password})
    r = requests.put(base_URL+"web_app/login/", data=data)
    r = json.loads(r.text)
    global access_token
    access_token = r["access_token"]
    print(access_token)
    if "Error" in r:
        print(r)

def error_handle_get(r):
    try:
        c = r.status_code
        r = json.loads(r.text)
    except:
        print({"Error":"No data received"})
    if "Error" in r:
        print(r)
        if r["Error"] == "Not logged in":
            login(username, password)
    return r, c


def get_farm_access():
    r = session.get(base_URL+"web_app/farm_access/", headers={"access-token":access_token})
    data, code = error_handle_get(r)
    print(data)
    print(code)


def get_farm_summary(core_id):
    # core_id -> check match'
    r = session.get(base_URL+"web_app/farm_summary/", params={"core_id":1}, headers={"access-token":access_token})
    data, code = error_handle_get(r)
    print(data)

def get_channel_summary(core_id, channel_name):
    # core_id -> check match'
    r = session.get(base_URL+"web_app/channel_summary/", params={"core_id":1, "name":channel_name}, headers={"access-token":access_token})
    data, code = error_handle_get(r)
    print(data)

def get_robot_summary(core_id, channel_name):
    # core_id -> check match'
    r = session.get(base_URL+"web_app/robot_summary/", params={"core_id":1}, headers={"access-token":access_token})
    data, code = error_handle_get(r)
    print(data)

def head_verify_token():
    r = session.get(base_URL+"web_app/verify_token/", headers={"access-token":access_token})
    data, code = error_handle_get(r)
    print(data)

key = "ByeFelicia"
username = "Eric"
login(username, key)
get_farm_access()
get_farm_summary(1)
get_channel_summary(1, "A4")
get_robot_summary(1, "A4")

head_verify_token()
# eric, ByeFelicia -> worker account

# Then add to subscriptions

