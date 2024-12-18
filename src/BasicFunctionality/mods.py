import discord
from discord.ext import commands
from dotenv import load_dotenv
import os 
from collections import defaultdict, deque
import time

#command : Kick a member 

@commands.command()
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

@commands.command()
@commands.has_permissions(ban_members = True)

async def ban(ctx ,member: discord.Member ,* ,reason = None):
    await member.ban(reason = reason) #ban the member
    await ctx.send(f"{member.mention} has been banned for{reason}") #confirm in chat

#command : unban a previous banned member

@commands.command()
@commands.has_permissions(ban_members = True)

async def unban(ctx, *, username):
    banned_users = await ctx.guild.bans() # Fetch tha list of banned users
    for banned in banned_users:
        user = banned.user
        if username == user.name:
            await ctx.guild.unban(user) # unban the user
            await ctx.send(f"{user} has been unbanned.")
    await ctx.send("User not found in the ban list.")

@commands.command()
@commands.has_permissions(moderate_members = True)

async def mute(ctx, member: discord.Member, duration, *, reason = None):
    time = discord.utils.utcnow() + discord.timedelta(duration)
    await member.timeout(utili = time, reason = reason) # Apply timeout
    await ctx.send(f"{member.mention}has been muted for{duration} minutes.")

#command : delete a specified numer of messages from a channel

@commands.command()
@commands.has_permissions(manage_messages = True)

async def purge(ctx, amount):
    await ctx.channel.urge(limit = amount + 1) #delelte the messages includes the command itself
    await ctx.send(f"Deleted {amount} messages", delete_after = 3)



#Anti spam :

#Spam settings :
message_limit = 5 #maximum messages allowed in the time window
time_window  = 10 #10 secondes
mute_duration = 600 # mute for 10 minutes

#store user messages data
user_messages = defaultdict(deque)


#Event : activated when a message is sent
@bot.event
async def on_message(message):
    if message.author.bot: #ignore bot messages
        return
    user_id = message.author.id
    current_time = time.time()

    #add the message timpestamp to the user's time wondow
    user_message[user_id].append(current_time)
    
    #Remove timestamp older than the time window
    while user_messages [user_id] and user_messages[user_id][0] - current_time > time_window :
        user_messages[user_id].popleft()

    #check if the user exceeds the message limit
    if len(user_messages[user_id]) > message_limit:
        await message.channel.send(f"{message.author.mention}, you are a spamming! Please slow down and chill.")

        #Delete the message and mute the spammer
        await message.delete()
        









def setup(bot):
    bot.add_command(unban)
    bot.add_command(mute)
    bot.add_command(purge)
    
