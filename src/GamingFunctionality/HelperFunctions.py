import json 
from GamingFunctionality.scraping_prompting_functions import create_or_update_deals_json, CHANNELS_FILE_LOC
import asyncio

def InsertChannelID(message): 
    data = []
    try:
        with open(CHANNELS_FILE_LOC, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"channels": []}

    if message.channel.id not in data["channels"]:
        data["channels"].append(message.channel.id)
        with open(CHANNELS_FILE_LOC, "w") as f:
            json.dump(data, f, indent=4)
            print(f"From {__name__}: dailyMessageChannels.json updated with new data")
        return True
    
    return False

#@returns codes for better response to the User (0- operation not Done 1-Done .2- not Subscribed)
def deleteChannelID(message):
    try:
        with open(CHANNELS_FILE_LOC, "r") as f:
            data = json.load(f)
            print(data)
        if message.channel.id not in data.get("channels", []):
            return 2

        data["channels"] = list(filter(lambda x: x != message.channel.id, data.get("channels", [])))

        with open(CHANNELS_FILE_LOC, "w") as f:
            json.dump(data, f, indent=4)
            print(f"From {__name__}: dailyMessageChannels.json updated with new data")
            return 1
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"From {__name__}: Couldn't find/read the dailyMessageChannels.json. Creating new one...")
        data = {"channels": []}
        with open(CHANNELS_FILE_LOC, "w") as f:
            json.dump(data, f, indent=4)
            print(f"From {__name__}: Empty dailyMessageChannels.json created ")
        return 2
    except Exception as e:
        print(f"From {__name__}: Error during DeleteChannelId function: {e}")
        return 0

def check_if_ID_Still_Present(message) :
    data = []
    try:
        with open(CHANNELS_FILE_LOC, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"From {__name__}: Error during checking for id in dailyMessageChannels.json ")
        return False 
    if message.channel.id in data["channels"] :
        return True
    else: 
        return False

    
def logging(message):
    try :
        with open("src/GamingFunctionality/logs.txt", "a") as f:
            log_entry = f'@{message.author} - `{message.content}\n'
            f.write(log_entry)
    except Exception as e:
        print("Error during logging: ", e)


# function that uses the deals.json to send the deals to the discord channel
async def send_deals(discord, message,colors):
    deals = create_or_update_deals_json()
    for index, deal in enumerate(deals):
        embed = discord.Embed(
            title=deal["name"],
            url=deal["link"],
            color=colors[index % len(colors)]
        )
        embed.add_field(name="Old Price", value=f"{deal["old_value"]}", inline=False)
        embed.add_field(name="New Price", value=f"{deal["deal_value"]}", inline=False)
        embed.set_image(url=deal["image"])
        await message.channel.send(embed=embed)
    await message.channel.send("Done!")


# use of async to be non-blocking
async def sendDailyDeals (discord, message,colors): 
    while(True) :
        if(check_if_ID_Still_Present(message)): 
            await send_deals(discord, message,colors)
            await asyncio.sleep(60 * 60 * 24) # once per day
        else :
            break
    