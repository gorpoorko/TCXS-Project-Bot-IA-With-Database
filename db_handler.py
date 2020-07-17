
import sqlite3











#dados anteriores---------------------->

try:
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    try:
        # seta a frequencia com 1 para o bot sempre falar pouco quando iniciado
        cursor.execute(f"""INSERT INTO frequencia(valor)VALUES('1')""")
    except:
        pass
    # tabela da loja_doadores TCXS STORE PKG para doadores
    cursor.execute("""  CREATE TABLE IF NOT EXISTS loja_doadores (int_id integer not null primary key autoincrement, versao varchar(5000), pkg varchar(5000));  """)
    # tabela do fix HAN
    cursor.execute("""  CREATE TABLE IF NOT EXISTS fix_han (int_id integer not null primary key autoincrement, versao varchar(5000), pkg varchar(5000));  """)
    # tabela do fix HEN
    cursor.execute("""  CREATE TABLE IF NOT EXISTS fix_hen (int_id integer not null primary key autoincrement, versao varchar(5000), pkg varchar(5000));  """)
    # tabela do fix XML EXCLUSIVO CFW
    cursor.execute("""  CREATE TABLE IF NOT EXISTS fix_cfw_xml (int_id integer not null primary key autoincrement, versao varchar(5000), pkg varchar(5000));  """)
    # tabela do fix XML EXCLUSIVO HEN
    cursor.execute("""  CREATE TABLE IF NOT EXISTS fix_hen_xml (int_id integer not null primary key autoincrement, versao varchar(5000), pkg varchar(5000));  """)

    #tabela das mensagens aleatorias da IA
    cursor.execute("""  CREATE TABLE IF NOT EXISTS mensagens  (int_id integer not null primary key autoincrement, 'tipo' TEXT, mensagem TEXT);  """)
    #tabela dos comandos que podem ser cadastrados com #      | deletar %  recadastrar $
    cursor.execute("""  CREATE TABLE IF NOT EXISTS comandos   (int_id integer not null primary key autoincrement, tipo varchar(5000), comando varchar(5000), resposta varchar(5000));  """)
    #insere um comando na tabela para questao de testes do bot
    cursor.execute(f"""INSERT INTO comandos(int_id,tipo,comando,resposta)VALUES(1,'texto','oi','Olá Brow, como você vai?')""")
    #tabela para cadastrar perguntas feitas pelos usuarios usando ??
    cursor.execute("""  CREATE TABLE IF NOT EXISTS perguntas  (int_id integer not null primary key autoincrement, usuario varchar(5000), pergunta varchar(5000));  """)
    #tabela de frequencia para dizer quanto o bot pode falar
    cursor.execute("""  CREATE TABLE IF NOT EXISTS frequencia  (valor int);  """)
    # seta a frequencia com 1 para o bot sempre falar pouco quando iniciado
    cursor.execute(f"""INSERT INTO frequencia(valor)VALUES('1')""")
    #tabela das palavras que podem ser definidas como proibidas no grupo
    cursor.execute("""  CREATE TABLE IF NOT EXISTS proibido (termo varchar(5000));  """)





    conn.commit()
    conn.close()
except:
    pass
conn = sqlite3.connect('bot.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS chats (chat_id INTEGER,
                                                    welcome,
                                                    welcome_enabled INTEGER,
                                                    rules,
                                                    goodbye,
                                                    goodbye_enabled INTEGER,
                                                    ia INTEGER,
                                                    warns_limit INTEGER,
                                                    antipedro_enabled INTEGER,
                                                    antipedro_list,
                                                    chat_lang,
                                                    cached_admins)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                                    user_id INTEGER,
                                                    ia INTEGER,
                                                    chat_lang)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS channels (
                                                       chat_id INTEGER)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS was_restarted_on (
                                                               chat_id INTEGER,
                                                               message_id INTEGER)''')


def chat_exists(chat_id):
    cursor.execute('SELECT * FROM chats WHERE chat_id = (?)', (chat_id,))
    if cursor.fetchone():
        return True
    else:
        return False


def channel_exists(chat_id):
    cursor.execute('SELECT * FROM channels WHERE chat_id = (?)', (chat_id,))
    if cursor.fetchone():
        return True
    else:
        return False


def user_exists(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = (?)', (user_id,))
    if cursor.fetchone():
        return True
    else:
        return False


def del_restarted():
    cursor.execute('DELETE FROM was_restarted_on')
    conn.commit()


def add_chat(chat_type, chat_id, chat_lang='en'):
    if chat_type == 'private':
        if not user_exists(chat_id):
            cursor.execute('INSERT INTO users (user_id, chat_lang) VALUES (?,?)', (chat_id, chat_lang))
            conn.commit()
    elif chat_type == 'supergroup' or chat_type == 'group':
        if not chat_exists(chat_id):
            cursor.execute('INSERT INTO chats (chat_id, welcome_enabled, antipedro_list, chat_lang) VALUES (?,?,?,?)',
                           (chat_id, True, '[]', chat_lang))
            conn.commit()
    elif chat_type == 'channel':
        if not channel_exists(chat_id):
            cursor.execute('INSERT INTO channels (chat_id) VALUES (?)', (chat_id,))
            conn.commit()


def get_restarted():
    cursor.execute('SELECT * FROM was_restarted_on')
    return cursor.fetchone()


def set_restarted(chat_id, message_id):
    cursor.execute('INSERT INTO was_restarted_on VALUES (?, ?)', (chat_id, message_id))
    conn.commit()
