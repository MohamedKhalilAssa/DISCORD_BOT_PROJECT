import discord
from discord.ext import commands
from dotenv import load_dotenv
import os 


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

#Handling errors:
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
        await ctx.send("An unexpected error occurred. Please contact an admin.")

#Anti spam :

#Spam settings :
message_limits = 5 #maximum messages allowed in the time window
time_window  = 10 #10 secondes
mute_duration = 600 # mute for 10 minutes

def setup(bot):
    bot.add_command(unban)
    