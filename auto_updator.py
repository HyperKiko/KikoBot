import requests
import os
import json

with open("config.json", "r") as filer:
    jsonfile = json.load(filer)

file_in_folder = False
url = jsonfile["auto_updator"]["github_raw_url"]
for file_or_dir in os.walk(os.getcwd()):
    if file_or_dir[0].startswith(os.getcwd()) and file_or_dir[0] != os.getcwd():
        file_in_folder = True
        folder = file_or_dir[0][len(os.getcwd()) + 1:len(file_or_dir[0])]
    elif file_or_dir[0] == os.getcwd():
        file_in_folder = False

    if file_in_folder == True:
        for a in file_or_dir[2]:
            if a != "config.json":
                file = folder + "/" + a
                b = requests.get(url + "/" + file)
                if int(b.status_code) != 404:
                    with open(file, "w") as c:
                        c.write(b.text)

    elif file_in_folder == False:
        for a in file_or_dir[2]:
            if a != "config.json":
                file = a
                b = requests.get(url + "/" + file)
                if int(b.status_code) != 404:
                    with open(file, "w") as c:
                        if file != "config.json":
                            c.write(b.text)
