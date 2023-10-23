import os
import json
import random
from datetime import datetime, timedelta
from aiogram import types, Dispatcher
from pathlib import Path

# from add_modules import messages, add_functions
from add_modules import add_functions, messages

# from create_bot import dp, bot
from create_bot import bot

FILENAME_CHAT = Path("chats_data", "chat_id.txt")

# час запуску бота
# потрібно для відслідковування часу подання запиту до бота: якщо до запуску - ігнорувати команду
time_now = datetime.now()

async def reg(message: types.Message):
    FILENAME = Path("chats_data", f"{message.chat.id}Members.json")

    list_path = [FILENAME, FILENAME_CHAT]

    for path in list_path:
        add_functions.open_file(path)

    time_delta = time_now - message.date
    if(time_delta.total_seconds() <= 0):
        add_functions.save_chat_id(message, FILENAME_CHAT)

        is_registered = 0
        new_user = {
                "id": message.from_user.id,
                "first_name": message.from_user.first_name,
                "last_name": message.from_user.last_name,
                "username": message.from_user.username,
                "count": 0
        }

        is_empty = os.stat(FILENAME).st_size == 0
        if(is_empty):
            users = []
            users.append(new_user)

            with open(FILENAME, 'w') as file:
                json.dump(users, file, indent=1)

            await messages.new_user(message)
        else:
            with open(FILENAME) as file:
                users = json.load(file)
            
            for user in users:
                if(new_user['id'] == user['id']):
                    is_registered = 1
                    break
                else:
                    is_registered = 0
            
            if(is_registered):
                await messages.already_registered(message)
            else:
                users.append(new_user)

                with open(FILENAME, 'w') as file:
                    json.dump(users, file, indent=1)

                await messages.new_user(message)


async def user_of_the_day(message: types.Message):
    FILENAME = Path("chats_data", f"{message.chat.id}Members.json")
    FILENAME_DATE = Path("chats_data", f"{message.chat.id}Date.txt")
    FILENAME_WINNER = Path("chats_data", f"{message.chat.id}Winner.json")

    list_path = [FILENAME, FILENAME_DATE, FILENAME_WINNER, FILENAME_CHAT]

    for path in list_path:
        add_functions.open_file(path)

    # заповнюємо файл з датою, якщо це перший запуск бота в чаті
    is_empty = os.stat(FILENAME_DATE).st_size == 0
    if(is_empty):
        with open (FILENAME_DATE, 'w') as file:
            file.write(datetime(2000, 1, 1).isoformat())

    time_delta = time_now - message.date

    # перевірка на час запиту
    if(time_delta.total_seconds() <= 0):
        add_functions.save_chat_id(message, FILENAME_CHAT)

        is_empty = os.stat(FILENAME).st_size == 0
        if(not is_empty):
            with open(FILENAME_DATE) as file:
                winner_past_iso = file.read()

            with open(FILENAME) as file:
                users = json.load(file)

            # якщо є відмінність у часі у n годин
            # winner_today = add_functions.convert_time(message, 3)
            
            winner_today = datetime(message.date.year, message.date.month, message.date.day)
            winner_past = datetime.fromisoformat(winner_past_iso)

            # winner_today += timedelta(hours=3)
            
            # якщо дата визначення минулого користувача дня менша за теперішню дату - визначити нового
            if(winner_today > winner_past):
                # перезаписати дату нового визначення 
                with open (FILENAME_DATE, 'w') as file:
                    file.write(winner_today.isoformat())

                random.shuffle(users)
                random_user = random.choice(users)
                random_user['count'] += 1

                # перезапис користувачів з оновленим count
                with open(FILENAME, 'w') as file:
                    json.dump(users, file, indent=1)

                # перезапис користувача дня у файл
                with open (FILENAME_WINNER, 'w') as file:
                    json.dump(random_user, file, indent=1)

                await messages.u_r_winner(message, random_user)
            elif(winner_today == winner_past):
                with open(FILENAME_WINNER) as file:
                    winner_now = json.load(file)
            
                if(winner_now['username']):
                    name = winner_now['username']
                    await message.answer(f'Сьогоднішнього переможця вже знайдено - @{name}.')
                elif(winner_now['first_name'] and winner_now['last_name']):
                    name = winner_now['first_name'] + " " + winner_now['last_name']
                    await message.answer(f'Сьогоднішнього переможця вже знайдено - {name}.')
                elif(winner_now['first_name'] and (not winner_now['last_name'])):
                    name = winner_now['first_name']
                    await message.answer(f'Сьогоднішнього переможця вже знайдено - {name}.')
            else:
                print('************Error: winner_today < winner_past*************')
        else:
            await message.answer('Жоден користувач ще не зареєструвався.')


async def user_stats(message: types.Message):
    FILENAME = Path("chats_data", f"{message.chat.id}Members.json")

    list_path = [FILENAME, FILENAME_CHAT]

    for path in list_path:
        add_functions.open_file(path)

    time_delta = time_now - message.date
    if(time_delta.total_seconds() <= 0):
        add_functions.save_chat_id(message, FILENAME_CHAT)


        is_empty = os.stat(FILENAME).st_size == 0
        if(not is_empty):
            with open(FILENAME) as file:
                members = json.load(file)
            
            members.sort(key=lambda x: x['count'], reverse=True)

            result_str = "Список \U0001F413 переможців:\n\n"
            i = 1
            for member in members:
                if(member['username']):
                    result_str += f"{i}. @{member['username']} - {member['count']} раз(-и/-ів)\n"
                elif(member['first_name'] and member['last_name']):
                    result_str += f"{i}. {member['first_name']} {member['last_name']} - {member['count']} раз(-и/-ів)\n"
                elif(member['first_name'] and (not member['last_name'])):
                    result_str += f"{i}. {member['first_name']} - {member['count']} раз(-и/-ів)\n"
                i += 1
            
            await message.answer(result_str)
        else:
            await message.answer('Жоден переможець ще не визначився.')



async def on_start_bot(_):
    print('Бот працює...')
    if(os.path.exists(FILENAME_CHAT)):
        with open (FILENAME_CHAT, 'r') as file:
            lines = file.read().splitlines()

        list_id = [int(item) for item in lines]
        for chat_id in list_id:
            await bot.send_message(chat_id, 'Я онлайн.')
    # await bot.send_message(424925610, 'Я онлайн.')


async def on_stop_bot(_):
    print('Бот не працює...')
    if(os.path.exists(FILENAME_CHAT)):
        with open (FILENAME_CHAT, 'r') as file:
            lines = file.read().splitlines()

        list_id = [int(item) for item in lines]
        for chat_id in list_id:
            await bot.send_message(chat_id, 'Я офлайн.')
    # await bot.send_message(424925610, 'Я офлайн.')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(reg, commands=['reg'])
    dp.register_message_handler(user_of_the_day, commands=['user_of_the_day'])
    dp.register_message_handler(user_stats, commands=['user_stats'])