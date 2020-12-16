import discord
import os
import requests
import json
import random
from replit import db

client = discord.Client()

no_negative = ['лох','пидр','пидор','хуйло','ебанат','жид','ниггер','дебил','шлюха']

starter_judges = [
  "Осуждаю!",
  "Не одобряю!",
  "Завали свое токсичное ебало!",
  "Ты!"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_judges(judging_message):
  if "judges" in db.keys():
    judges = db["judges"]
    judges.append(judging_message)
    db["judges"] = judges
  else:
    db["judges"] = [judging_message]

def delete_judge(index):
  judges = db["judges"]
  if len(judges) > index:
    del judges[index]
    db["judges"] = judges

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): 
  if message.author == client.user:
    return

  msg = message.content.lower()
  
  if msg.startswith('$hello'):
    await message.channel.send('Hello! :)')

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db["responding"]:
    options = starter_judges
    if "judges" in db.keys():
      options = options + db["judges"] 

    if any(word in msg for word in no_negative):
      await message.channel.send(random.choice(options))


  if msg.startswith("$new"):
    judging_message = msg.split("$new ",1)[1]
    update_judges(judging_message)
    await message.channel.send("New judge added.")
  
  if msg.startswith("$del"):
    judges = []
    if "judges" in db.keys():
      index = int(msg.split("$del", 1)[1])
      delete_judge(index)
      judges = db["judges"]
      await message.channel.send(judges)

  if msg.startswith("$list"):
    judges = []
    if "judges" in db.keys():
      judges = db["judges"]
    await message.channel.send(judges)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
 

client.run(os.getenv('TOKEN'))

