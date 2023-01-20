import telebot
from config import TOKEN, currency
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
\n<в какую валюту перевести> \
\n<колличество переводимой валюты> \
\nУвидеть список доступных валют: /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()

        if len(values) != 3:
            raise APIException('Введите три параметра\n например:   доллар рубль 10')

        quote, base, amount = values
        amount = amount.replace(',', '.')  # нечувствительность к запятой
        quote, base = quote.lower(), base.lower()  # преобразование регистра

        convertion = CurrencyConverter.get_price(quote, base, amount)
        total, rate = convertion
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(total, 2)}\n курс\t {rate}'
        bot.send_message(message.chat.id, text)


bot.polling()
