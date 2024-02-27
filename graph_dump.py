import os
import sys
import json
import time
import base64
import urllib.request
from pathlib import Path

def send_request(url, jwt, json_decode = True):
    headers = {"Authorization": "bearer %s" % jwt}
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req).read()
    if json_decode:
        return json.loads(data)
    return data

def process_data(data, jwt, path):
      for email in data["value"]:
            try:
                fd = open(os.path.join(path, "report.html"), "a+")
                fd.write("<hr><br>")
                fd.write("ID: %s <br>" % email["id"])
                fd.write("Received Date: %s <br>" % email["receivedDateTime"])
                fd.write("Has Attachments: %s <br>" % email["hasAttachments"])
                if email["hasAttachments"]:
                     filename = fetch_attachment(email["id"], jwt, path)
                     fd.write('Attachment URL: <a href="%s">%s</a><br>' % (filename, filename))
                fd.write("From: %s %s <br>" % (email["from"]["emailAddress"]["name"], email["from"]["emailAddress"]["address"]))
                fd.write("Subject: %s <br>" % email["subject"])
                fd.write("Body: %s <br>" % email["body"]["content"])
                fd.close()
            except Exception as e:
                print("Something when wrong: %s" % e)

def fetch_attachment(email_id, jwt, path):
    url = "https://graph.microsoft.com/v1.0/me/messages/%s/$value" % email_id
    print("Fetching attachment url: %s" % url)
    data = send_request(url, jwt, False)
    filename, data = parse_data(data)
    filename = "%s-%s" % (email_id[:32], filename)
    open(os.path.join(path, filename), "wb+").write(data)
    return filename

def parse_data(data):
     filter = 'Content-Disposition: attachment; filename="'
     data = data.decode()
     position = data.find(filter) + len(filter)
     data = data[position:]
     filename = data[:data.find('"')]

     data = data[data.find("\r\n\r\n") + 4:]
     data = data[:data.find("\r\n\r\n")].strip().replace("\r", "").replace("\n", "")

     try:
         data = base64.b64decode(data)
     except Exception as e:
         print("Base64 failed on attachment: %s" % e)

     return [filename, data]

filter = ""
iterator = 1
if len(sys.argv) > 2:
        filter = '?$search="%s"' % sys.argv[2]

url = "https://graph.microsoft.com/v1.0/me/messages%s" % filter

jwt = Path(sys.argv[1]).read_text().strip()

path = str(int(time.time()))
os.mkdir(path)

print("Report path: %s" % os.path.join(path, "report.html"))
print("Fetching URL: %s" % url)

data = send_request(url, jwt)
process_data(data, jwt, path)
print("Page %d completed" % iterator)

while "@odata.nextLink" in data:
      print("Page %d completed" % iterator)
      data = send_request(data["@odata.nextLink"], jwt)
      process_data(data, path)
      iterator += 1

print("Process completed")
