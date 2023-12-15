import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata
import asyncio

# Load environment variables from a .env file
load_dotenv()

# Create Discord bot with custom intents to enable message content and messages events
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = commands.Bot(command_prefix="!", intents=intents)

# Retrieve Discord bot token from environment variable
token = os.getenv('TOKEN')

@client.event
async def on_ready():
    # Print a message when the bot is successfully connected to Discord
    print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
    # Extract information from the received message
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    # Log the message details to the console
    print(f'Message {user_message} by {username} on {channel}')

    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Check if the message is in the "random" channel
    if channel == "random":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            # Respond to greetings
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            # Respond to farewells
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            # Respond with a random joke
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called llene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))

    # Check if the message is in the "ec2-info" channel
    elif channel == "ec2-info":
        if user_message.lower() == "!ec2info":
            # Retrieve and send EC2 information
            await get_ec2_info(message)

async def get_ec2_info(message):
    try:
        # Retrieve EC2 metadata
        ip_address = ec2_metadata.public_ipv4
        region = ec2_metadata.region
        instance_id = ec2_metadata.instance_id

        # Compose and send the EC2 information response
        response = f"EC2 Information:\nIP Address: {ip_address}\nRegion: {region}\nInstance ID: {instance_id}"
        await message.channel.send(response)
    except Exception as e:
        # Log and inform about errors in retrieving EC2 information
        print(f"Error retrieving EC2 information: {str(e)}")
        await message.channel.send("An error occurred while retrieving EC2 information. Please try again later.")

# Run the Discord bot with the provided token
client.run(token)


