import telebot
import os
from replies import *
from util import API_KEYS

# if os.environ.get("LOCAL") is None:
bot = telebot.TeleBot(API_KEYS.get("TUALETKA_BOT"))
# else:
#     bot = telebot.TeleBot(os.environ.get("BOTKEY"))


users = {}
sleep_time = os.environ.get("SLEEP")
if sleep_time is None:
    sleep_time = 1000


# TODO:
#  add db support
#  revive the annoyance
#  may be schedulers?


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id,
                     f"/help для этой хуеты\n"
                     f"/join чтобы стать частью семьи\n"
                     f"/bought если ты купил\n"
                     f"/nomoney если не можешь купить\n"
                     f"/need если туалетка закончилась\n"
                     f"/list шобы показать чо пачом по ребятам")


@bot.message_handler(commands=['join'])
def join(message):
    users[message.from_user.username] = [0, True]
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAO3Xit6cgTNTlj2Lgpd0hNcs5i2dcsAAtcCAALzVj8X6AESBi04AhgYBA")
    bot.send_message(message.chat.id, f"@{message.from_user.username}, Добро пожаловать в семью, засрашка")


@bot.message_handler(commands=['bought'])
def bought_toilet_paper(message):
    current_username = message.from_user.username
    current_user = users.get(current_username)
    if current_user is None:
        bot.send_message(message.chat.id, f"@{current_username}, заджойнись сука\n"
                                          f"/join")
        return

    current_user[0] += 1

    # make everyone available
    for user in users.keys():
        users[user][1] = True

    bot.send_sticker(message.chat.id, very_cool_stickers())
    bot.send_message(message.chat.id,
                     f"@{current_username}, аригато гозаимасу, "
                     f"ты уже купил {current_user[0]} туалеток!")


@bot.message_handler(commands=['nomoney'])
def no_money(message):
    current_username = message.from_user.username
    current_user = users.get(current_username)
    if current_user is not None:
        current_user[1] = False  # make him unavailable

    bot.send_sticker(message.chat.id, didnt_buy_stickers())
    bot.send_message(message.chat.id, f"@{message.from_user.username} уу сука я запомнил тебя")
    need_toilet_paper(message)


@bot.message_handler(commands=['need'])
def need_toilet_paper(message):
    current_username = message.from_user.username
    if len(users.keys()) == 0:
        bot.send_message(message.chat.id, f"@{current_username}, заджойнись сука\n"
                                          f"/join")
    available = sorted(list(filter(lambda x: users[x][1], users.keys())))
    if len(available):
        available = min(available, key=lambda x: users[x][0])
        bot.send_message(message.chat.id, f"@{available}, купляешь туалетку")
    else:
        bot.send_sticker(message.chat.id, fuck_you_stickers())
        bot.send_message(message.chat.id, "ТАК БЛЯ ВСЕ ХОТЯТ СРАТЬ А ПОКУПАТЬ НИКТО НЕ ХОЧЕТ ВЫ АХУЕЛИ?")
        # make everyone available
        for user in users.keys():
            users[user][1] = True
        need_toilet_paper(message)


@bot.message_handler(commands=['list'])
def list_users(message):
    list_of_users = ""
    for user, info in users.items():
        list_of_users += f"{user} купил {info[0]} туалеток, availability: {info[1]}\n"
    list_of_users += "nya^_^\n"
    bot.send_message(message.chat.id, list_of_users)


"""pls dont read or translate those"""
bad_words = ['hui', 'хуй', 'пизд', 'пзд']
@bot.message_handler(content_types=['text'])
def fuck_you(message):
    text: str = message.text.lower()
    for bad_word in bad_words:
        if bad_word in text:
            bot.send_sticker(message.chat.id, fuck_you_stickers())
            bot.send_message(message.chat.id, f"@{message.from_user.username} {fuck_you_text()}")


bot.polling()
