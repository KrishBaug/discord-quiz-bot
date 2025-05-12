import random
import asyncio
import discord
from dataHandling import return_no_of_questions, required_set_of_questions
from dataHandling import update_or_create_json_file, creat_tracking_file, get_question
from dataHandling import update_question_no
from discordBotsCommands import QuestionView,TimerButton, send_question_embed
from discord.ui import View

def choose_question_index(no_of_questions: int) -> list:
    total_qustions = return_no_of_questions()
    question_choose = True
    no_of_question_chosen = 0
    index_of_questions = []
    question_is_repeated = False
    while no_of_question_chosen < no_of_questions:
        question_is_repeated = False
        question_index = random.randint(0, int(total_qustions) - 1)
        if index_of_questions != []:
            for i in index_of_questions:
                if i == question_index:
                    question_is_repeated = True

        if not question_is_repeated:
            index_of_questions.append(question_index)
            no_of_question_chosen = no_of_question_chosen + 1

    return index_of_questions 


def default_alg_choose_question(id: str) -> list:
    question_index=choose_question_index(no_of_questions:=10)
    quiz_questions = required_set_of_questions(question_index)
    update_or_create_json_file(quiz_questions, id)

    return question_index

async def send_response(chanel_id: str, interaction: discord.Interaction, channel):
    timer_view = View()
    timer_button = TimerButton(timeout=10)
    timer_view.add_item(timer_button)
    timer_message = await channel.send(view=timer_view) 
    # Start the countdown in the background
    optionView = QuestionView(str(interaction.channel_id), timer_button)
    embed = send_question_embed(interaction.channel_id)
    
    await channel.send(embed=embed, view=optionView)
    await timer_button.start_timer(timer_message, unique_code=str(interaction.channel_id))
    
    await asyncio.sleep(1)
 

#send to specific channel not user interaction next work
async def run_quiz(channel_id:str, interaction: discord.Interaction):
    q= default_alg_choose_question(str(interaction.channel_id))
    c = interaction.user
    creat_tracking_file(c.id, c.name, interaction.guild_id, interaction.channel_id, q )
    q, current_question_no, total_qustions = get_question(str(channel_id))
    channel = interaction.guild.get_channel(int(channel_id))
    while current_question_no < total_qustions:
        q, current_question_no, total_qustions = get_question(str(channel_id))
        await send_response(channel_id, interaction, channel)
        update_question_no(str(channel_id))
    
    
    
    
    
    
 
