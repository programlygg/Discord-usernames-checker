import requests
import json
import time
from colorama import Fore, Style, init


init(autoreset=True)


with open("config.json", "r") as f:
    config = json.load(f)

DISCORD_TOKEN = config["token"]
WEBHOOK_URL = config["webhook"]
LIST_FILE = config["list_file"]

HEADERS = {
    "authorization": DISCORD_TOKEN,
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0"
}

API_URL = "https://discord.com/api/v9/users/@me/pomelo-attempt"

def banner():
    skull = f"""
{Fore.CYAN}
 VX1 CHECKER
{Style.RESET_ALL}
"""
    print(skull)
    print(Fore.GREEN + "made by @pa7m on discord" + Style.RESET_ALL)
    print()

def send_webhook(msg):
    data = {"content": msg}
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

def check_username(username):
    data = {"username": username}
    response = requests.post(API_URL, headers=HEADERS, json=data)

    if response.status_code == 200:
        res = response.json()
        if res.get("taken") is False:
            print(Fore.GREEN + f"@{username} Claimed !!" + Style.RESET_ALL)
            send_webhook(f"New claim **@{username}**")
        else:
            print(Fore.RED + f"@{username} taken" + Style.RESET_ALL)
    elif response.status_code == 401:
        print(Fore.RED + "Invalid token." + Style.RESET_ALL)
        exit()
    elif response.status_code == 429:
        print(Fore.RED + "Rate limited, waiting..." + Style.RESET_ALL)
        time.sleep(100)
    else:
        print(Fore.RED + f"Error {response.status_code}" + Style.RESET_ALL)


if __name__ == "__main__":
    banner()
    with open(LIST_FILE, "r") as f:
        usernames = [u.strip() for u in f if u.strip()]

    for username in usernames:
        check_username(username)
        time.sleep(1)
