import os
import sys
import logging
import asyncio
from aiogram.types import BotCommand
from aiogram.filters import Command
from dotenv import load_dotenv
from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.web_app_info import WebAppInfo
from bs4 import BeautifulSoup
from parse import parse_apartments



load_dotenv()
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

status_send = True

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Розпочати розсилку"),
        BotCommand(command="find_apartamens", description="Пошук квартир"),
        BotCommand(command="help", description="Хто я")
    ]
    await bot.set_my_commands(commands)

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    global status_send
    status_send = True
    
    while status_send:
        await message.answer('Це займе трохи часу, зачекай...')

        links = parse_apartments()

        for link_dict in links:
            link = link_dict.get('link')
            if link:
                await message.answer(link)
                await asyncio.sleep(1)
        
        await asyncio.sleep(14400)


@dp.message(Command(commands=["stop"]))
async def stop(message: types.Message):
    global status_send
    status_send = False

    await message.answer('Розсилку зупинено')

@dp.message(Command(commands=["find_apartamens"]))
async def send_links(message: types.Message):
    await message.answer('Це займе трохи часу, зачекай...')

    links = parse_apartments()

    for link_dict in links:
        link = link_dict.get('link')
        if link:
            await message.answer(link)
            await asyncio.sleep(1)

@dp.message(Command(commands=["help"]))
async def help(message: types.Message):
    await message.answer('''В мене є пару корисних команд, перша команда це: /find_apartamens
вона шукає квартири в Києві до 12000 гривень в таких районах:   
Печерський, Шевченківський, Подільський, Оболонський, Солом'янський
Наступна команда це: /start грубо кажучи ти підписуєшься на мою розсиклу,
кожні 4 години тобі будуть приходити повідомлення з квартирами, На разі це все :) 
                         ''')
    

@dp.message()
async def echo(message: types.Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer('IDK')

async def main():
    try:
        await set_commands(bot)

        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
