import discord as ds
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



client = ds.Client()  #instance of discord bot


command_list = ["$hello - fun reply", "$help - commands", "$bye - fun reply", "$joke - get a random joke", "$add - add a new anime suggestion for you frnd", "$del - delete suggestion", "$show - shows list", "$respond - followed by true or false"]

anime_word = ["anime", "japan", "korea", "kpop", "AOT", "Re:Zero", "FMAB", "show", "TV", "tv"]

anime_list = ["AOT", "Re:Zero", "Haikyuu", "Solo Leveling", "Beserk", "HunterxHunter", "Naruto"]

if "response" not in db.keys():
  db["response"] = True
  


def get_joke():
  response = requests.get("https://official-joke-api.appspot.com/random_joke")
  json_data = json.loads(response.text)
  joke = json_data['setup'] + '\n' + json_data['punchline'] 
  return (joke) 


def get_helps():
  text = " "
  for i in range(len(command_list)):
    text = text + command_list[i] + '\n'  
  text = text + "\n These are the basic functions one can use on this bot. Many more to come!"
  return (text)  

def add_anime(suggestion): 
  if "anime" in db.keys():
    anime = db["anime"]
    anime.append(suggestion)
    db["anime"] = anime
  else:
    db["anime"] = [suggestion]


def del_anime(index):
  anime = db["anime"]
  if len(anime) > index:
    anime.pop(index)
    db["anime"] = anime



@client.event   #authorizes an event
async def on_ready():   #on ready event 
  print("I, an autonomous being has logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$hello"): 
    await message.channel.send("Heyoo, how's it going?")
  
  if msg.startswith("$bye"):
    await message.channel.send("Hasta la vista")
  
  if msg.startswith("$joke"):
    joke = get_joke()
    await message.channel.send(joke)
  
  if msg.startswith("$help"):
    text = get_helps()
    await message.channel.send(text)

  if db["response"]:
    choices =  anime_list
    if "anime" in db.keys():
      x = list(db["anime"])
      choices = choices + x

    if any (word in msg for word in anime_word):
      await message.channel.send("You should watch: " + random.choice(choices))

  if msg.startswith("$add"):
   anime_sugg = msg.split("$add ", 1)[1] 
   add_anime(anime_sugg)
   await message.channel.send("Your recommended show has been added to the database successfully!")

  if msg.startswith("$del"):
   anime = []
   if "anime" in db.keys():
     index = int(msg.split("$del",1)[1])
     del_anime(index)
     anime = db["anime"]
     await message.channel.send("The new list is: {}".format(anime.value))

  if msg.startswith("$show"):
    anime = []
    if "anime" in db.keys():
      anime = db["anime"]
    await message.channel.send(anime)

  if msg.startswith("$respond"):
    value = msg.split("$respond ", 1)[1]
    if value.lower() == "true":
      db["response"] = True
      await message.channel.send("Response on")
    else: 
      db["response"] = False
      await message.channel.send("Response off")



keep_alive()
client.run(os.getenv('Token'))
