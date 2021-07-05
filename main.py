import discord
import os
import requests
import json
from replit import db
from keep_alive import keep_alive
from discord.ext import  tasks, commands


client = discord.Client()

def get_shlepa():
  shlepa = 'https://memepedia.ru/wp-content/uploads/2020/10/screenshot_10-3.png'
  return shlepa
if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def get_cat():
  response = requests.get('https://api.thecatapi.com/v1/images/search')
  response = response.json()
  image = response[0]['url']
  return(image)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))




@client.event
async def on_message(message): 
  if message.author == client.user:
    return

  msg = message.content.lower()
  
  if msg.startswith('привет'):
    author = str(message.author)[:-5]
    await message.channel.send('Привет, ' + author + "!")

  if msg.startswith('hello'):
    author = str(message.author)[:-5]
    await message.channel.send('Hello, ' + author + "!")

  if msg.startswith('цитата'):
    quote = get_quote()
    await message.channel.send(quote)

  if msg.startswith('cat'):
    cat = get_cat()
    await message.channel.send(cat)

  if msg.startswith('кот'):
    cat = get_cat()
    await message.channel.send(cat)

  if msg.startswith('большой русский кот'):
    shlepa = get_shlepa()
    await message.channel.send(shlepa)

  if msg.startswith('шлёпа'):
    shlepa = get_shlepa()
    await message.channel.send(shlepa)

# turn on and off responding
  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
 

class MyCog(commands.Cog):
  @tasks.loop(seconds=300)

  async def send_quote():
    channel = client.get_channel(788712072086028338)
    quote = get_quote()
    print(quote)
    await channel.send(quote)
    
  send_quote.start()
 




keep_alive()

client.run(os.getenv('TOKEN'))

