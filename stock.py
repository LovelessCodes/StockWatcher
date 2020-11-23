import os
import json
import time
import random
import requests
import threading
from colorama import Style, Fore

os.system("cls")
data = {}

with open('token.json') as f:
    data = json.load(f)
token = data['token']
server_ids = ["743007671724277781", "763479037497966593"]
servers = []
api = "https://discord.com/api/v8"
s = requests.Session()
s.headers.update({"Authorization": token})
user = s.get(f"{api}/users/@me").json()
msg_list = [
    "Bro <@<ID>>, I can take the stock off your hands if you're down?",
    "<@<ID>>, don't mind me, taking that stock? ;)",
    "<@<ID>>, ready to take ur stock"
]

def has_read(num):
    return (int(num) & 0x400) == 0x400

def get_channels(server_id):
    ser = s.get(f"{api}/guilds/{server_id}").json()
    t = s.get(f"{api}/guilds/{server_id}/channels").json()
    st = None
    ti = None
    for ch in t:
        hg = None
        for us in ch['permission_overwrites']:
            if us['id'] == user['id']:
                hg = us
        if hg:
            if has_read(hg['deny']):
                continue
        if "stock" in ch['name'].lower():
            st = ch['id']
        elif ("ticket" in ch['name'].lower() and not ("tickets" in ch['name'].lower() or "create" in ch['name'].lower())) and (hg and has_read(hg['allow'])):
            ti = ch['id']
    if st and ti:
        return {"stock": st, "ticket": ti, "id": server_id, "name": ser['name']}
    return None

def next_one(num, uid):
    if num > len(msg_list)-1:
        num = random.randint(0, len(msg_list)-1)
    return msg_list[num].replace("<ID>", str(uid))

def run_guild():
    nonce = 0
    serv = servers.pop()
    while True:
        t = s.get(f"{api}/channels/{serv['stock']}/messages?limit=1").json()
        if "message" in t:
            time.sleep(t['retry_after'])
            continue
        skipper = t[0]['id']
        break
    while True:
        t = s.get(f"{api}/channels/{serv['stock']}/messages?limit=1").json()
        if "message" in t:
            time.sleep(t['retry_after'])
            continue
        if t[0]['id'] == skipper:
            continue
        if t[0]['mention_everyone'] and len(t[0]['attachments']) > 0:
            cr = t[0]['author']
            print(f"[{Fore.YELLOW}~{Style.RESET_ALL}] New stock on {serv['name']} by {cr['id']}!")
            msg = next_one(nonce, cr['id'])
            s.post(f"{api}/channels/{serv['ticket']}/typing")
            time.sleep(1)
            k = s.post(f"{api}/channels/{serv['ticket']}/messages", json={"content": msg, "tts": False})
            if k.status_code == 200:
                skipper = t[0]['id']
                nonce += 1
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Sent message in {serv['name']} for a stock!")
        time.sleep(1)

for sc in server_ids:
    kg = get_channels(sc)
    if kg:
        servers.append(kg)

t_list = []
for server in servers:
    print(f"[{Fore.LIGHTBLUE_EX}>{Style.RESET_ALL}] Starting thread for: {server['name']}")
    t_list.append(threading.Thread(target=run_guild))

[t.start() for t in t_list]
[t.join() for t in t_list]
