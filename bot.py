import os
import sys
import logging
import asyncio
import requests
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.types.web_app_info import WebAppInfo
from bs4 import BeautifulSoup
from parse import parse_apartments



load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def send_links(message: types.Message):
    links = parse_apartments()
    
    for link_dict in links:
        link = link_dict.get('link')
        if link:  
            await message.answer(link)
    

@dp.message()
async def echo(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('IDK')

async def main():
    bot = Bot(token=TELEGRAM_TOKEN)

    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())