import discord
from dotenv import load_dotenv
import json
import os
from GamingFunctionality.fetchingData import finalizing_recommendations, scrape_deals

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

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
        try :
          with open("src/GamingFunctionality/logs.txt", "a") as f:
                log_entry = f'@{message.author} asked for {message_content[0]} with a budget of ${message_content[1]}\n'
                f.write(log_entry)
        except Exception as e:
            print("Error during logging: ", e)
        
        colors = [discord.Color.blue(), discord.Color.green(), discord.Color.red(), discord.Color.purple(),discord.Color.teal()]

        for index, recomm in enumerate(recomms):
            embed = discord.Embed(
                title=f"Recommendation #{index + 1}",
                description=recomm["desc"],
                color=colors[index % len(colors)]  
            )
            embed.add_field(name="Product Name", value=recomm["name"], inline=False)
            embed.add_field(name="Price", value=recomm["actual_price"], inline=False)
            embed.add_field(name="Links", value="\n".join([f"- {link}" for link in recomm["links"]]), inline=False)
            await message.channel.send(embed=embed)
        await message.channel.send('Recommendations have been sent successfully!')


if __name__ == "__main__":
    try: 
        client.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print("Error during the running of the bot process: ",e)