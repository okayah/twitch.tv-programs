##[ IMPORTS ]##
import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
from os.path import dirname, join
from colorama import Fore, init
init()

##[ LOAD FILES ]##
config = json.load(open(join(dirname(__file__), "./config.json")))
try:
    r = requests.post('https://id.twitch.tv/oauth2/token', {
        'client_id': config['Authentication']['client_id'],
        'client_secret': config['Authentication']['client_secret'],
        "grant_type": 'client_credentials'
    })
    headers = {
        'Client-ID': config['Authentication']['client_id'],
        'Authorization': 'Bearer ' + r.json()['access_token']
    }
except KeyError:
    print(Fore.LIGHTRED_EX + 'Please input a client_id & client_secret.')
    quit()


##[ FUNCTIONS ]##
old = []
def send_webhook(content):
    wh = config['Settings']['Webhook']['URL']
    delete_after = config['Settings']['Webhook']['Delete_After']
    delete_after_time = config['Settings']['Webhook']['Delete_After_Time']

    webhook = DiscordWebhook(url=config['Settings']['Webhook']['URL'],rate_limit_retry=True)
    embed = DiscordEmbed(title=content, color=config['Settings']['Webhook']['Color'])
    webhook.add_embed(embed)
    sent = webhook.execute()
    if delete_after:
        time.sleep(delete_after_time)
        webhook.delete(sent)

def get_latest_followers():
    r = requests.get(f'https://api.twitch.tv/helix/users/follows?to_id={userid}&first=100',headers=headers)
    for follow in r.json()['data']:
        name = follow['from_name']
        if name in old:
            pass
        else:
            if len(old) < 100:
                pass
                old.append(name)
            else:
                print(Fore.LIGHTGREEN_EX+name,'has just followed you!')
                if config['Settings']['Webhook'] != "":
                    send_webhook(name+' has just followed you!')
                old.append(name)


##[ MAIN CODE ]##
user = requests.get('https://api.twitch.tv/helix/users?login='+config['Settings']['Username'], headers=headers).json()
userid = user['data'][0]['id']
username = user['data'][0]['login']

send_webhook('> Started')
while(True):
    get_latest_followers()
    time.sleep(5)