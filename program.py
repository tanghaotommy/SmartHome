import requests
import json

url = 'http://192.168.0.14/test_upload_photo.php'
files =  open('not.png','rb')
r=requests.post(url, data=files)


