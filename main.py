import discord
from discord.ext import commands
import time
import asyncio
import os
from dotenv import load_dotenv
from botBackend import run_quiz
from integrateGPT import askGPT, askDoubt

load_dotenv()


class QuizBot(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user} !')
        try:
            guild = discord.Object(id=1342087352432066644)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')

        except Exception as e:
            print(f'Error syncing command {e}')


    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')

intents = discord.Intents.default()
intents.message_content = True
quizBot = QuizBot(command_prefix='!', intents=intents)
GUILD_ID =discord.Object(id=1342087352432066644)

@quizBot.tree.command(name='sq', description='Start a quiz competion', guild=GUILD_ID)
async def startQuiz(interaction: discord.Interaction):
    await interaction.response.send_message("Starting a quiz competition !")
    await asyncio.create_task(run_quiz(interaction.channel_id, interaction))

@quizBot.tree.command(name="ask", description='Ask question and interact with chatGPT-AI', guild=GUILD_ID)
async def ask_doubt(interaction: discord.Interaction, prompt:str):
    await interaction.response.defer(thinking=True)
    response = askGPT(prompt)

    await interaction.followup.send(response)
    
@quizBot.tree.command(name="askdt", description='Ask doubt about the questions from chatGPT-AI', guild=GUILD_ID)
async def askdoubt(interaction: discord.Interaction, prompt:str):
    await interaction.response.defer(thinking=True)
    response = askDoubt(prompt, interaction.channel_id) 

    await interaction.followup.send(response)
 
quizBot.run(str(os.getenv('API_KEY')))
