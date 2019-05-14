import numpy as np
import requests
import time
import sys
import json
import os
import files
import datetime

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
    print(f"got token {token}")


def upload_all_details(file_name):
    global token
    if token is None:
        print("Haven't got any valid token! You should login first")
        return

    photos = files.get_all_photos()
    if len(photos) == 0:
        print("Oops! Photos are empty, nothing to upload")
        return
    for photo in photos:
        upload_detail(photo)


def upload_detail(photo):
    # TODO: Get values from open cv
    values = [1.4, 1.6]
    deviations_config = config["deviations"]
    ids = list(map(lambda x: x["id"], deviations_config))
    deviations = dict(zip(ids, values))
    upload_quality_params(deviations)


def upload_photo(file_name):
    global token
    headers = {'Authorization': 'Bearer ' + token}

    url = base_url + "/uploadPhoto"
    print("Uploading photo" + file_name)
    try:
        file = open(file_name, "rb")
    except FileNotFoundError:
        print("File was not found!")
        return

    photo = {
        "file": file
    }
    data = {
        "description": f"photo from IoT {datetime.datetime.now()}"
    }
    requests.post(url, files=photo, headers=headers, data=data)
    print("Upload success!")
    print("Removing file...")
    os.remove(file_name)


def upload_quality_params(deviations):
    for deviationId, value in deviations.items():
        add_quality_param(deviationId, f"deviation from IoT {datetime.datetime.now()}", value)


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
    requests.post(url, json=data, headers=headers)


try:
    config = json.loads((open("config.json").read()))
except IOError:
    print("Failed reading config. Please create config.json to login")
    sys.exit()

print(config)
sign_in(config["login"], config["password"])

upload_photo("1.png")

while True:
    # upload_all_photos()
    time.sleep(delay)
