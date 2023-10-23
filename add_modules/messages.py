import time
from aiogram import types


async def already_registered(message: types.Message):
    if(message.from_user.username):
        await message.answer(f'@{message.from_user.username}, ти вже зареєстрований.')
    elif(message.from_user.first_name and message.from_user.last_name):
        await message.answer(f'{message.from_user.first_name} {message.from_user.last_name}, ти вже зареєстрований.')
    elif(message.from_user.first_name and (not message.from_user.last_name)):
        await message.answer(f'{message.from_user.first_name}, ти вже зареєстрований.')


async def new_user(message: types.Message):
    if(message.from_user.username):
        await message.answer(f'Оп, новий гравець - (@{message.from_user.username}).')
    elif(message.from_user.first_name and message.from_user.last_name):
        await message.answer(f'Оп, новий гравець - ({message.from_user.first_name} {message.from_user.last_name}).')
    elif(message.from_user.first_name and (not message.from_user.last_name)):
        await message.answer(f'Оп, новий гравець - ({message.from_user.first_name}).')


async def u_r_winner(message: types.Message, winner):
    list_of_phrase = ['Збираємо інформацію \U0001F970', 
                      'Аналізуємо дані \U0001F608', 
                      'Повторний аналіз \U0001F4A6']
    if(winner['username']):
        time.sleep(1)
        for phrase in list_of_phrase:
            await message.answer(phrase)
            time.sleep(2)
        await message.answer(f"Опааа, сьогоднішній переможець - @{winner['username']} \U0001F48B")
    elif (winner['first_name'] and winner['last_name']):
        time.sleep(1)
        for phrase in list_of_phrase:
            await message.answer(phrase)
            time.sleep(2)
        await message.answer(f"Опааа, сьогоднішній переможець - {winner['first_name']} {winner['last_name']} \U0001F48B")
    elif (winner['first_name'] and (not winner['last_name'])):
        time.sleep(1)
        for phrase in list_of_phrase:
            await message.answer(phrase)
            time.sleep(2)
        await message.answer(f"Опааа, сьогоднішній переможець - {winner['first_name']} \U0001F48B")
