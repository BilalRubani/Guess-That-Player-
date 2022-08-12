# GuessThatPlayerBot.py

import discord
from discord.ext import commands
from datetime import datetime
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from random import choice, shuffle


TOKEN = 'Unique Discord Bot Token'
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)


PLAYER_DICT = players.get_active_players()


def generate_choices(player_of_the_day):
    '''Generates random answer options for the user to choose from.'''
    answer_choices = []
    answer_choices.append(player_of_the_day['full_name'])
    for _ in range(3):
        option = choice(PLAYER_DICT)
        if option != player_of_the_day:
            answer_choices.append(option['full_name'])
    shuffle(answer_choices)
    return answer_choices


def called_once_a_day():
    '''
    Serves as the primary location for most of the program; the bot is
    activated once a specific time is reached, and the bot will reenter
    this "asleep" state once all actions are taken care of.
    '''
    print("bot is asleep")
    while True:
        current_time = datetime.now().strftime("%H:%M") # Military Time am:pm
        if current_time == "00:00": # 12:00 am PST
            print("bot is now activated")
            break

called_once_a_day()


@client.event
async def on_ready():
    '''
    All actions of the bot take place in this function. The bot gathers
    all necessary information, including generating the random player
    of the day, as well as all of that player's information, including
    their draft information as well as that player's statistics. The
    bot sends all this information to each user, and the bot will re-
    enter the asleep state once all actions have been completed.
    '''
    print(f'{client.user} has connected to Discord!')
    player_of_the_day = choice(PLAYER_DICT)
    correct_name = player_of_the_day['full_name']
    current_id = player_of_the_day['id']

    successful = False
    while not successful:
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id = current_id)
        
            draft_year = player_info.get_data_frames()[0]['DRAFT_YEAR'][0]
            draft_round = player_info.get_data_frames()[0]['DRAFT_ROUND'][0]
            draft_number = player_info.get_data_frames()[0]['DRAFT_NUMBER'][0]
            points_per_game = player_info.get_data_frames()[1]['PTS'][0]
            assists_per_game = player_info.get_data_frames()[1]['AST'][0]
            rebounds_per_game = player_info.get_data_frames()[1]['REB'][0]
            current_timeframe = player_info.get_data_frames()[1]['TimeFrame'][0]
            
            successful = True
        except:
            pass
    
    
    answer_choices = generate_choices(player_of_the_day)
    
    for guild in client.guilds:
        print(guild)
        for member in guild.members:
            if (member.id != 'Insert Bot Member ID') and not member.bot:
                await member.send('**Guess That Player!**')
                await member.send('**-----------------------**')
                await member.send(f'**DRAFT INFORMATION:**\nRound #: {draft_round}\nPick #: {draft_number}\nYear Drafted: {draft_year}')
                await member.send(f'**STATS ({current_timeframe}):**\nPPG: {points_per_game}\nAPG: {assists_per_game}\nRPG: {rebounds_per_game}\n')
                await member.send(f'A) {answer_choices[0]}\nB) {answer_choices[1]}\nC) {answer_choices[2]}\nD) {answer_choices[3]}')
                await member.send("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                await member.send(f'The Correct Answer is... (DON\'T CHEAT!!!): ||**{correct_name}**||')
                await member.send("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    current_time = datetime.now().strftime("%H:%M")
    while current_time == "00:00":
        current_time = datetime.now().strftime("%H:%M")
    else:
        called_once_a_day()
        

client.run(TOKEN)
