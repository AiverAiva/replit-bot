import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from threading import Thread
from flask import Flask
from utilties.multicog import apply_multicog

token = os.getenv('TOKEN')

app = Flask(__name__)



@app.route('/')
def hello():
    return 'Your Bot Is Ready'

def run():
  app.run(host="0.0.0.0", port=8000)
  
if __name__ == '__main__':
  server = Thread(target=run)
  server.start()

intents = discord.Intents.default()
bot=commands.Bot(command_prefix="/", intents=intents)
status = cycle(['You <3'])

@bot.event
async def on_ready():
  change_status.start()
  print('{0.user} wake the fuck up'.format(bot))

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(status)))

bot.load_extension("cogs", recursive=True)
apply_multicog(bot)
# for root, dirs, files in os.walk("./cogs"):
#     for dir in dirs:
#         for file in os.listdir(os.path.join(root, dir)):
#             if file.endswith(".py"):
#                 file_path = os.path.join(root, dir, file)
#                 module_path = os.path.relpath(file_path, './cogs').replace(os.path.sep, '.')[:-3]
#                 bot.load_extension(f'cogs.{module_path}')
          
bot.run(token)