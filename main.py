import discord
import os
from random import randint
import pandas as pd

client = discord.Client()

def file_read(fname):
        content_array = []
        with open(fname) as f:
                for line in f:
                        content_array.append(line)
                return content_array

def write_to_log(sent_message, author):
  f = open("chat_log.txt", "a")
  entry = "{}::".format(author) + sent_message + "\n"
  f.write(entry)
  f.close()

bot_response_q = file_read('bot_question_responses')
bot_response_r = file_read('bot_response_requests')
bot_response_d = file_read('bot_dm_responses')

question_words = ["who","what","when","where","how", "?"]
request_words = ["can", "will"]
emotional_words = ["sad", "angry", "happy", "upset", "depressed"]

def decide_response(message):
  q_count = 0
  r_count = 0
  e_count = 0
  for word in message.split(" "):
    if word.lower() in emotional_words:
        e_count = e_count + 1
  if message[0:6].lower() == "motoko":
    for word in message.split(" "):
      if word.lower() in question_words:
        q_count = q_count + 1
      elif word.lower() in emotional_words:
        e_count = e_count +1
  if q_count > 0:
        num = randint(0, (len(bot_response_q) - 1))
        return bot_response_q[num]
  elif r_count > 0:
        num = randint(0, (len(bot_response_r) - 1))
        return bot_response_r[num]
  elif e_count > 0:
        num = randint(0, (len(bot_response_d) - 1))
        return bot_response_d[num] + ";)"
  else:
    return ""

@client.event
async def on_ready():
  print("Motoko has activated.")

@client.event
async def on_disconnect():
  chat_log = pd.read_csv("chat_log.txt", delimiter="::")
  chat_log.to_csv("chat_log.csv")

  await client.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("Conversation Analysis"))

@client.event
async def on_member_join(member):
  print(f'{member} has joined the  server!')

@client.event
async def on_member_remove(member):
  print(f'{member} has been booted from the server!')

@client.event
async def on_message(message):

  if message.author == client.user:
    return

  if message.content == "Introduce yourself, Motoko.":
     await message.channel.send("Hello everyone! My name is Motoko :) I'm super excited to get to know you all! If you wish to speak with me, please start your message with \"Motoko\" and use a question word!")

  sentence = message.content
  author = message.author
  write_to_log(sentence, author)
  response = decide_response(sentence)

  if response == "":
    return
  elif ';)' in response:
    await message.author.send(response)
  else:
    await message.channel.send(response)

client.run(os.getenv("TOKEN"))


