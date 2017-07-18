# Sample bot for convai.io challenge
Bot demonstrates how to use RouterBot API to communicate with telegram users. Bot supports only one dialogue at a time and should be used only for testing purpose. Do not run more then one instance of bot with same BOT_ID.

## Clone repo
```sh
git clone https://github.com/seliverstov/convai_sample_bot/
cd convai_sample_bot
pip install
```
## Edit bot.py and enter your bot id
```python
def main():
    """
    !!!!!!! Put your bot id here !!!!!!!
    """
    BOT_ID = None
```
## Run bot (python 3 required)
```sh
python bot.py
```
## Start chattings
Open telegram client, find @ConvaiBot (convai-bot), send "/test PUT_YOUR_BOT_ID_HERE" to start chatting with your own bot

>**WARNING:** if you start chatting with command /begin then @ConvaiBot will connect your with random bot or human. To evaluate your own bot you should use the command /test with your bot id
