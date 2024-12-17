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