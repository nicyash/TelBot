import telebot
from config import keys, TOKEN
from extensions import ConvertionException, ValueConvertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def helper(message: telebot.types.Message):
    text = 'Чтобы наать работу введите команду в следующем формате:\n <имя валюты, цену которой он хочет узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n Команда /value выводит список доступных валют'
    bot.reply_to(message, text)


@bot.message_handler(commands=['value'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        value = message.text.split(' ')

        if len(value) != 3:
            raise ConvertionException('Слишком много параметров')

        quote, base, amount = value
        total_base = ValueConvertor.get_price(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Неудалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
