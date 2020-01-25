import telebot
from os import environ
from replies import *


bot = telebot.TeleBot(environ.get("BOTKEY"))
users = {
}
# TODO:
#  add annoying reminder
#  add db support


@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.chat.id,
                     f"/help для этой хуеты\n"
                     f"/join чтобы стать частью семьи\n"
                     f"/bought если ты купил\n"
                     f"/nomoney если не можешь купить\n"
                     f"/need если туалетка закончилась")


@bot.message_handler(commands=['join'])
def join(message):
    users[message.from_user.username] = [0, True]
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAO3Xit6cgTNTlj2Lgpd0hNcs5i2dcsAAtcCAALzVj8X6AESBi04AhgYBA")
    bot.send_message(message.chat.id, f"@{message.from_user.username}, Добро пожаловать в семью, засрашка")


@bot.message_handler(commands=['bought'])
def bought_toilet_paper(message):
    username = message.from_user.username
    users[username][0] += 1

    # make everyone available
    for user in users.keys():
        users[user][1] = True

    bot.send_sticker(message.chat.id, very_cool_stickers())
    bot.send_message(message.chat.id,
                     f"@{message.from_user.username}, аригато гозаимасу, "
                     f"ты уже купил {users[username][0]} туалеток!")


@bot.message_handler(commands=['nomoney'])
def no_money(message):
    users[message.from_user.username][1] = False  # make him unavailable
    bot.send_sticker(message.chat.id, didnt_buy_stickers())
    bot.send_message(message.chat.id, f"@{message.from_user.username} уу сука я запомнил тебя")
    need_toilet_paper(message)


@bot.message_handler(commands=['need'])
def need_toilet_paper(message):
    available = list(filter(lambda x: users[x][1], users.keys()))
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
