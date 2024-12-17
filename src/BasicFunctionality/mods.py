import discord
from discord.ext import commands
from dotenv import load_dotenv
import os 

#set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

#Define the command prefix 

bot = commands.Bot(command_prefix = '!', intents = intents)

@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")

bot.run(os.getenv("DISCORD_TOKEN"))


#command : Kick a member 

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member,*,reason = None):
    
    '''
    kicks a member from the server
    the member to kick : member
    reason = reason

    '''
    await member.kick(reason = reason) #kick the member
    await ctx.send(f"{member.mention} has been kicked for {reason}") #confirm in chat

#command : ban

@bot.command()
@commands.has_permission(ban_members = True)

async def ban(ctx ,member: discord.Member ,* ,reason = None):
    await member.ban(reason = reason) #ban the member
    await ctx.send(f"{member.mention} has been banned for{reason}") #confirm in chat

#command : unban a previous banned member

@bot.command()
@commands.has_permission(ban_members = True)

async def unban(ctx, *, username):
    banned_users = await ctx.guild.bans() # Fetch tha list of banned users
    for banned in banned_users:
        user = banned.user
        if username == user.name:
            await ctx.guild.unban(user) # unban the user
            await ctx.send(f"{user} has been unbanned.")
    await ctx.send("User not found in the ban list.")

@bot.command()
@commands.has_permission(moderate_members = True)

async def mute(ctx, member: discord.Member, duration, *, reason = None):
    time = discord.utils.utcnow() + discord.timedelta(duration)
    await member.timeout(utili = time, reason = reason) # Apply timeout
    await ctx.send(f"{member.mention}has been muted for{duration} minutes.")

#command : delete a specified numer of messages from a channel

@bot.command()
@commands.has_permission(manage_messages = True)

async def purge(ctx, amount):
    await ctx.channel.urge(limit = amount + 1) #delelte the messages includes the command itself
    await ctx.send(f"Deleted {amount} messages", delete_after = 3)

#handling permission errors

@bot.event
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermission): #if the error(exception object) is in the exception class commands.MissingPermission
        await ctx.send("You don't have permission to use this command")

#Anti spam :

#Spam settings :
message_limits = 5 #maximum messages allowed in the time window
time_window  = 10 #10 secondes
mute_duration = 600 # mute for 10 minutes
