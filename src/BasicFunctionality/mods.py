import discord
from discord.ext import commands
from collections import defaultdict, deque
import time

GEMINI_API_TOKEN = os.getenv("GEMINI_API_TOKEN")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

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
async def spam_detection(message):
    if message.author.bot: #ignore bot messages
        return
    user_id = message.author.id
    current_time = time.time()

    #add the message timpestamp to the user's time wondow
    user_messages[user_id].append(current_time)
    
    #Remove timestamp older than the time window
    while user_messages [user_id] and user_messages[user_id][0] - current_time > time_window :
        user_messages[user_id].popleft()

    #check if the user exceeds the message limit
    if len(user_messages[user_id]) > message_limit:
        await message.channel.send(f"{message.author.mention}, you are a spamming! Please slow down and chill.")

        #Delete the message and mute the spammer
        await message.delete()
        await mute(ctx = message , member = message.author.mention, duration = mute_duration, reason = "Spamming messages" ) #calling the mute command


# ban bad/racist words :
# Configuration
WARN_THRESHOLD = 3   # Warnings before mute
MUTE_DURATION = 300    # Duration of mute in secondes
BANNED_WORDS = [
    # General Profanity
    "fuck", "bitch", "damn", "bastard", "asshole",
    "cunt", "piss", "prick", "slut", "whore",

    # Racist and Discriminatory Words
    "nigger", "negro", "chink", "spic", "cracker", "wetback",
    "gook", "kike", "honkey", "beaner", "redskin",

    

    # Hate Speech and Religious Intolerance
    "terrorist", "nazi", "hitler", "isis",

    # Sexually Explicit and Inappropriate Words
    "rape", "rapist", "molest", "pedophile", "childporn",
    "porn", "incest", "bestiality",

    # Slang and Offensive Phrases
    "kill yourself", "kms", "kys", "die in a fire", "go to hell"
]


# Dictionary to track warnings
user_warnings = defaultdict(int)


async def ban_words(message):
    if message.author.bot:
        return

    # Check if the message contains a banned word
    if any(banned_word in message.content.lower() for banned_word in BANNED_WORDS):
        # Delete the offensive message
        await message.delete()

        # Increase the user's warning count
        user_id = message.author.id
        user_warnings[user_id] += 1

        # Notify the channel and user
        await message.channel.send(
            f"🚨 {message.author.mention}, your message contained prohibited language and has been deleted."
        )
        # Check if the user has reached the warning threshold
        if user_warnings[user_id] >= WARN_THRESHOLD:
            await mute(message, member = message.author.mention, duration = MUTE_DURATION, reason = "Offensive words")
            await message.channel.send(
                f"🔇 {message.author.mention} has been muted for {MUTE_DURATION} secondes due to repeated violations."
            )
            # Reset user's warnings after mute
            user_warnings[user_id] = 0
        else:
            warnings_left = WARN_THRESHOLD - user_warnings[user_id]
            await message.channel.send(
                f"⚠️ {message.author.mention}, this is warning {user_warnings[user_id]} of {WARN_THRESHOLD}. "
                f"You will be muted if you receive {warnings_left} more warnings."
            )   
#Auto reply :
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



def setup(bot):
    bot.add_command(unban)
    bot.add_command(mute)
    bot.add_command(purge)
    
