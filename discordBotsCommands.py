from discord.ui import View, Button
from discord import Embed
from discord import ButtonStyle as color
import discord
from dataHandling import get_options, get_question, handle_button_click,reset_ans_state 
import asyncio


async def on_click_response(interaction: discord.Interaction, option:str, option_no: str, ans: str, button: Button, time):
    print(option.lower(), ans.lower())
    time.button_clicked()
    answer_state = bool
    if option.lower() == ans.lower():
        button.style = color.success
        button.label = f" ✔ {option}"
        answer_state = True

    else:
        button.style =color.danger
        button.label= f" ✖ {option}"
        print(ans.lower())
        print(OptionButtonA.label)
        answer_state = False
        

        for items in button.view.children:
            if items.option.lower() == ans.lower():
                items.style = color.success
                items.label = f" ✔ {items.option}"
    

    if handle_button_click(unique_code=str(interaction.channel_id), user_id=str(interaction.user.id),
                           user_name=interaction.user.name, answer_state=answer_state):
        await interaction.response.defer()
        return
    else:
        pass
    for item in button.view.children:
        if item.option.lower() != option.lower():
            if item.option.lower() != ans.lower():
                button.view.remove_item(item)


    for items in button.view.children:
        items.disabled = True
    await interaction.response.send_message(f"✅ Correct!" if option.lower() == ans.lower() else "❌ Wrong!", ephemeral=True, view=button.view)


class TimerButton(Button):
    """A disabled button acting as a timer display."""
    def __init__(self, timeout: int):
        super().__init__(label=f"Remaining Time: ⏳ {timeout}", style=discord.ButtonStyle.gray, disabled=True)
        self.timeout = timeout
        self.timer_running = True
        self.button_clicked_ = False

    async def start_timer(self, message, unique_code:str):
        """Updates the timer button every second."""
        while self.timeout > 0 and not self.button_clicked_:
            self.label = f"Remaining Time: ⏳ {self.timeout}"
            await message.edit(view=self.view)
            self.timeout -= 1
            await asyncio.sleep(1)

        if self.button_clicked_:
            while self.timeout > 0:
                self.label = f"Next Question in : ⏳{self.timeout}"
                await message.edit(view=self.view)
                self.timeout -= 1
                await asyncio.sleep(1)

        # When time is up, update the button label
        if not self.button_clicked_:
            self.label = "⏳ Time's Up!, Get Ready for the Next Question"
            await message.edit(view=self.view)

        if self.button_clicked_:
            self.label = "Get Ready for Next Question"
            await message.edit(view=self.view)

        reset_ans_state(unique_code=str(unique_code))

    def stop_timer(self):
        self.timer_running=False

    def button_clicked(self):
        self.button_clicked_ = True


class OptionButtonA(Button):
    def __init__(self, option: str, ans: str):
        super().__init__(label=option, style=color.blurple)
        self.option = option
        self.ans = ans
                


class OptionButtonB(Button):
    def __init__(self, option: str, ans: str):
        super().__init__(label=option, style=color.blurple)
        self.option = option
        self.ans = ans
                


class OptionButtonC(Button):
    def __init__(self, option: str, ans: str):
        super().__init__(label=option, style=color.blurple)
        self.option = option
        self.ans = ans
                


class OptionButtonD(Button):
    def __init__(self, option: str, ans: str):
        super().__init__(label=option, style=color.blurple)
        self.option = option
        self.ans = ans
                



class QuestionView(View):
    def __init__(self,unique_code: str, timer_button: TimerButton):
        super().__init__()
        options_list = get_options(unique_code)
        correct_answer = options_list[4]

        option_a = OptionButtonA(options_list[0], correct_answer)
        option_b = OptionButtonB(options_list[1], correct_answer)
        option_c = OptionButtonC(options_list[2], correct_answer)
        option_d = OptionButtonD(options_list[3], correct_answer)

        # ✅ Pass the running timer instance to stop it on click
        option_a.callback = lambda interaction: on_click_response(interaction, option_a.option, "A", option_a.ans, option_a, timer_button)
        option_b.callback = lambda interaction: on_click_response(interaction, option_b.option, "B", option_b.ans, option_b, timer_button)
        option_c.callback = lambda interaction: on_click_response(interaction, option_c.option, "C", option_c.ans, option_c, timer_button)
        option_d.callback = lambda interaction: on_click_response(interaction, option_d.option, "D", option_d.ans, option_d, timer_button)

        self.add_item(option_a)
        self.add_item(option_b)
        self.add_item(option_c)
        self.add_item(option_d)

def send_question_embed(unique_code:str):
    question, question_no, t = get_question(str(unique_code))    
    embed = discord.Embed(title=f"Question : {question_no}",description=f'**{question}**' ,color=discord.Color.blue())
    return embed

    

