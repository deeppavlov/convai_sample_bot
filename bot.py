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
        print("Observe:")
        if self.chat_id is None:
            if m['message']['text'].startswith('/start '):
                self.chat_id = m['message']['chat']['id']
                self.observation = m['message']['text']
                print("\tStart new chat #%s" % self.chat_id)
            else:
                self.observation = None
                print("\tChat not started yet. Ignore message")
        else:
            if self.chat_id == m['message']['chat']['id']:
                if m['message']['text'] == '/end':
                    self.observation = None
                    print("\tEnd chat #%s" % self.chat_id)
                    self.chat_id = None
                else:
                    self.observation = m['message']['text']
                    print("\tAccept message as part of chat #%s: %s" % (self.chat_id, self.observation))
            else:
                self.observation = None
                print("\tOnly one chat is allowed at a time. Ignore message from different chat #%s" % m['message']['chat']['id'])
        return self.observation

    def act(self):
        print("Act:")
        if self.chat_id is None:
            print("\tChat not started yet. Do not act.")
            return

        if self.observation is None:
            print("\tNo new messages for chat #%s. Do not act." % self.chat_id)
            return

        message = {
            'chat_id': self.chat_id
        }

        texts = ['I love you!', 'Wow!', 'Really?', 'Nice!', 'Hi', 'Hello', '', '/end']
        text = texts[random.randint(0, 7)]

        data = {}
        if text == '':
            print("\tDecide to do not respond and wait for new message")
            return
        elif text == '/end':
            print("\tDecide to finish chat %s" % self.chat_id)
            self.chat_id = None
            data['text'] = '/end'
            data['evaluation'] = {
                'quality': 0,
                'breadth': 0,
                'engagement': 0
            }
        else:
            print("\tDecide to respond with text: %s" % text)
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

    BOT_URL = os.path.join('https://ipavlov.mipt.ru/nipsrouter/', BOT_ID)

    bot = ConvAISampleBot()

    while True:
        try:
            time.sleep(1)
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
        except Exception as e:
            print("Exception: {}".format(e))


if __name__ == '__main__':
    main()
