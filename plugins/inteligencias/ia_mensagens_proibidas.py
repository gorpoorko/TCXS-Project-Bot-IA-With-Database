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
import subprocess
import time
import speech_recognition as sr
from pydub import AudioSegment
import os
import dropbox
import re
import wikipedia
import sqlite3
from config import bot, sudoers, logs, bot_username,token_dropbox
from datetime import datetime
from plugins.admins import is_admin



async def ia_mensagens_proibidas(msg):
    try:
        id_usuario = msg['from']['id']
        adm = await is_admin(msg['chat']['id'], msg['from']['id'], id_usuario)
    except Exception as e:
        pass
    try:
        conexao_sqlite = sqlite3.connect('bot_database.db')
        conexao_sqlite.row_factory = sqlite3.Row
        cursor_sqlite = conexao_sqlite.cursor()
        chat_id = msg['chat']['id']
        # se a mensagem e no privado do bot-------------->
        if msg['chat']['type'] == 'private':
            grupo = f'Privado: @{bot_username}'
            try:
                usuario = msg['from']['username']
            except:
                usuario = f"@{msg['from']['id']}({msg['from']['first_name']})"
                pass
            try:
                texto = msg['text']
            except:
                pass
        #se a mensagem e no canal do bot-------------->
        if msg['chat']['type'] == 'channel':
            grupo = f'Canal: @{bot_username}'
            usuario = f'Administrador do: @{bot_username}'
            try:
                texto = msg['text']
            except:
                pass
        # se for um supergrupo ou grupo secreto ele trata o nome do grupo e o usuario se ele tem ou nao um username
        if msg['chat']['type'] == 'supergroup':
            try:
                grupo = f"https://t.me/{msg['chat']['username']}"
            except:
                grupo = f"Secreto: {msg['chat']['title']}"
                pass
            try:
                usuario = msg['from']['username']
            except:
                usuario = f"@{msg['from']['id']}({msg['from']['first_name']})"
                pass
            try:
                texto = msg['text']
            except:
                pass
            try:
                linguagem = msg['from']['language_code']
            except:
                linguagem = 'none'
                pass
        data = datetime.now().strftime('%d/%m/%Y %H:%M')
        chat_type = msg['chat']['type']
        id_grupo = msg['chat']['id']
        # SISTEMA QUE DELETA MENSAGENS PROIBIDAS --------------------------------------------------------------------->
        if chat_type == 'supergroup' and msg.get('text'):# verifica se a palavra é proibida, se for deleta a mensagem do usuario e envia um aviso------>
                cursor_sqlite.execute("""SELECT * FROM proibido; """)
                mensagens_proibidas = cursor_sqlite.fetchall()
                for mensagem in mensagens_proibidas:
                    if mensagem['termo'] in texto and not 'permitir' in texto:
                        try:#em caso de erro inverter este try except pelo de baixo pois da erro entre message_id e reply_to_message
                            await bot.deleteMessage((msg['chat']['id'], msg['message_id']))
                            await bot.sendMessage(chat_id,f"@{msg['from']['username']} `você usou uma palavra proibida, não fale bosta aqui!`",'markdown')
                        except TelegramError:

                            try:
                                await bot.deleteMessage((msg['chat']['id'], msg['reply_to_message']['message_id']))
                                await bot.sendMessage(chat_id,f"@{msg['from']['username']} `você usou uma palavra proibida, não fale bosta aqui!`",'markdown')
                            except TelegramError:
                                pass

        try:
            if msg.get('text'):
                texto = msg['text']
                if texto.lower().startswith('proibir') and adm['user'] == True:  # proibe as palavras e as cadastra na Database------------------------------->
                    palavra_proibida = texto[8:]
                    if palavra_proibida.lower() == 'proibir' or palavra_proibida.lower() == '' or palavra_proibida.lower() == ' '  or palavra_proibida.lower() == '' or palavra_proibida.lower() == 'comandos' or palavra_proibida.lower() == '/help' or palavra_proibida.lower() == 'fale sobre' or palavra_proibida.lower() == 'frequencia' or palavra_proibida.lower() == 'cmd' or palavra_proibida.startswith('/') or palavra_proibida.startswith('#') or palavra_proibida.startswith('$') or palavra_proibida.startswith('%') or palavra_proibida.startswith('@'):
                        await bot.sendMessage(chat_id,f"@{msg['from']['username']} `não posso proibir esta palavra, talvez ela seja um comando meu.`",'markdown')
                        pass
                    else:
                        cursor_sqlite.execute(f"""INSERT INTO proibido VALUES('{palavra_proibida}')""")
                        conexao_sqlite.commit()
                        await bot.sendMessage(chat_id,f'🤖🚫 `Proibido:`***{palavra_proibida}***\nPara voltar permitir esta palavra use o comando `permitir`, para ver palavras proibidas use `proibidas`','markdown', reply_to_message_id=msg['message_id'])
                if texto.lower().startswith('proibir') and adm['user'] == False:
                    await bot.sendMessage(chat_id,f"@{msg['from']['username']} `este comando é permitido so para admin's`",'markdown')
                if texto.lower().startswith('permitir') and adm['user'] == True:  # permite novamente as palavras e as descadastra na Database------------------------------->
                    palavra_permitida = texto[9:]
                    cursor_sqlite.execute(f"""DELETE FROM proibido WHERE termo='{palavra_permitida}'""")
                    conexao_sqlite.commit()
                    await bot.sendMessage(chat_id, f'🤖✔️ `Permitido:`***{palavra_permitida}***\nPara voltar proibir esta palavra use o comando `proibir`, para ver palavras proibidas use `proibidas`','markdown', reply_to_message_id=msg['message_id'])
                if texto.lower().startswith('permitir') and adm['user'] == False:
                    await bot.sendMessage(chat_id,f"@{msg['from']['username']} `este comando é permitido so para admin's`",'markdown')

                if texto.lower().startswith('proibidas'):  # lista as palavras proibidas cadastradas  na Database------------------------------->
                    cursor_sqlite.execute("""SELECT * FROM proibido; """)
                    mensagens_proibidas = cursor_sqlite.fetchall()
                    todas_proibidas = []
                    separador = ' \n'
                    for result in mensagens_proibidas:
                        todas_proibidas.append(result['termo'])
                    await bot.sendMessage(chat_id,f'🤖 `Palavras Proibidas:`\n ***{separador.join(map(str, todas_proibidas))}***','markdown', reply_to_message_id=msg['message_id'])
                    await bot.sendMessage(chat_id, 'Para proibir use `proibir` e para permitir use `permitir`', 'markdown')
        except Exception as e:
            pass
# excessao final para tratar do codigo todo--->
    except:
        pass
        return True
