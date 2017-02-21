import requests
import configparser
import json

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

    def feed(self):
        return self.post_to_api(json.dumps({"bar": "food"}))

    def attention(self):
        return self.post_to_api(json.dumps({"bar": "attention"}))

    def knowledge(self):
        return self.post_to_api(json.dumps({"bar": "knowledge"}))

    def post_to_api(self, payload):
        with requests.Session() as s:
            r = s.post("https://api.kamergotchi.nl/game/care", headers=self.headers, verify=True, data=payload)
            response = r.json()
            remaining = response['game']['careLeft']
            print(remaining)

if __name__ in '__main__':
    Game = Care()
    Game.post_to_api(json.dumps({"bar": "food"}))

