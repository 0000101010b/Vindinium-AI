import vindinium
import pandas as pd

from bot_B import RandomBot

# Create a vindinium client
client = vindinium.Client(
    key='6nrsobfc',                 # your bot code
    mode='training',                # 'training' or 'arena'
    n_turns=300,                    # only valid for training
    server='http://vindinium.org', # if local, or 'http://vindinium.org'
    open_browser=True               # if true, it open the browser when
                                    #    game starts
)


url = client.run(RandomBot())
print ('Replay in:', url)


