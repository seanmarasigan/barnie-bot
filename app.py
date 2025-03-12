from typing import Final
import os
from dotenv import load_dotenv

import discord
from discord import Intents, Client, Message, Embed, File

from responses import get_response
from database import log_message, init_db, get_conversations

# STEP 0: INITIATE TOKEN and DB
load_dotenv()
conn, cur = init_db()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client = Client(intents=intents)

# STEP 2: HELP FUNCTION
async def send_help(message: Message) -> None:
    embed = Embed(
        color=discord.Colour.purple(),
        title="Barnie Commands",
        description="Here are the commands you can use with this bot:"
    )

    
    help_text = (
        "\n\n"
        "1. `!b <your question>` - Ask Barnie a question and receive a response.\n"
        "2. `!help` - Display this help message.\n"
        "For further assistance, feel free to reach out!"
    )
    embed.add_field(name="Commands", value=help_text)
    await message.channel.send(embed=embed)

# STEP 3: B COMMAND FUNCTION
async def send_b_response(message: Message, question: str) -> None:
    try:
        username: str = str(message.author.display_name)
        id: str = str(message.author.id)
        conversation_hist = get_conversations(cur, id)
        response: str = get_response(question, conversation_hist)
        log_message(conn, cur, id, response, "model")
        if len(response) < 2000:
            await message.channel.send(f"{username}, {response}")
        else:
            f = open("file.txt", "w")
            f.write(response)
            f.close()
            await message.channel.send(f"{username}, \n", file=File("file.txt"))
    except Exception as e:
        print(e)

# STEP 4: MESSAGE FUNCTIONALITY
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    lowered: str = user_message.lower()

    # Check for help command
    if lowered.startswith('!help'):
        await send_help(message)
        return

    # Check for !b command
    if lowered.startswith('!b ') and message.channel.name == 'talk-with-barnie-bot':
        print("true")
        question = user_message[3:].strip()
        id: str = str(message.author.id)
        log_message(conn, cur, id, question, "user")
        await send_b_response(message, question)

# STEP 5: HANDLING THE STARTUP FOR OUR BOT
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

# STEP 6: HANDLING INCOMING MESSAGES
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username: str = str(message.author)
    id: str = str(message.author.id)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username} #{id}: "{user_message}"')
    if message.channel.name == 'talk-with-barnie-bot':
        
        await send_message(message, user_message)

# STEP 7: MAIN ENTRY POINT
def main() -> None:
    client.run(TOKEN)

if __name__ == '__main__':
    main()