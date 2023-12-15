import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata
import asyncio

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = commands.Bot(command_prefix="!", intents=intents)
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == client.user:
        return

    if channel == "random":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called llene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))

    elif channel == "ec2-info":
        if user_message.lower() == "!ec2info":
            await get_ec2_info(message)

async def get_ec2_info(message):
    try:
        ip_address = ec2_metadata.public_ipv4
        region = ec2_metadata.region
        instance_id = ec2_metadata.instance_id

        response = f"EC2 Information:\nIP Address: {ip_address}\nRegion: {region}\nInstance ID: {instance_id}"
        await message.channel.send(response)
    except Exception as e:
        print(f"Error retrieving EC2 information: {str(e)}")
        await message.channel.send("An error occurred while retrieving EC2 information. Please try again later.")

client.run(token)

