
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
SendMessageForAllUsers = KeyboardButton("Написать всем пользователям")
BalanceChange = KeyboardButton("Изменить баланс пользьзователя")
EnterProducts = KeyboardButton("Внести товар")
CancelHandler = KeyboardButton("Отмена")
clientmode = KeyboardButton("Клиентский режим")
AdminButtons = ReplyKeyboardMarkup(resize_keyboard = True).add(SendMessageForAllUsers).row(BalanceChange, EnterProducts).add(CancelHandler, clientmode)


products = KeyboardButton('🛒Меню')
support = KeyboardButton('❓Поддержка❓')
UserProfile = KeyboardButton("📝Мой профиль")
AdminPanel = KeyboardButton("Админ панель")
rules = KeyboardButton("©Правила покупки")
reviews = KeyboardButton("📩Отзывы")
UpgradedButtons = ReplyKeyboardMarkup(resize_keyboard = True).row(products, UserProfile).add(rules, reviews, support).add(AdminPanel)




