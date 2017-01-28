import requests
import json
import time

def Analysis(response):
    status = response['Status']
    if status == 3:
        print "No notification"
    elif status == 4:
        index = 1
        print "New Notification"
        while response.has_key(str(index)):
            msg = response[str(index)]
            Type = msg['Type']
            content = msg['Content']
            if Type == '2':
                print "Open the door"
            index = index + 1
    elif status == 0:
        print "User username cannot be empty!"
    elif status == 1:
        print "Cannot access the database!"
    elif status == 2:
        print "No such user username!"

notificationURL = 'http://192.168.0.14/notification.php'
username = 'rp'
payload = {'Username': username}
payload = json.dumps(payload)
while True:
    r=requests.post(notificationURL, data=payload)
    response = r.json()
    Analysis(response)
    time.sleep(3)