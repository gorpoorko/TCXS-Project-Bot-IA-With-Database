# -*- coding: utf-8 -*-
#███╗   ███╗ █████╗ ███╗   ██╗██╗ ██████╗ ██████╗ ███╗   ███╗██╗ ██████╗
#████╗ ████║██╔══██╗████╗  ██║██║██╔════╝██╔═══██╗████╗ ████║██║██╔═══██╗
#██╔████╔██║███████║██╔██╗ ██║██║██║     ██║   ██║██╔████╔██║██║██║   ██║
#██║╚██╔╝██║██╔══██║██║╚██╗██║██║██║     ██║   ██║██║╚██╔╝██║██║██║   ██║
#██║ ╚═╝ ██║██║  ██║██║ ╚████║██║╚██████╗╚██████╔╝██║ ╚═╝ ██║██║╚██████╔╝
#╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝ ╚═════╝
#     [+] @GorpoOrko 2020 - Telegram Bot and Personal Assistant [+]
#     |   TCXS Project Hacker Team - https://tcxsproject.com.br   |
#     |   Telegram: @GorpoOrko Mail:gorpoorko@protonmail.com      |
#     [+]        Github Gorpo Dev: https://github.com/gorpo     [+]

import html
import re
import random
import amanobot
import aiohttp
from amanobot.exception import TelegramError
import time
from config import bot, sudoers, logs, bot_username
from utils import send_to_dogbin, send_to_hastebin

async def coub(msg):
    if msg.get('text'):

        if msg['text'].startswith('/coub') or msg['text'].startswith('coub'):
            text = msg['text'][4:]
            
            try:
                
                async with aiohttp.ClientSession() as session:
                    r = await session.get(f'https://coub.com/api/v2/search/coubs?q={text}')
                    rjson = await r.json()
                content = random.choice(rjson['coubs'])
                links = content['permalink']
                title = content['title']
                
                await bot.sendMessage(msg['chat']['id'], f'*{title}*[\u00AD](https://coub.com/v/{links})',
                                      reply_to_message_id=msg['message_id'], parse_mode="Markdown")

            except IndexError:
                await bot.sendMessage(msg['chat']['id'], 'Not Found!', reply_to_message_id=msg['message_id'])
                
            return True
   