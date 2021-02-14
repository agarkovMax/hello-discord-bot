import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive

client = discord.Client()

triger = []

response = []

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_neg(neg_word):
  if "negative" in db.keys():
    negative = db["negative"]
    negative.append(negative)
    db["negative"] = negative
  else:
    db["negative"] = [neg_word]

def delete_negative(index):
  negative = db["negative"]
  if len(negative) > index:
    del negative[index]
  db["negative"] = negative  

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

  if msg.startswith("$add_neg"):
    neg_word = msg.split("$add_neg ",1)[1]
    update_neg(neg_word)
    await message.channel.send("New negative word added.")

  if msg.startswith('$remove_neg'):
    negative = []
    if "negative" in db.keys():
      index = int(msg.split("$remove_neg",1)[1])
      delete_negative(index)
      negative = db["negative"]
    await message.channel.send(negative)


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
    
  if msg.startswith("$l_neg"):
    negatives = []
    if "negative" in db.keys():
      negative = db["negative"]
    await message.channel.send(negative)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")
 
 
keep_alive()

client.run(os.getenv('TOKEN'))

