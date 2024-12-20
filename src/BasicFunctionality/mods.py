import discord
from discord.ext import commands
from collections import defaultdict, deque
import time
from BasicFunctionality.prompt import contain_bad_words
import json
from datetime import datetime, timedelta
#command : unban a previous banned member

@commands.command(name="unban")
@commands.has_permissions(ban_members = True)

async def unban(ctx, *, username):
    banned_users = await ctx.guild.bans() # Fetch tha list of banned users
    for banned in banned_users:
        user = banned.user
        if username == user.name:
            await ctx.guild.unban(user) # unban the user
            await ctx.send(f"{user} has been unbanned.")
    await ctx.send("User not found in the ban list.")

@commands.command(name="mute")
@commands.has_permissions(moderate_members = True)
async def mute(message, member: discord.Member, duration : int, *, reason=None):

    # Calculate the end time for the timeout
    end_time = datetime.now().astimezone()  + timedelta(seconds=duration)
    # Apply the timeout
    try:
        await member.timeout(end_time, reason=reason)
        await message.channel.send(f"{member.mention} has been muted for {duration // 60} minutes.")
    except Exception as e:
        await message.channel.send(f"Failed to mute {member.mention}. Error: {e}")

@commands.command(name="unmute")
@commands.has_permissions(moderate_members = True)
async def unmute(message, member: discord.Member):
    # Apply the timeout
    try:
        await member.timeout(datetime.now().astimezone() - timedelta(days=1))
        await message.channel.send(f"{member.mention} has been unmuted.")
    except Exception as e:
        await message.channel.send(f"Failed to unmute {member.mention}. Error: {e}")
#command : delete a specified numer of messages from a channel

@commands.command(name="purge")
@commands.has_permissions(manage_messages = True)

async def purge(ctx, amount=10):
    await ctx.channel.purge(limit = amount + 1) #delelte the messages includes the command itself
    await ctx.send(f"Deleted {amount} messages", delete_after = 3)

import json

WARN_THRESHOLD1 = 3   # Warnings before mute
MUTE_DURATION1 = 300  # Duration of mute in seconds
user_warning_path = "src/BasicFunctionality/user_warnings.json"

async def ban_words(message):
    """
    Handles messages containing banned words.
    """
    if message.author.bot:
        return

    # Check if the message contains a banned word
    if await contain_bad_words(message.content):
        print("Message contains a banned word")
        
        # Delete the offensive message
        await message.delete()

        user_id = str(message.author.id)  

        try:
            with open(user_warning_path, "r") as f:
                user_warnings = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            user_warnings = {}

        user_warnings[user_id] = user_warnings.get(user_id, 0) + 1

        try:
            with open(user_warning_path, "w") as f:
                json.dump(user_warnings, f, indent=4)
        except Exception as e:
            print(f"Error saving user warnings: {e}")
            return

        await message.channel.send(
            f"🚨 {message.author.mention}, your message contained prohibited language and has been deleted."
        )

        # Check if the user has reached the warning threshold
        if user_warnings[user_id] >= WARN_THRESHOLD1:
            # Mute the user
            await mute(message, member=message.author, duration=MUTE_DURATION1,reason="Offensive words")

            await message.channel.send(
                f"🔇 {message.author.mention} has been muted for {MUTE_DURATION1} seconds due to repeated violations."
            )

            # Reset the user's warnings after mute
            user_warnings[user_id] = 0
            try:
                with open(user_warning_path, "w") as f:
                    json.dump(user_warnings, f, indent=4)
            except Exception as e:
                print(f"Error saving user warnings after reset: {e}")
        else:
            warnings_left = WARN_THRESHOLD1 - user_warnings[user_id]
            await message.channel.send(
                f"⚠ {message.author.mention}, this is warning {user_warnings[user_id]} of {WARN_THRESHOLD1}. "
                f"You will be muted if you receive {warnings_left} more warnings."
            )

SPAM_THRESHOLD = 5   # Messages allowed in time window
TIME_WINDOW = 10     # Time window in seconds
MUTE_DURATION = 600  # Mute duration in seconds
user_messages_path = "src/BasicFunctionality/user_messages.json"

async def anti_spam(message):
    """
    Anti-spam function to detect and mute spamming users.
    """
    if message.author.bot:
        return

    user_id = str(message.author.id)  # Convert user ID to string for JSON compatibility
    current_time = time.time()

    # Load user message timestamps from the file
    try:
        with open(user_messages_path, "r") as f:
            user_messages = json.load(f)
            # Convert lists to deque for efficient processing
            user_messages = {k: deque(v) for k, v in user_messages.items()}
    except (FileNotFoundError, json.JSONDecodeError):
        user_messages = {}

    # Initialize deque for the user if not present
    if user_id not in user_messages:
        user_messages[user_id] = deque()

    # Add the current message timestamp
    user_messages[user_id].append(current_time)

    # Remove timestamps older than the time window
    while user_messages[user_id] and current_time - user_messages[user_id][0] > TIME_WINDOW:
        user_messages[user_id].popleft()

    # Save the updated user messages back to the file
    try:
        with open(user_messages_path, "w") as f:
            # Convert deques to lists for JSON serialization
            json.dump({k: list(v) for k, v in user_messages.items()}, f, indent=4)
    except Exception as e:
        print(f"Error saving user messages: {e}")
        return

    # Check if the user exceeds the spam threshold
    if len(user_messages[user_id]) > SPAM_THRESHOLD:
        await message.channel.send(f"🚨 {message.author.mention}, you are spamming! Please slow down.")
        await message.delete()

        # Mute the user
        await mute(
            message,
            member=message.author,
            duration=MUTE_DURATION,
            reason="Spamming messages"
        )
        await message.channel.send(
            f"🔇 {message.author.mention} has been muted for {MUTE_DURATION // 60} minutes due to spamming."
        )
def setup(bot):
    bot.add_command(unban)
    bot.add_command(mute)
    bot.add_command(unmute)
    bot.add_command(purge)
    
