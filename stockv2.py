import asyncio
import json
import time
import requests
import traceback
import random
from os import system
from discord.ext import commands
from colorama import Fore, Style
import platform

data = {}

with open('token.json') as f:
    data = json.load(f)
token = data['token']

server_ids = ["743007671724277781", "763479037497966593"]
servers = {}
api = "https://discord.com/api/v8"
s = requests.Session()
s.headers.update({"Authorization": token})
user = s.get(f"{api}/users/@me").json()
snipes = 0
emotes = [
    ":man_raising_hand:",
    ":eyes:",
    ":comet:"
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

for sc in server_ids:
    kg = get_channels(sc)
    if kg:
        servers[sc] = kg

os = platform.system()

if os == "Windows":
    system("cls")
    system("title StockWatcher by Loveless#2020")
else:
    system("clear")
    print(chr(27) + "[2J")

print(Fore.RED + """StockWatcher by Loveless#2020 - v. 2""" + Fore.RESET)

bot = commands.Bot(command_prefix=".", self_bot=True)
ready = False

while 1:
    try:
        @bot.event
        async def on_message(ctx):
            global ready
            if not ready:
                print(f"{Fore.LIGHTCYAN_EX}Sniping Stocks on {str(len(servers))} Servers 🔫\n{Fore.RESET}")
                print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                print(f"[{Fore.GREEN}+{Style.RESET_ALL}] Sniper is ready")
                ready = True
            start_time = time.time()
            if ctx.guild and str(ctx.guild.id) in servers and "stock" in ctx.channel.name.lower() and ctx.mention_everyone:
                print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                chan = bot.get_channel(int(servers[str(ctx.guild.id)]['ticket']))
                await chan.send(f"<@{ctx.author.id}> {random.choice(emotes)}")
                delay = (time.time() - start_time)
                try:
                    print(f"[{Fore.LIGHTGREEN_EX}-{Fore.RESET}] Sniped stock: From {Fore.LIGHTRED_EX}{ctx.author.name}#{ctx.author.discriminator}{Fore.RESET}{Fore.LIGHTMAGENTA_EX} [{ctx.guild.name} > {ctx.channel.name}]{Fore.RESET}")
                except:
                    print(f"[{Fore.LIGHTGREEN_EX}-{Fore.RESET}] Sniped stock: From {Fore.LIGHTRED_EX}{ctx.author.name}#{ctx.author.discriminator}{Fore.RESET}")
                print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                print(" Delay:" + Fore.GREEN + " %.3fs" % delay + Fore.RESET)
                try:
                    await ctx.add_reaction("🔥")
                    print(Fore.LIGHTBLUE_EX + time.strftime("%H:%M:%S ", time.localtime()) + Fore.RESET, end='')
                    print(f"[{Fore.LIGHTGREEN_EX}~{Fore.RESET}] Added Reactions 👀{Fore.RESET}")
                except Exception:
                    pass

        bot.run(token, bot=False)
    except:
        file = open("traceback.txt", "w")
        file.write(traceback.format_exc())
        file.close()
        exit(0)
