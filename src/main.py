import discord
from dotenv import load_dotenv
from discord.ext import commands
from BasicFunctionality.mods import setup
from GamingFunctionality.HelperFunctions import InsertChannelID, logging, send_deals, sendDailyDeals, deleteChannelID
import os
from GamingFunctionality.scraping_prompting_functions import finalizing_recommendations


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


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    #MOHAMED's PART :  
    #/help command
    if message.content.startswith('/help'):
        embed = discord.Embed(title="Help", 
                              description="Available commands:", color=discord.Color.random())
        embed.add_field(name="/help", value="Displays this help message.", inline=False)
        embed.add_field(name="/buy <product> <budget>", value="Sends recommendations for a product.", inline=False)
        embed.add_field(name="/deals", value="Sends deals for games.", inline=False)
        embed.add_field(name="/dailyDeals", value="Sends deals daily for games.", inline=False)
        embed.add_field(name="/stopDailyDeals", value="Stops Sending daily deals for games.", inline=False)
        await message.channel.send(embed=embed)
     
    # /buy command
    if message.content.startswith('/buy'):
        message_content = message.content.split(' ')[1:]
        if(len(message_content) != 2 or message_content[0].isalnum() == False or  message_content[1].isnumeric() == False):
            await message.channel.send('Invalid Input (ex: /buy PS5 1000)')
            return
        code , recomms = finalizing_recommendations(message_content[0],int(message_content[1]))
        if code == -1:
            await message.channel.send('Only Tech/Gaming related recommendations are allowed')
            return
        logging(message)
        for index, recomm in enumerate(recomms):
            embed = discord.Embed(
                title=f"Recommendation #{index + 1}",
                description=recomm["desc"],
                color=colors[index % len(colors)]  
            )
            embed.add_field(name="Product Name", value=recomm["name"], inline=False)
            embed.add_field(name="Price", value=f"${recomm["actual_price"]}", inline=False)
            embed.add_field(name="Links", value="\n".join([f"- {link}" for link in recomm["links"]]), inline=False)
            await message.channel.send(embed=embed)
        await message.channel.send('Recommendations have been sent successfully!')

    #/deals       
    if message.content.startswith('/deals'):
        await send_deals(discord,message,colors)

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
    
setup(bot)

    #/dailyDeals
    if message.content.startswith('/dailyDeals'):
       
        if(InsertChannelID(message)) : 
            await message.channel.send("This channel is now set to receive daily deals, starting from now.")
            await sendDailyDeals(discord,message,colors)
        else:
            await message.channel.send("This channel is already set to receive daily deals.")
    
    # /stopDailyDeals
    if message.content.startswith('/stopDailyDeals'):
        code = deleteChannelID(message)
        if(code == 1): 
            await message.channel.send("This channel won't receive new updates.")
        elif(code == 2):
            await message.channel.send("You already aren't subscribed")
        else :
            await message.channel.send("An Error Occured. Please Try again.")
    
    #MEHDI's PART 



if __name__ == "__main__":
    try: 
        bot.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print("Error during the running of the bot process: ",e)