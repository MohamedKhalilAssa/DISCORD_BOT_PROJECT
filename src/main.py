import discord
from dotenv import load_dotenv
from discord.ext import commands
from BasicFunctionality.mods import setup
import os
from GamingFunctionality.gamingCommandsIndex import gamingSetup
from BasicFunctionality.mods import ban_words, anti_spam


load_dotenv()

#custom functions 
# 
# must be called inside the on_message function
colors = [discord.Color.blue(), discord.Color.green(), discord.Color.red(), discord.Color.purple(),discord.Color.teal()]

# BOT SETUP
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Command: Help


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        bot.remove_command('help')
        setup(bot)
        gamingSetup(bot)
    except Exception as e:
        print(f"Error during on_ready: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await anti_spam(message)
    await ban_words(message)
    await bot.process_commands(message)
    

AUTO_REPLIES = {
    "hello": "Hi there!",
    "how are you": "I'm just a bot, but I'm doing great!",
    "discord bot": "That's me!"
}

@bot.event
async def auto_reply(message):
    for key, response in AUTO_REPLIES.items():
        if key in message.content.lower():
            await message.channel.send(response)
            break
    
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):  # Fixing the error type
        await ctx.send("You don't have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("A required argument is missing. Please check the command usage.")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Use /help or !help for a list of commands.")
    else:
        # Log the error for debugging purposes
        print(f"An error occurred: {error}")
        await ctx.send("An unexpected error occurred. Please contact an admin.")
    




if __name__ == "__main__":
    try: 
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print("Error during the running of the bot process: ",e)