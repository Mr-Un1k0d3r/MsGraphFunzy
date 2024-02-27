import os
import sys
import json
import time
import base64
import urllib.request
from pathlib import Path

def put_request(url, token, data, json_decode = True):
        headers = {"Authorization": "Bearer %s" % token, "Content-Type": "application/octet-stream"}
        req = urllib.request.Request(url, headers=headers, method="PUT", data=data)
        data = urllib.request.urlopen(req).read()
        if json_decode:
                return json.loads(data)
        return data

def post_request(url, token, data, json_decode = True):
        headers = {"Authorization": "Bearer %s" % token, "Content-Type": "application/json"}
        req = urllib.request.Request(url, headers=headers, method="POST", data=data)
        data = urllib.request.urlopen(req).read()
        if json_decode:
                return json.loads(data)
        return data

if len(sys.argv) < 4:
        print("Missing arguments: %s azure_token_file file_to_upload remote_filename" % sys.argv[0])
        exit()

put_url = "https://graph.microsoft.com/v1.0/me/drive/root:/%s:/content" % sys.argv[3]


print("*** WARNING IF THE FILE IS BIGGER THAN 4 Mb it will fail\r\n")
print("Pushing to the following URL: %s" % put_url)

jwt = Path(sys.argv[1]).read_text().strip()
data = open(sys.argv[2], "rb").read()


data = put_request(put_url, jwt, data)


print("webUrl: %s" % data["webUrl"])
print("ID: %s" % data["id"])
print("Making it shareable...")

share_url = "https://graph.microsoft.com/v1.0/me/drive/items/%s/createLink" % data["id"]

permission = b'{"type": "view", "scope": "anonymous"}'
if "-organization" in sys.argv:
        permission = b'{"type": "view", "scope": "organization"}'

data = post_request(share_url, jwt, permission)

print("Shareable link is: %s" % data["link"]["webUrl"])
print("Process completed")
