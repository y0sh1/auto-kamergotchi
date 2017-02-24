import requests
import configparser
import json
from datetime import datetime


class Care:
    token = None
    config = configparser.ConfigParser()

    url = ""
    headers = {'User-Agent': '',
               'x-player-token': '',
               'content-type': 'application/json;charset=utf-8'}

    def __init__(self):
        self.config.read('config.ini')
        self.headers['x-player-token'] = self.config['kamergotchi']['token']
        self.headers['User-Agent'] = self.config['kamergotchi']['useragent']
        self.url = self.config['kamergotchi']['url']

    def fill_up(self):
        response = self.game_info()
        while 'message' not in response:
            stats = response['game']['current']
            lowest_stat = lowest(stats)
            response = self.post_to_api(json.dumps({"bar": lowest_stat}))

        print("All filled up for now")

    def feed(self):
        return self.post_to_api(json.dumps({"bar": "food"}))

    def attention(self):
        return self.post_to_api(json.dumps({"bar": "attention"}))

    def knowledge(self):
        return self.post_to_api(json.dumps({"bar": "knowledge"}))

    def game_info(self):
        with requests.Session() as s:
            r = s.get(self.url + "/game", headers=self.headers, verify=True)
            response = r.json()
            return response

    def check_claim(self):
        response = self.game_info()
        if 'message' not in response:
            current_time = datetime.now()
            last_reset_time = datetime.strptime(response['game']['claimReset'], "%Y-%m-%dT%H:%M:%S.%fZ")
            claim_diff = (current_time - last_reset_time).total_seconds()
            claim_diff += 3600 # Offset to fix timezone aids
            if claim_diff >= response['game']['claimLimitSeconds']:
                self.claim_bonus()
                print("We claimed a bonus")

    def claim_bonus(self):
        with requests.Session() as s:
            r = s.post(self.url + "/game/claim", headers=self.headers, verify=True)
            response = r.json()
            return response

    def post_to_api(self, payload):
        with requests.Session() as s:
            r = s.post(self.url + "/game/care", headers=self.headers, verify=True, data=payload)
            response = r.json()
            if 'message' in response:
                print(response['message'])
            else:
                print(response)
                remaining = response['game']['careLeft']
                print("%d remaining" % remaining)
            return response


def lowest(dictionary):
    """Return the key from a dictionary that has the lowest value"""
    return min(dictionary.items(), key=lambda x: x[1])[0]


if __name__ in '__main__':
    Game = Care()
    Game.fill_up()
    Game.check_claim()
