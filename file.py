from poe_api_wrapper import PoeExample
from poe_api_wrapper import PoeApi

token = "5kpmWSkg6ysb6dThRM9Q_A%3D%3D"
client = PoeApi(token)

# Using Client with proxy (default is False)
client = PoeApi(token, proxy=True)
bot = 'ChatGPT'
message = 'write an article about communism'

for chunk in client.send_message(bot, message):
    article = print(chunk["response"], end="", flush=True)
print(article)