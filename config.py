import os

# ### TELEGRAM ### #
# generate token here: https://telegram.me/BotFather
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
# add bot to channel, send some message, then get update and find chat_id
TELEGRAM_CHANNEL_ID = os.environ['TELEGRAM_CHANNEL_ID']
####################

# ###DATABASE### #
DB_FILE = os.getenv('DB_FILE', './database.sqlite3')
##################
