from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot
import requests
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

def cancel(update, context):
    cancel_handler(update, context)

def cancel_handler(update, context):
    keyboard = [[InlineKeyboardButton('Купить Биткоин', callback_data='option_1')],
                [InlineKeyboardButton('Промокод', callback_data='option_2'),
                 InlineKeyboardButton('Помощь', callback_data='option_3')],
                [InlineKeyboardButton('Партнерская программа', callback_data='option_4'),
                 InlineKeyboardButton('Обратная связь', callback_data='option_5')],
                [InlineKeyboardButton('Поддержка / Оператор', url="https://t.me/")],
                [InlineKeyboardButton('Отзывы', url="https://t.me/")],
                [InlineKeyboardButton('Новостной канал', url="https://t.me/")],
                [InlineKeyboardButton('Продать биткоин', callback_data='option_9')],
                [InlineKeyboardButton('Мои заказы', callback_data='orders')],
                [InlineKeyboardButton('Правила', callback_data='option_10')],
                [InlineKeyboardButton('⚡ BTC Mixer', url="https://t.me/")],
                [InlineKeyboardButton('📱Надежный VPN', url="https://t.me/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "✌️ Бот обменник! Тут можно обменять свои RUB на BTC. ✌️\n\n Если ты 'новичок' и хочешь получить промокод на скидку? - пиши мне \n\n Жми кнопку '👉 Купить Биткоин 👈' или просто введи сумму в RUB или BTC\n \nПример: 0.001 или 0,001",
        reply_markup=reply_markup)


def main_menu(update, context):
    keyboard = [[InlineKeyboardButton('Купить Биткоин', callback_data='option_1')],
                 [InlineKeyboardButton('Промокод', callback_data='option_2'),
                InlineKeyboardButton('Помощь', callback_data='option_3')],
                 [InlineKeyboardButton('Партнерская программа', callback_data='option_4'),
                InlineKeyboardButton('Обратная связь', callback_data='option_5')],
                 [InlineKeyboardButton('Поддержка / Оператор',  url="https://t.me/")],
                [InlineKeyboardButton('Отзывы', url="https://t.me/")],
                 [InlineKeyboardButton('Новостной канал', url="https://t.me/")],
                [InlineKeyboardButton('Продать биткоин', callback_data='option_9')],
                 [InlineKeyboardButton('Мои заказы', callback_data='orders')],
                [InlineKeyboardButton('Правила', callback_data='option_10')],
                 [InlineKeyboardButton('⚡ BTC Mixer', url="https://t.me/")],
                [InlineKeyboardButton('📱Надежный VPN', url="https://t.me/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("✌️ Бот обменник! Тут можно обменять свои RUB на BTC. ✌️\n\n Если ты 'новичок' и хочешь получить промокод на скидку? - пиши мне \n\n Жми кнопку '👉 Купить Биткоин 👈' или просто введи сумму в RUB или BTC\n \nПример: 0.001 или 0,001", reply_markup=reply_markup)

def process_amount(update, context):
    # Get the user's input
    user_input = update.message.text
    # Check if the input is a valid number
    if user_input.isdigit():
        # Convert the input to an integer
        user_amount = int(user_input)
        # Check if the user entered an amount in rubles or bitcoin
        if user_amount < 4:
            user_amount_float = float(user_amount)
            # The user entered an amount in bitcoin
            # Calculate the equivalent amount in rubles
            btc_rate = 16584.63  # current market rate for BTC in rubles
            user_amount_rubles = user_amount_float * btc_rate * 71
            # Add the commission to the total amount
            user_amount_rubles += 400
            # Display the amount in rubles and the payment options
            context.bot.send_message(chat_id=update.effective_chat.id,text=f"Сумма к оплате: {user_amount_rubles} руб.\n\nПожалуйста, выберите предпочитаемый способ оплаты:")
            # Create a keyboard with options for payment methods
            keyboard = [[telegram.InlineKeyboardButton("Сбербанк ( {}руб.)".format(user_amount_rubles), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("СберБанк MOSCOW ( {}руб.)".format(user_amount_rubles),
                                                       callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Сбербанк Питер ({}руб.)".format(user_amount_rubles),
                                                       callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Visa / MasterCard / МИР ({}руб.)".format(user_amount_rubles),
                                                       callback_data="wallet")],
                        [telegram.InlineKeyboardButton("🚫 Отмена.)", callback_data="cancel")]]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Способы оплаты:", reply_markup=reply_markup)
        elif 5000 > user_amount >= 500:
            # The user entered an amount in bitcoin
            user_amount = user_amount + (18/100*user_amount)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Вы ввели сумму в RUB. Пожалуйста, выберите предпочитаемый способ оплаты:")
            # Create a keyboard with options for payment methods
            keyboard = [[telegram.InlineKeyboardButton("Сбербанк ( {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("СберБанк MOSCOW ( {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Сбербанк Питер ({}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Visa / MasterCard / МИР {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("🚫 Отмена.)", callback_data="cancel")]]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Способы оплаты:",
                                     reply_markup=reply_markup)
        elif user_amount >= 5000:
            # The user entered an amount in bitcoin
            user_amount = user_amount + (15/100*user_amount)
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Вы ввели сумму в RUB. Пожалуйста, выберите предпочитаемый способ оплаты:")
            # Create a keyboard with options for payment methods
            keyboard = [[telegram.InlineKeyboardButton("Сбербанк ( {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("СберБанк MOSCOW ( {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Сбербанк Питер ({}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("Visa / MasterCard / МИР {}руб.)".format(user_amount), callback_data="wallet")],
                        [telegram.InlineKeyboardButton("🚫 Отмена.)", callback_data="cancel")]]
            reply_markup = telegram.InlineKeyboardMarkup(keyboard)
            context.bot.send_message(chat_id=update.effective_chat.id, text="Способы оплаты:",
                                     reply_markup=reply_markup)


    elif 34>=len(user_input)>=27:

        # Define the text variable
        text = ""
        wallet = str(user_input)
        print("Wallet {}".format(wallet))
        return wallet

def convert_currency(amount, currency):
    # Make a request to the API to get the current exchange rate
    api_url = "https://api.coindesk.com/v1/bpi/currentprice/RUB.json"
    try:
        response = requests.get(api_url)
        response_json = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the API request: {e}")
        return

    # Extract the exchange rate from the API response
    try:
        exchange_rate = response_json["bpi"][currency]["rate_float"]
    except KeyError as e:
        print(f"An error occurred while processing the API response: {e}")
        return

    # Convert the amount to Bitcoins and the specified currency
    btc_amount = amount / exchange_rate
    currency_amount = amount

    # Return the conversion results
    return {
        "btc_amount": btc_amount,
        "currency_amount": currency_amount
        }
wallet = "3CCvPjdpB3d2Md8jw8KJspDKJY1A448qHa"
amount = 5000
currency = "RUB"
result = convert_currency(amount, currency)
if result:
    print(f"Вы получите: {result['btc_amount']:.8f} BTC")
    print(f"Вы получите: {result['currency_amount']} {currency}")

def button(update, context):
    # Get the callback data of the button that was pressed
    query = update.callback_query
    data = query.data
    # Define the text variable
    text = ""
    if data == "option_1":
        query = update.callback_query
        data = query.data
        # Define the text variable
        text = ""
        # Check if the input is a valid number
        if data == "option_1":

            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Пожалуйста, введите сумму в BTC или RUB:\n\n Пример: 0.001 или 0,001 или 5030")
            # Add the MessageHandler to the dispatcher
            message_handler = MessageHandler(Filters.text, process_amount)
            context.dispatcher.add_handler(message_handler)
        else:
            print("didn't work")



    elif data == "option_2":
        text = "Вы не можете активировать данный промокод, так как ваш баланс в боте больше 50 руб. Для активации промокода, - создайте обмен и нажмите кнопку Списать с баланса."
    elif data == "option_3":
        text = "Инструкция как пользоваться ботом: https://telegra.ph/Kak-polzovatsya-botom-11-26 \n\n Видеоинструкция: https://youtu.be/-jFd532Fo0w \n\n Не разобрался с ботом? Пиши мне, проведем обмен вручную: \n Промокоды, акции, а также всегда свежие новости в нашем канале: \n Наш канал с отзывами: "
    elif data == "option_4":
        # Create the four buttons"🔗 Моя партнерская ссылка", callback_data="link"
        text = "Условия партнерской программы: Рекомендуйте наш сервис, стройте команду и получайте вознаграждение от каждого обмена привлеченных вами клиентов!\n"
        keyboard = [[telegram.InlineKeyboardButton("🔗 Моя партнерская ссылка", callback_data="option_1")],
                    [telegram.InlineKeyboardButton("📝 Мои финансы", callback_data="option_2"),
                     telegram.InlineKeyboardButton("📖Помощь", callback_data="option_3")],
                    [telegram.InlineKeyboardButton("Вывод комиссионных (кошелек)", callback_data="option_4")]]

        inline_keyboard = telegram.InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text, reply_markup=inline_keyboard)
        return telegram.Update.DEFAULT

    elif data == "option_5":
        text = "Контакты поддержки:  \n\nНаш канал с отзывами: \n\n Новости нашего обменника, а также промокоды, акции и конкурсы в нашем официальном канале:@ "
    elif data == "option_10":
        text = "1. Запрещается использование услуг обменника для незаконных переводов и мошеннических действий. Клиент обязуется предоставлять все документы, удостоверяющие его личность, в случае подозрения о мошенничестве и/или отмывании денег.\n\n"
        text += "2. Администрация обменника имеет право отказать в заключении сделки и выполнении заявки, причем без объяснения причин. Данный пункт применяется по отношению к любому клиенту.\n\n"
        text += "3. Строго запрещено: совершать переводы по номеру 900; оплачивать с банкоматов и терминалов; совершать оплату 2-мя или более переводами без согласования с оператором.\n\n"
        text += "4. Для предотвращения операций незаконного характера, обменник использует внутреннюю систему автоматизированного анализа транзакций и поведения Пользователя (систему предотвращения мошенничества), останавливающую все подозрительные транзакции."

    elif data == "option_9":
        text = "Покупаем от 10000 руб. Если хотите продать BTC, пишите "


    elif data == "wallet":
        text = "Скопируйте и отправьте боту свой кошелек BTC. Бот сохранит его и при следующем обмене предложит в виде удобной кнопки ниже:"
        keyboard = [[telegram.InlineKeyboardButton("✅ согласно", callback_data="precard")],
                    [telegram.InlineKeyboardButton("🚫 Отмена", callback_data="option_1")]]

        inline_keyboard = telegram.InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text, reply_markup=inline_keyboard)
        return telegram.Update.DEFAULT

    elif data == "card":
        text = "5xx3"

    elif data == "precard":
        text = "Время на оплату заказа 15 минут!\n\nОбращаем внимание: средства вы должны отправлять только со своей личной карты. \n\n Администрация может потребовать верификацию документов клиента или задержать обмен для проверки других данных. Средства отправленные без заявки, возврату не подлежат! Оплачивать вы должны ровно ту сумму, которая указана в заявке, иначе ваш платеж «затеряется».  Все претензии по обмену принимаются в течении 24 часов.\n\nВНИМАТЕЛЬНО сверяйте адрес своего кошелька! \n\n После оплаты средства будут переведены на свой кошелек {}\n\n Если у вас есть вопрос, или возникли проблемы с оплатой, пишите поддержке: @ \n\n Вы согласны на обмен?".format(wallet)
        keyboard = [[telegram.InlineKeyboardButton("✅ согласно", callback_data="card")],
                    [telegram.InlineKeyboardButton("🚫 Отмена", callback_data="option_1")]]

        inline_keyboard = telegram.InlineKeyboardMarkup(keyboard)
        update.callback_query.edit_message_text(text, reply_markup=inline_keyboard)
        return telegram.Update.DEFAULT
    elif data == "cancel":
        cancel_handler(update, context)
        return telegram.Update.DEFAULT


    # Edit the message to display the new text
    query.edit_message_text(text=text)






def start(update, context):
    main_menu(update, context)


updater = Updater("59xg", use_context=True)
bot = Bot("59376696xxg")
start_handler = CommandHandler('start', start)
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.start_polling()
updater.idle()
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", lambda update, context: print("/start command received")))
dp.add_handler(MessageHandler(Filters.text, process_amount))
cancel_handler = CommandHandler("cancel", cancel)
updater.dispatcher.add_handler(cancel_handler)

