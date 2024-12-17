import discord
from dotenv import load_dotenv
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

    if message.content.startswith('/buy'):
        message_content = message.content.split(' ')[1:]
        print(len(message_content))
        if(len(message_content) != 2 or message_content[0].isalnum() == False or  message_content[1].isnumeric() == False):
            await message.channel.send('Invalid Input (ex: /buy PS5 1000)')
            return
        code , recomms = finalizing_recommendations(message_content[0],int(message_content[1]))
        if code == -1:
            await message.channel.send('Only Tech/Gaming related recommendations are allowed')
            return
        for index, recomm in enumerate(recomms):
            links = "\n".join(recomm["links"])  
            await message.channel.send(
                f"""
                ---------------------------------------
                **Recommendation Number** : {index + 1}
                **Product's Name** : {recomm["name"]}
                **Product's Price** : {recomm["actual_price"]}
                **Product's Description** : {recomm["desc"]}
                **Product's Links** :
                {links}
                """
            )
        
        await message.channel.send('Done')


if __name__ == "__main__":
    try: 
        client.run(os.getenv('DISCORD_TOKEN'))
    except Exception as e:
        print("Error during the running of the bot process: ",e)