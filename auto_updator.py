import requests
import base64
import os
import sys
import json

with open("config.json", "r") as file:
    configjson = json.load(file)

if configjson["auto_updator"]["enabled"] == True:
    repository_owner = configjson["auto_updator"]["github_repository_owner"]
    repository_name = configjson["auto_updator"]["github_repository_name"]
    a = requests.get(f"https://api.github.com/repos/{repository_owner}/{repository_name}/git/trees/master?recursive=1")

    if a.headers["X-RateLimit-Remaining"] != 0 and a.status_code != 403:
        if a.status_code == 200:

            print("Checking for Updates\n\n\n\n\n")

            b = a.json()

            d = []

            for c in b["tree"]:
                if c["type"] != "tree":
                    d.append(c["path"])

            for e in d:
                f = requests.get(f"https://api.github.com/repos/{repository_owner}/{repository_name}/contents/" + e)
                if f.status_code == 200:
                    g = f.json()
                    if os.path.exists(e) == True:
                        print(f"Checking Updates for {e}")
                    currently_in_dir = False
                    for k in e:
                        if k == "/":
                            currently_in_dir = True

                    if currently_in_dir == True:
                        os.makedirs(os.path.dirname(e), exist_ok=True)
                    if os.path.exists(e) == True:
                        with open(e, "rb") as filerb:
                            with open(e, "wb") as filewb:
                                if filerb.read().decode("utf-8") != base64.b64decode(g["content"]).decode("utf-8"):
                                    print(f"Update found for {e}")
                                    print(f"Updating {e}")
                                    filewb.write(base64.b64decode(g["content"]))
                                    print(f"Successfully updated {e}\n\n\n\n\n")
                                else:
                                    print(f"No update found for {e}\n\n\n\n\n")
                    else:
                        with open(e, "wb") as filewb:
                            print(f"Found new file in github repository ({e})")
                            print(f"Downloading {e}")
                            filewb.write(base64.b64decode(g["content"]))
                            print(f"Successfully Downloaded {e}\n\n\n\n\n")
                else:
                   sys.stderr.write(f"{f.status_code}: Error finding the file {e} at https://github.com/{repository_owner}/{repository_name}/tree/master/{e} . Please make sure you put the right repository name and owner in the config.json file.") 
        else:
            sys.stderr.write(f"{f.status_code}: Error finding the github repository at https://github.com/{repository_owner}/{repository_name} . Please make sure you put the right repository name and owner in the config.json file.")
    else:
        sys.stderr.write("Auto Updator Error: You are being rate limited, Please try again in one hour.\n")
        print("(Note: this does not mean the bot will not run it only means the auto updator will not check for updates right now.)")
