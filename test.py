import requests
import os
import time

base_url = "http://f0fc465d.ngrok.io/api"
token = None
delay = 8


def sign_in(email, password):
    print("Logging in user " + email + password)

    login_data = {
        "email": email,
        "password": password,
        "rememberMe": "true"
    }
    login_url = base_url + "/User/login"
    try:
        r = requests.post(login_url, json=login_data)
    except:
        print("Internet is not available! Exiting..")
        return

    global token
    token = r.json().get('access_token')
    print(token)


def upload_photo(token, file_name):
    print("Uploading " + file_name)
    if token is None:
        print("Haven't got any valid token! You should login first")
        return
    headers = {'Authorization': 'Bearer ' + token}
    url = base_url + "/user/uploadPhoto"
    try:
        file = open(file_name, "rb")
    except FileNotFoundError:
        print("File was not found!")
        return

    photo = {
        "file": file
    }
    requests.post(url, files=photo, headers=headers)
    print("Upload success!")
    print("Removing file...")
    os.remove(file_name)

def get_all_files():
    return list([f for f in os.listdir('.') if os.path.isfile(f)])


def get_all_photos():
    return list(filter(lambda x: x.endswith("png"), get_all_files()))


def print_all_images():
    files = get_all_files()
    for f in files:
        if f.endswith(".png"):
            print(f)


def upload_all_photos():
    photos = get_all_photos()
    if len(photos) == 0:
        print("Oops! Photos are empty, nothing to download")
        return
    for photo in photos:
        upload_photo(token, photo)


config = open("config.json")
text = config.read()
print(text)

sign_in(text.split()[0], text.split()[1])

while True:
    upload_all_photos()
    time.sleep(delay)


