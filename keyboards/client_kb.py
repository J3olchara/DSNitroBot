from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
products = KeyboardButton('🛒Меню')
support = KeyboardButton('❓Поддержка❓')
UserProfile = KeyboardButton("📝Мой профиль")
rules = KeyboardButton("©Правила покупки")
reviews = KeyboardButton("📩Отзывы")
MainButtons = ReplyKeyboardMarkup(resize_keyboard = True)
MainButtons = MainButtons.row(products, UserProfile).add(rules, reviews, support)

BalanceTopUpAmount = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard=True).row(KeyboardButton('50₽'),KeyboardButton('100₽')).row(KeyboardButton('300₽'),KeyboardButton('500₽')).add(KeyboardButton('Отмена'))


OrderButtons = ReplyKeyboardMarkup(resize_keyboard = True).row(KeyboardButton("Проверить оплату"), KeyboardButton("Отмена оплаты"))
def PayCheckingButton(url):
    return InlineKeyboardMarkup(row_width = 1).add(InlineKeyboardButton(text = "Оплатить", url = url)) 
def DirectPayCheckingButton(url, amount, bill_id, ProductType, NewPaymentID):
    Pay = InlineKeyboardButton(text = f"Оплатить {amount}₽", url = url)
    PaymentCheck = InlineKeyboardButton(text = "Проверить оплату", callback_data = f"DP {bill_id} {amount} {ProductType} {NewPaymentID}")
    PaymentCancel = InlineKeyboardButton(text = "Отменить оплату", callback_data = f"DDP {bill_id} {amount} {ProductType} {NewPaymentID}")
    return InlineKeyboardMarkup(row_width = 2).add(Pay).row(PaymentCheck, PaymentCancel)