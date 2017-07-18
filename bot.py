"""
Copyright 2017 Neural Networks and Deep Learning lab, MIPT

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import requests
import os
import json
import time
import random


class ConvAISampleBot:

    def __init__(self):
        self.chat_id = None
        self.observation = None

    def observe(self, m):
        if self.chat_id is None and m['message']['text'].startswith('/start '):
            self.chat_id = m['message']['chat']['id']
            print("Start new chat #%s" % self.chat_id)
        elif self.chat_id is not None and m['message']['text'] == '/end':
            print("End chat #%s" % self.chat_id)
            self.chat_id = None
            self.observation = None
            return

        if self.chat_id is None:
            print("Dialog not started yet. Ignore message.")
        elif m['message']['chat']['id'] == self.chat_id:
            print("Accept message as part of chat #%s" % self.chat_id)
            self.observation = m['message']['text']
            return self.observation
        else:
            print("Multiple dialogues are not allowed. Ignore message.")

    def act(self):
        if self.chat_id is None:
            print("Dialog not started yet. Do not act.")
            return

        message = {
            'chat_id': self.chat_id
        }

        texts = ['I love you!', 'Wow!', 'Really?', 'Nice!', 'Hi', 'Hello', '', '/end']
        text = texts[random.randint(0, 7)]

        data = {}
        if text == '':
            print("Decided to do not respond and wait for new message")
            return
        elif text == '/end':
            print("Decided to finish chat %s" % self.chat_id)
            self.chat_id = None
            data['text'] = '/end'
            data['evaluation'] = {
                'quality': 0,
                'breadth': 0,
                'engagement': 0
            }
        else:
            print("Decided to respond with text: %s" % text)
            data = {
                'text': text,
                'evaluation': 0
            }

        message['text'] = json.dumps(data)
        return message


def main():

    """
    !!!!!!! Put your bot id here !!!!!!!
    """
    BOT_ID = None

    if BOT_ID is None:
        raise Exception('You should enter your bot token/id!')

    BOT_URL = os.path.join('https://convaibot.herokuapp.com/', BOT_ID)

    bot = ConvAISampleBot()

    while True:
        print("Get updates from server")
        res = requests.get(os.path.join(BOT_URL, 'getUpdates'))

        if res.status_code != 200:
            print(res.text)
            res.raise_for_status()

        print("Got %s new messages" % len(res.json()))
        for m in res.json():
            print("Process message %s" % m)
            bot.observe(m)
            new_message = bot.act()
            if new_message is not None:
                print("Send response to server.")
                res = requests.post(os.path.join(BOT_URL, 'sendMessage'),
                                    json=new_message,
                                    headers={'Content-Type': 'application/json'})
                if res.status_code != 200:
                    print(res.text)
                    res.raise_for_status()
        print("Sleep for 1 sec. before new try")
        time.sleep(1)


if __name__ == '__main__':
    main()
