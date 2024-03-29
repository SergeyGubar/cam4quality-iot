import numpy as np
import requests
import time
import sys
import json
import os
import files
import datetime
import parameters_analyzer

base_url = "http://159.89.145.225:8080/api"
token = None
delay = 5
config = None


def sign_in(email, password):
    print("Logging in user " + email + " " + password)

    login_data = {
        "email": email,
        "password": password
    }
    login_url = base_url + "/User/login"
    try:
        r = requests.post(login_url, json=login_data)
    except:
        print("Internet is not available! Exiting..")
        return

    global token
    token = r.json().get('access_token')
    print("got token" + token)


def upload_all_details():
    global token
    if token is None:
        print("Haven't got any valid token! You should login first")
        return

    photos_names = files.get_all_photos_names()
    if len(photos_names) == 0:
        print("Oops! Photos are empty, nothing to upload")
        return
    for photo in photos_names:
        upload_detail(photo)


def upload_detail(photo):
    url = base_url + "/addDetail"
    global token
    headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}

    values = parameters_analyzer.get_params(photo)
    deviations_config = config["deviations"]
    ids = list(map(lambda x: x["id"], deviations_config))
    deviations = dict(zip(ids, values))
    params_ids = upload_quality_params(deviations)
    photo_id = upload_photo(photo)
    data = {
        'detailQualityParamsIds': params_ids,
        'photoId': photo_id,
        'factoryId': config["factoryId"]
    }
    print("Uploading detail..")
    r = requests.post(url, headers=headers, json=data)
    os.remove(photo)
    print(r.status_code)


def upload_photo(file_name):
    global token
    headers = {'Authorization': 'Bearer ' + token}

    url = base_url + "/uploadPhoto"
    print("Uploading photo " + file_name)
    try:
        file = open(file_name, "rb")
    except FileNotFoundError:
        print("File was not found!")
        return

    day = datetime.datetime.today().day
    month = datetime.datetime.today().month
    year = datetime.datetime.today().year

    photo = {
        "file": file
    }
    data = {
        "description": "IoT " + str(day) + "/" + str(month) + "/" + str(year)
    }
    r = requests.post(url, files=photo, headers=headers, data=data)
    print("Upload success!")
    print("Removing file...")
    print(r.json()["id"])
    return r.json()["id"]


def upload_quality_params(deviations):
    result = []
    day = datetime.datetime.today().day
    month = datetime.datetime.today().month
    year = datetime.datetime.today().year
    for deviationId, value in deviations.items():
        qp_id = add_quality_param(deviationId, "IoT " + str(day) + "/" + str(month) + "/" + str(year), value)
        result.append(qp_id)
    return result


def add_quality_param(deviation_id, name, value):
    global token
    if token is None:
        print("Haven't got any valid token! You should login first")
        return
    headers = {'Authorization': 'Bearer ' + token}
    url = base_url + "/addQualityParam"
    data = {
        "qualityParamDeviationId": deviation_id,
        "name": name,
        "standardValue": value
    }
    r = requests.post(url, json=data, headers=headers)
    param_id = r.json()["id"]
    print("Add quality param: " + str(param_id))
    return param_id


try:
    config = json.loads((open("config.json").read()))
except IOError:
    print("Failed reading config. Please create config.json to login")
    sys.exit()

print(config)
sign_in(config["login"], config["password"])

while True:
    upload_all_details()
    time.sleep(delay)
