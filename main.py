from aiogram import executor
from create_bot import dp

from handlers import client
# from server import keep_alive
# from handlers.client import FILENAME_CHAT


client.register_handlers_client(dp)

if __name__ == "__main__":
    # keep_alive()
    executor.start_polling(dp, 
                           on_startup=client.on_start_bot, 
                           on_shutdown=client.on_stop_bot)