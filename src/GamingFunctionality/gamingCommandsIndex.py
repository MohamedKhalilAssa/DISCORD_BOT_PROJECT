import discord
from discord.ext import commands
from GamingFunctionality.HelperFunctions import (
    InsertChannelID,
    logging,
    send_deals,
    sendDailyDeals,
    deleteChannelID,
)
from GamingFunctionality.scraping_prompting_functions import finalizing_recommendations

colors = [
    discord.Color.blue(),
    discord.Color.green(),
    discord.Color.red(),
    discord.Color.purple(),
    discord.Color.teal(),
]



# Command: Buy
@commands.command(name='buy', help='Sends recommendations for a product')
async def buy(ctx):
    message_content = ctx.message.content.split(' ')[1:]
    if (
        len(message_content) != 2
        or not message_content[0].isalnum()
        or not message_content[1].isnumeric()
    ):
        await ctx.send('Invalid Input (ex: /buy PS5 1000)')
        return

    code, recomms = finalizing_recommendations(message_content[0], int(message_content[1]))
    if code == -1:
        await ctx.send('Only Tech/Gaming related recommendations are allowed')
        return

    logging(ctx.message)
    for index, recomm in enumerate(recomms):
        embed = discord.Embed(
            title=f"Recommendation #{index + 1}",
            description=recomm["desc"],
            color=colors[index % len(colors)],
        )
        embed.add_field(name="Product Name", value=recomm["name"], inline=False)
        embed.add_field(name="Price", value=f"${recomm['actual_price']}", inline=False)
        embed.add_field(
            name="Links",
            value="\n".join([f"- {link}" for link in recomm["links"]]),
            inline=False,
        )
        await ctx.send(embed=embed)
    await ctx.send('Recommendations have been sent successfully!')


# Command: Deals
@commands.command(name='deals', help='Sends deals for games')
async def deals(ctx):
    await send_deals(discord, ctx, colors)


# Command: Daily Deals
@commands.command(name='dailyDeals', help='Sends deals daily for games')
async def dailyDeals(ctx):
    if InsertChannelID(ctx.message):
        await ctx.send(
            "This channel is now set to receive daily deals, starting from now."
        )
        await sendDailyDeals(discord, ctx, colors)
    else:
        await ctx.send("This channel is already set to receive daily deals.")


# Command: Stop Daily Deals
@commands.command(
    name='stopDailyDeals', help='Stops Sending daily deals for games'
)
async def stopDailyDeals(ctx):
    code = deleteChannelID(ctx.message)
    if code == 1:
        await ctx.send("This channel won't receive new updates.")
    elif code == 2:
        await ctx.send("You already aren't subscribed.")
    else:
        await ctx.send("An error occurred. Please try again.")

@commands.command(name='help', help='Displays a list of available commands')
async def info(ctx):
    embed = discord.Embed(
        title="Help",
        description="Available commands:",
        color=discord.Color.random(),
    )
    embed.add_field(name="/help", value="Displays this help message.", inline=False)
    embed.add_field(
        name="/buy <product> <budget>",
        value="Sends recommendations for a product.",
        inline=False,
    )
    embed.add_field(name="/deals", value="Sends deals for games.", inline=False)
    embed.add_field(
        name="/dailyDeals", value="Sends deals daily for games.", inline=False
    )
    embed.add_field(
        name="/stopDailyDeals",
        value="Stops Sending daily deals for games.",
        inline=False,
    )
    embed.add_field(
        name="/stopDailyDeals",
        value="Stops Sending daily deals for games.",
        inline=False,
    )
    embed.add_field(
        name="/mute <username> <duration>", value="Mutes a user.", inline=False
    )
    
    embed.add_field(
        name="/unmute <username>", value="Unmutes a user.", inline=False
    )
    embed.add_field(
        name="/purge <amount>", value="Deletes Messages and purges them.", inline=False
    )
    
    await ctx.send(embed=embed)
# Function to register commands with the bot
def gamingSetup(bot):
    bot.add_command(buy)
    bot.add_command(deals)
    bot.add_command(dailyDeals)
    bot.add_command(info)
    bot.add_command(stopDailyDeals)
