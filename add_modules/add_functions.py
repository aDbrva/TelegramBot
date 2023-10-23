import os
from datetime import datetime, timedelta
import pytz
from aiogram import types

# def make_dictionary(FILENAME):
#     users = {}
#     with open(FILENAME) as file:
#         lines = file.read().splitlines()
#         for line in lines:
#             key,value = line.split(': ')
#             users[key] = int(value)
    
#     return users


def open_file(FILENAME):
    if(not os.path.exists(FILENAME)):
        file = open(FILENAME, "a")
        file.close() 
    # else:
    #     print(f'{FILENAME} already exist.')


def save_chat_id(message: types.Message, FILENAME_CHAT):
    with open (FILENAME_CHAT, 'r') as file:
        lines = file.read().splitlines()

    list_id = [int(item) for item in lines]
    if(not (message.chat.id in list_id)):
        with open(FILENAME_CHAT, "a") as file:
            file.write(f"{message.chat.id}\n")



def convert_time(message: types.Message, hours):
    curr_date = message.date.astimezone(pytz.utc)
    curr_date += timedelta(hours = hours)
    curr_date = datetime(curr_date.year, curr_date.month, 
                            curr_date.day)
    
    return curr_date