from platform import python_branch
from aiogram import types 
import asyncio
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import ContentType
from bot_body import bot, dp
from aiogram.dispatcher.filters import Text
from database.adminDB import insert_admin, take_admins_id
from database.userlistDB import InsertBalance, InsertNewUser, get_users_id, ProfileData, BuyerBalanceUpdate, BuyerBalanceCheck
from database.ProductsDB import AllProductList, TakeProductsList, buying_product
from database.receiptsDB import TakeNewPaymentID, InsertingBillInformation
from keyboards import inline_kb
from keyboards.client_kb import MainButtons, BalanceTopUpAmount, OrderButtons, PayCheckingButton, DirectPayCheckingButton
from keyboards.admin_kb import UpgradedButtons
from keyboards.inline_kb import ProductBuying_kb, InlineBalanceTopUp
from kassa import TGCreateTopUpInvoice, YandexCreateTopUpInvoice, QiwiCreateTopUpInvoice, qiwi
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, reply_keyboard
#from keyboards.inline_kb import Products

async def startcommand(message: types.Message):
    userlist = await get_users_id()
    admins = await take_admins_id()
    if str(message.from_user.id) not in userlist:
        await InsertNewUser(message.from_user.username, str(message.from_user.id))
        await bot.send_message(message.from_user.id, "Привет! Используй кнопки снизу для использования магазина", reply_markup = MainButtons)
        await bot.send_message(message.from_user.id, "В связи с обстановкой в мире, если вы проживаете в РФ и у вас привязана карта Российского Банка к вашему дискорд аккаунту, есть возможность, что у вас не активируется дискорд нитро. Для того чтобы активировать его отвяжите от своего аккаунта свою банковскую карту, так же лучше используйте впн при активации гифта. Если выполнив эти действия вы всеравно не можете активировать гифт, пишите в саппорт", reply_markup = MainButtons)
    else:
        if message.from_user.id in admins:
            await bot.send_message(message.from_user.id, "Привет! Используй кнопки снизу для использования магазина", reply_markup = UpgradedButtons)
            await bot.send_message(message.from_user.id, "В связи с обстановкой в мире, если вы проживаете в РФ и у вас привязана карта Российского Банка к вашему дискорд аккаунту, есть возможность, что у вас не активируется дискорд нитро. Для того чтобы активировать его отвяжите от своего аккаунта свою банковскую карту, так же лучше используйте впн при активации гифта. Если выполнив эти действия вы всеравно не можете активировать гифт, пишите в саппорт", reply_markup = UpgradedButtons)
        else:
            await bot.send_message(message.from_user.id, "Привет! Используй кнопки снизу для использования магазина", reply_markup = MainButtons)
            await bot.send_message(message.from_user.id, "В связи с обстановкой в мире, если вы проживаете в РФ и у вас привязана карта Российского Банка к вашему дискорд аккаунту, есть возможность, что у вас не активируется дискорд нитро. Для того чтобы активировать его отвяжите от своего аккаунта свою банковскую карту, так же лучше используйте впн при активации гифта. Если выполнив эти действия вы всеравно не можете активировать гифт, пишите в саппорт", reply_markup = MainButtons)
async def reviews(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    await bot.send_message(message.from_user.id, "Посмотреть или оставить отзыв можно тут:\n")

async def NewAdmin(message: types.Message):
    userlist = await get_users_id()
    admins = await take_admins_id()
    if str(message.from_user.id) not in userlist:
        await InsertNewUser(message.from_user.username, message.from_user.id)
        if message.from_user.id not in admins:
            await insert_admin(message.from_user.username, message.from_user.id)
            await bot.send_message(message.from_user.id, "Теперь ты админ", reply_markup = UpgradedButtons)
        else:
            await bot.send_message(message.from_user.id, "Ты и так админ, зачем ты это делаешь?")
    else:
        if message.from_user.id not in admins:
            await insert_admin(message.from_user.username, message.from_user.id)
            await bot.send_message(message.from_user.id, "Теперь ты админ")
        else:
            await bot.send_message(message.from_user.id, "Ты и так админ, зачем ты это делаешь?")

async def CheckMyProfile(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    userlist = await get_users_id()
    if str(message.from_user.id) not in userlist:
        await InsertNewUser(message.from_user.username, str(message.from_user.id))
        ID = message.from_user.id
        userdata = await ProfileData(str(ID))
        username = message.from_user.username
        balance = userdata[2]
        msg = await bot.send_message(message.from_user.id, f"Ваше имя @{username}\n🔑Ваш Telegram ID: {ID}\n\n💰На вашем счету {balance}₽")
                               #reply_markup = InlineKeyboardMarkup(row_width = 1)
                               #.add(InlineKeyboardButton(text = "Пополнить баланс", callback_data = f"TopUp {ID}")))
    else:
        ID = message.from_user.id
        userdata = await ProfileData(str(ID))
        username = userdata[0]
        balance = userdata[2]
        msg = await bot.send_message(message.from_user.id, f"📓Ваше имя @{username}\n🔑Ваш Telegram ID: {ID}\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n💰На вашем счету {balance}₽\n➖➖➖➖➖➖➖➖➖➖➖➖➖")
                               #reply_markup = InlineKeyboardMarkup(row_width = 1)
                               #.add(InlineKeyboardButton(text = "Пополнить баланс", callback_data = f"TopUp {ID}")))
class BalanceTopUpCount(StatesGroup):
    amount = State()
async def top_up_start(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    await bot.send_message(call.from_user.id, text = "Введите сумму пополнения(в рублях) или воспользуйтесь кнопками внизу",
                           reply_markup = BalanceTopUpAmount) 
    async with state.proxy() as data:
        data["callback"] = call
    await BalanceTopUpCount.amount.set()
async def GetTopUpAmount(message: types.Message, state: FSMContext):
    if "₽" in message.text:
        async with state.proxy() as data:
            amount = int(message.text.replace("₽", ""))
            data['amount'] = int(amount)
    elif " " in message.text:
        async with state.proxy() as data:
            amount = int(message.text.replace(" ", ""))
            data['amount'] = int(amount)
    else:
        try:
            async with state.proxy() as data:
                amount = int(message.text)
                data['amount'] = amount
        except:
            await bot.send_message(message.from_user.id, "Ошибка в получении суммы пополнения")
            return
    if amount >= 5:
        try:
            ID = message.from_user.id
            admins = await take_admins_id()
            NewPaymentID = await TakeNewPaymentID()
            bill = await QiwiCreateTopUpInvoice(ID, amount, NewPaymentID)
            bill_id = bill.bill_id
            url = bill.pay_url
            await bot.send_message(message.from_user.id, f"Пополнениие на сумму {amount}₽ для пользователя {ID}\nВремя на оплату 10 минут", 
                                   reply_markup = DirectPayCheckingButton(url, amount, bill_id, NewPaymentID))
            await state.finish()
        except Exception:
            admins = await take_admins_id()
            if str(message.from_user.id) in admins:
                await bot.send_message(message.from_user.id, "Ошибка в создании платежа", reply_markup = UpgradedButtons)
                await state.finish()
            else: 
                await bot.send_message(message.from_user.id, "Ошибка создания платежа", reply_markup = MainButtons)
                await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Сумма пополнения должна быть больше 5₽", reply_markup = MainButtons)
        await state.finish()
async def CheckPaymentStatus(call: types.CallbackQuery):
    data = call.data.replace("Payment ", "").split(" ")
    bill_id = data[0]
    ID = call.from_user.id
    username = call.from_user.username
    amount = data[1]
    await call.answer()
    if str(qiwi.check(bill_id = bill_id).status) == "PAID":
        await bot.send_message(ID, f"Счёт оплачен")
        admins = await take_admins_id()
        paymentID = await TakeNewPaymentID()
        if ID in admins:
            await bot.send_message(ID, f"Ваш баланс пополнен на {amount}", reply_markup = UpgradedButtons)
            await InsertingBillInformation(paymentID, ID, username, amount, bill_id)
            await BuyerBalanceUpdate(ID, amount)
        else:
            await bot.send_message(ID, f"Ваш баланс пополнен на {amount}", reply_markup = MainButtons)
            await InsertingBillInformation(paymentID, ID, username, amount, bill_id)
            await BuyerBalanceUpdate(ID, amount)
    else:
        await bot.send_message(ID, "Счёт не оплачен")
async def CancelPayment(call: types.CallbackQuery):
    data = call.data.replace("DelPayment ", "").split(" ")
    bill_id = data[0]
    amount = data[1]
    admins = await take_admins_id()
    await call.answer()
    await qiwi.check(bill_id = bill_id).reversal
    if call.from_user.id in admins:
        await bot.send_message(call.from_user.id, "Пополнение отменена.\nВозврат в главное меню", reply_markup = UpgradedButtons)
        await BuyingProduct(call)
    else:
        await bot.send_message(call.from_user.id, "Пополнение отменена.\nВозврат в главное меню", reply_markup = MainButtons)

        await BuyingProduct(call)

async def CancelHandler(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    currentstate = await state.get_state()
    if currentstate == None:
        return
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Пополение отменено", reply_markup = MainButtons)

async def TermsConfirmation(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    await bot.send_message(message.from_user.id, 
                           "❗️Начните записывать видео❗️\nУчтите что на вашем видео должны быть сочтены следующие условия:\n 1. Включение впн(ВРЕМЕННО)\n 2. Отвязывание карт от аккаунта/показ их отсутствия(ВРЕМЕННО)\n 3. Оплата\n 4. Получение товара\n 5. Попытка использовать товар (не более 5 секунд задержки, с момента получения товара), более 5 секунд = мог активировать с другого устройства.\n ❗️Товар проверяется на валид перед выдачей и видео нужно только если произойдет какая-либо непредвиденная ситуация", reply_markup = InlineKeyboardMarkup(row_width = 2).row(
                               InlineKeyboardButton(text = "Я согласен", callback_data = "TC Yes"), 
                               InlineKeyboardButton(text = "Я отказываюсь", callback_data = "TC No")))
async def TermsCanceling(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    await bot.send_message(call.from_user.id, "Для того чтобы пользоваться магазином нужно принять правила")

async def BuyingProduct(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    userlist = await get_users_id()
    DSNitro1monthCount = await TakeProductsList("DSNitro1month")
    if DSNitro1monthCount == []:
        DSNitro1monthCount = 0
    else: 
        DSNitro1monthCount = len(DSNitro1monthCount)
    DSNitro1yearCount = await TakeProductsList("DSNitro1year")
    if DSNitro1yearCount == []:
        DSNitro1yearCount = 0
    else: 
        DSNitro1yearCount = len(DSNitro1yearCount)
    DSClassic1monthCount = await TakeProductsList("DSClassic1month")
    if DSClassic1monthCount == []:
        DSClassic1monthCount = 0
    else: 
        DSClassic1monthCount = len(DSClassic1monthCount)
    DSClassic1yearCount = await TakeProductsList("DSClassic1year")
    if DSClassic1yearCount == []:
        DSClassic1yearCount = 0
    else: 
        DSClassic1monthCount = len(DSClassic1monthCount)
    if str(call.from_user.id) not in userlist:
        await InsertNewUser(call.from_user.username, call.from_user.id)
        await bot.send_message(call.from_user.id, "📌Выберите товар📌", reply_markup = InlineKeyboardMarkup(row_width = 1)\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 месяц | 300₽ | Кол-во: {DSNitro1monthCount}",
                                      callback_data = "DSNitro1month 300"))\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 год | 2000₽ | Кол-во: {DSNitro1yearCount}",
                                      callback_data= "DSNitro1year 2000"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 месяц | 150₽ | Кол-во: {DSClassic1monthCount}",
                                      callback_data = "DSClassic1month 150"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 год | 1000₽ | Кол-во: {DSClassic1yearCount}",
                                      callback_data = "DSClassic1year 1000")))
    else:
        await bot.send_message(call.from_user.id, "📌Выберите товар📌", reply_markup = InlineKeyboardMarkup(row_width = 1)\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 месяц | 300₽ | Кол-во: {DSNitro1monthCount}",
                                      callback_data = "DSNitro1month 300"))\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 год | 2000₽ | Кол-во: {DSNitro1yearCount}",
                                      callback_data= "DSNitro1year 2000"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 месяц | 150₽ | Кол-во: {DSClassic1monthCount}",
                                      callback_data = "DSClassic1month 150"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 год | 1000₽ | Кол-во: {DSClassic1yearCount}",
                                      callback_data = "DSClassic1year 1000")))
async def BuyingProduct1(call):
    userlist = await get_users_id()
    DSNitro1monthCount = await TakeProductsList("DSNitro1month")
    if DSNitro1monthCount == []:
        DSNitro1monthCount = 0
    else: 
        DSNitro1monthCount = len(DSNitro1monthCount)
    DSNitro1yearCount = await TakeProductsList("DSNitro1year")
    if DSNitro1yearCount == []:
        DSNitro1yearCount = 0
    else: 
        DSNitro1yearCount = len(DSNitro1yearCount)
    DSClassic1monthCount = await TakeProductsList("DSClassic1month")
    if DSClassic1monthCount == []:
        DSClassic1monthCount = 0
    else: 
        DSClassic1monthCount = len(DSClassic1monthCount)
    DSClassic1yearCount = await TakeProductsList("DSClassic1year")
    if DSClassic1yearCount == []:
        DSClassic1yearCount = 0
    else: 
        DSClassic1monthCount = len(DSClassic1monthCount)
    if str(call.from_user.id) not in userlist:
        await InsertNewUser(call.from_user.username, call.from_user.id)
        await bot.send_message(call.from_user.id, "📌Выберите товар📌", reply_markup = InlineKeyboardMarkup(row_width = 1)\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 месяц | 300₽ | Кол-во: {DSNitro1monthCount}",
                                      callback_data = "DSNitro1month 300"))\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 год | 2000₽ | Кол-во: {DSNitro1yearCount}",
                                      callback_data= "DSNitro1year 2000"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 месяц | 150₽ | Кол-во: {DSClassic1monthCount}",
                                      callback_data = "DSClassic1month 150"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 год | 1000₽ | Кол-во: {DSClassic1yearCount}",
                                      callback_data = "DSClassic1year 1000")))
    else:
        await bot.send_message(call.from_user.id, "📌Выберите товар📌", reply_markup = InlineKeyboardMarkup(row_width = 1)\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 месяц | 300₽ | Кол-во: {DSNitro1monthCount}",
                                      callback_data = "DSNitro1month 300"))\
            .add(InlineKeyboardButton(text = f"Discord Nitro | 1 год | 2000₽ | Кол-во: {DSNitro1yearCount}",
                                      callback_data= "DSNitro1year 2000"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 месяц | 150₽ | Кол-во: {DSClassic1monthCount}",
                                      callback_data = "DSClassic1month 150"))\
            .add(InlineKeyboardButton(text = f"Discord Classic | 1 год | 1000₽ | Кол-во: {DSClassic1yearCount}",
                                      callback_data = "DSClassic1year 1000")))
async def Nitro1month(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    ProductType = call.data.split(" ")[0]
    Product = "Discord Nitro 1 месяц"
    count = await TakeProductsList(ProductType)
    ID = call.from_user.id
    price = call.data.split(" ")[1]
    if len(count) > 0:
        photo = open("nitro.png", "rb")
        await bot.send_photo(call.from_user.id, photo, f"{Product}\n💵Стоимость: {price}₽\n🗂Подписка даёт пользователям следующие преимущества:\n\n📌Установка анимированного GIF-аватара.\n📌Возможность использования анимированных эмодзи.\n📌Возможность использовать эмодзи с серверов в личной переписке.\n📌Максимальный размер загрузок изменен с 8 Мб на 100 Мб.\n📌Возможность демонстрации экрана в 720p 60fps или 1080p 30fps.\n📌Значок Discord Nitro badge в профиле.\n📌Возможность смены вашего уникального ID пользователя.\n📌2 Буста сервера, чтобы дать любимому серверу эксклюзивные бонусы и крутой значок.\n📌Специальный значок в профиля, показывающий всем, что вы поддерживаете Discord.", reply_markup = InlineKeyboardMarkup(row_width = 1).add(
            InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}"), 
            InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}"),
            InlineKeyboardButton(text = "Назад", callback_data = f"BuyingBack")))
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, "В данный момент товара нет в наличии")
        await call.answer()
async def Nitro1year(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    ProductType = call.data.split(" ")[0]
    Product = "Discord Nitro 1 год"
    count = await TakeProductsList(ProductType)
    ID = call.from_user.id
    price = call.data.split(" ")[1]
    if len(count) > 0:
        photo = open("nitro.png", "rb")
        await bot.send_photo(call.from_user.id, photo, f"{Product}\n💵Стоимость: {price}₽\n🗂Подписка даёт пользователям следующие преимущества:\n\n📌Установка анимированного GIF-аватара.\n📌Возможность использования анимированных эмодзи.\n📌Возможность использовать эмодзи с серверов в личной переписке.\n📌Максимальный размер загрузок изменен с 8 Мб на 100 Мб.\n📌Возможность демонстрации экрана в 720p 60fps или 1080p 30fps.\n📌Значок Discord Nitro badge в профиле.\n📌Возможность смены вашего уникального ID пользователя.\n📌2 Буста сервера, чтобы дать любимому серверу эксклюзивные бонусы и крутой значок.\n📌Специальный значок в профиля, показывающий всем, что вы поддерживаете Discord.", reply_markup = InlineKeyboardMarkup(row_width = 1).add(
            InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}"), 
            InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}"),
            InlineKeyboardButton(text = "Назад", callback_data = f"BuyingBack")))
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, "В данный момент товара нет в наличии")
        await call.answer()
async def Classic1month(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    ProductType = call.data.split(" ")[0]
    Product = "Discord Classic 1 месяц"
    count = await TakeProductsList(ProductType)
    ID = call.from_user.id
    price = call.data.split(" ")[1]
    if len(count) > 0:
        photo = open("classic.png", "rb")
        await bot.send_photo(call.from_user.id, photo, f"{Product}\n💵Стоимость: {price}₽\n🗂Nitro Classic даст вам следующие бонусы:\n\n📌Загружайте Gif-аватар. Nitro Classic позволит вам добавить в свой профиль немного анимированной годноты. Превратите свой аватар в крутую “гифку”, и он проявит свою магию в текстовых каналах и на серверах Ваших друзей.\n📌Выбирайте свой собственный Тег. Примечание: с окончанием действия подписки он будет изменен на случайный.\n📌Используйте пользовательские эмодзи где угодно. Обычно, пользовательские эмодзи можно использовать только на сервере, на который они загружены (за редким исключением).\n📌Видео более высокого качества. Прокачайте свои параметры для демонстрации экрана до  720p @ 60fps, или 1080p @ 30fps. Также, качество стримов улучшается до 1080p @ 60fps при активации Go Live!\n📌Увеличьте размер загружаемого файла с 8 до 50 Мб.\n📌Бонус. Вы также получите милый значок Nitro, которым можно покрасоваться в своем профиле. Статус крутого пользователя!", reply_markup = InlineKeyboardMarkup(row_width = 1).add(
            InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}"), 
            InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}"),
            InlineKeyboardButton(text = "Назад", callback_data = f"BuyingBack")))
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, "В данный момент товара нет в наличии")
        await call.answer()
async def Classic1year(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    ProductType = call.data.split(" ")[0]
    Product = "Discord Classic 1 год"
    count = await TakeProductsList(ProductType)
    ID = call.from_user.id
    price = call.data.split(" ")[1]
    if len(count) > 0:
        photo = open("classic.png", "rb")
        await bot.send_photo(call.from_user.id, photo, f"{Product}\n💵Стоимость: {price}₽\n🗂Nitro Classic даст вам следующие бонусы:\n\n📌Загружайте Gif-аватар. Nitro Classic позволит вам добавить в свой профиль немного анимированной годноты. Превратите свой аватар в крутую “гифку”, и он проявит свою магию в текстовых каналах и на серверах Ваших друзей.\n📌Выбирайте свой собственный Тег. Примечание: с окончанием действия подписки он будет изменен на случайный.\n📌Используйте пользовательские эмодзи где угодно. Обычно, пользовательские эмодзи можно использовать только на сервере, на который они загружены (за редким исключением).\n📌Видео более высокого качества. Прокачайте свои параметры для демонстрации экрана до  720p @ 60fps, или 1080p @ 30fps. Также, качество стримов улучшается до 1080p @ 60fps при активации Go Live!\n📌Увеличьте размер загружаемого файла с 8 до 50 Мб.\n📌Бонус. Вы также получите милый значок Nitro, которым можно покрасоваться в своем профиле. Статус крутого пользователя!", reply_markup = InlineKeyboardMarkup(row_width = 1).add(
            InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}"), 
            InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}"),
            InlineKeyboardButton(text = "Назад", callback_data = f"BuyingBack")))
        await call.answer()
    else:
        await bot.send_message(call.from_user.id, "В данный момент товара нет в наличии")
        await call.answer()

async def balancebuying(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    data = call.data.replace("BB ", "").split(" ")
    ProductType = data[0]
    if ProductType == "DSNitro1month":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            cost = 300
            ID = call.from_user.id
            username = call.from_user.username
            if await BuyerBalanceCheck(call.from_user.id, cost) == True:
                ProductKey = await buying_product(ID, username, ProductType)
                await BuyerBalanceUpdate(call.from_user.id, cost)
                await bot.send_message(call.from_user.id, f"Вот твой ключ {ProductKey} он стоил {cost}₽\nБудет очень круто если ты оставишь здесь отзыв: ")
                await call.answer("Товар куплен")
            else:
                await bot.send_message(call.from_user.id, "Недостаточно средств на балансе") 
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSNitro1year":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            cost = 2000
            ID = call.from_user.id
            username = call.from_user.username
            if await BuyerBalanceCheck(call.from_user.id, cost) == True:
                await BuyerBalanceUpdate(call.from_user.id, cost)
                ProductKey = await buying_product(ID, username, ProductType)
                await bot.send_message(call.from_user.id, f"Вот твой ключ {ProductKey} он стоил {cost}₽\nБудет очень круто если ты оставишь здесь отзыв: h")
                await call.answer("Товар куплен")
            else:
                await bot.send_message(call.from_user.id, "Недостаточно средств на балансе")
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSClassic1month":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            cost = 150
            ID = call.from_user.id
            username = call.from_user.username
            if await BuyerBalanceCheck(call.from_user.id, cost) == True:
                await BuyerBalanceUpdate(call.from_user.id, cost)
                ProductKey = await buying_product(ID, username, ProductType)
                ProductKey = ProductKey
                await bot.send_message(call.from_user.id, f"Вот твой ключ {ProductKey} он стоил {cost}₽\nБудет очень круто если ты оставишь здесь отзыв: ")
                await call.answer("Товар куплен")
            else:
                await bot.send_message(call.from_user.id, "Недостаточно средств на балансе")
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSClassic1year":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            cost = 1000
            ID = call.from_user.id
            username = call.from_user.username
            if await BuyerBalanceCheck(call.from_user.id, cost) == True:
                await BuyerBalanceUpdate(call.from_user.id, cost)
                ProductKey = await buying_product(ID, username, ProductType)
                ProductKey = ProductKey
                await bot.send_message(call.from_user.id, f"Вот твой ключ {ProductKey} он стоил {cost}₽\nБудет очень круто если ты оставишь здесь отзыв: ")
                await call.answer("Товар куплен")
            else:
                await bot.send_message(call.from_user.id, "Недостаточно средств на балансе")
        else:
            await call.answer("Товар закончился")
async def directbuying(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
    data = call.data.replace("DB ", "").split(" ")
    ProductType = data[0]
    ID = data[1]
    NewPaymentID = await TakeNewPaymentID()
    if ProductType == "DSNitro1month":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            amount = 300
            bill = await QiwiCreateTopUpInvoice(ID, amount, NewPaymentID)
            bill_id = bill.bill_id
            url = bill.pay_url
            await bot.send_message(call.from_user.id, f"Покупка Discord Nitro на 1  месяц от пользователя {ID}\nВремя на оплату 10 минут",
                                   reply_markup = DirectPayCheckingButton(url, amount, bill_id, ProductType, NewPaymentID))
            await call.answer()
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSNitro1year":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            amount = 2000
            bill = await QiwiCreateTopUpInvoice(ID, amount, NewPaymentID)
            url = bill.pay_url
            bill_id = bill.bill_id
            await bot.send_message(call.from_user.id, f"Покупка Discord Nitro на 1  месяц от пользователя {ID}\nВремя на оплату 10 минут",
                                   reply_markup = DirectPayCheckingButton(url, amount, bill_id, ProductType, NewPaymentID))
            await call.answer()
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSClassic1month":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            amount = 150
            bill = await QiwiCreateTopUpInvoice(ID, amount, NewPaymentID)
            url = bill.pay_url
            bill_id = bill.bill_id
            await bot.send_message(call.from_user.id, f"Покупка Discord Nitro на 1  месяц от пользователя {ID}\nВремя на оплату 10 минут",
                                   reply_markup = DirectPayCheckingButton(url, amount, bill_id, ProductType, NewPaymentID))
            await call.answer()
        else:
            await call.answer("Товар закончился")
    if ProductType == "DSClassic1year":
        count = await TakeProductsList(ProductType)
        if len(count) > 0:
            amount = 1000
            bill = await QiwiCreateTopUpInvoice(ID, amount, NewPaymentID)
            bill_id = bill.bill_id
            url = bill.pay_url
            await bot.send_message(call.from_user.id, f"Покупка Discord Nitro на 1  месяц от пользователя {ID}\nВремя на оплату 10 минут",
                                   reply_markup = DirectPayCheckingButton(url, amount, bill_id, ProductType, NewPaymentID))
            await call.answer()
        else:
            await call.answer("Товар закончился")
async def DirectPaymentCheck(call: types.CallbackQuery):
    data = call.data.replace("DP ", "").split(" ")
    bill_id = data[0]
    ID = call.from_user.id
    username = call.from_user.username
    amount = data[1]
    ProductType = data[2]
    NewPaymentID = data[3]
    if str(qiwi.check(bill_id = bill_id).status) == "PAID":
        await bot.delete_message(call.from_user.id, message_id= call.message.message_id)
        admins = await take_admins_id()
        if ID in admins:
            await call.answer("Счёт оплачен")
            ProductKey = await buying_product(ID, username, ProductType)
            await InsertingBillInformation(NewPaymentID, ID, username, amount, bill_id)
            await bot.send_message(ID, f"Вот твой ключ {ProductKey} он стоил {amount}₽\nБудет очень круто если ты оставишь здесь отзыв: ", reply_markup = UpgradedButtons)
        else:
            await call.answer("Счёт оплачен")
            ProductKey = await buying_product(ID, username, ProductType)
            await InsertingBillInformation(NewPaymentID, ID, username, amount, bill_id)
            await bot.send_message(ID, f"Вот твой ключ {ProductKey} он стоил {amount}₽\nБудет очень круто если ты оставишь здесь отзыв: ", reply_markup = MainButtons)
    else:
        await call.answer("Счёт не оплачен")
async def DirectPaymentCancel(call: types.CallbackQuery):
    data = call.data.replace("DDP ", "").split(" ")
    bill_id = data[0]
    ID = call.from_user.id
    username = call.from_user.username
    amount = data[1]
    ProductType = data[2]
    admins = await take_admins_id()
    await call.answer()
    if call.from_user.id in admins:
        await bot.send_message(call.from_user.id, "Оплата отменена.", reply_markup = UpgradedButtons)
        await BuyingProduct1(call)
    else:
        await bot.send_message(call.from_user.id, "Оплата отменена.", reply_markup = MainButtons)
        await BuyingProduct1(call)
async def GetSupport(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    username = message.from_user.username
    userlist = await get_users_id()
    if str(message.from_user.id) not in userlist:
        await InsertNewUser(username, message.from_user.id)
        await bot.send_message(message.from_user.id, "По всем вопросом обращайтесь к\n")
    else:
        await bot.send_message(message.from_user.id, "По всем вопросом обращайтесь к\n")
async def rules(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    await bot.send_message(message.from_user.id,\
"📔 Правила перед покупкой и после покупки.\n\
➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
💵 | Манибек не производим, исключительно замена.\n\
🔒 | Гарантия замены 2 недели после покупки оригинала(после замены отсчёт не обнуляется)\n\
☕ | Чтобы получить замену, Вы должны предоставить видео-доказательство своей покупки по форме(указана при нажатии на кнопку меню)\n\
➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\
⛔ | Оскорбления в любых формах, попытка обмана или фейк-чеков, фейк-видео караются добавлением в чёрный список у Администратора")
async def others(message: types.Message):
    await bot.delete_message(message.from_user.id, message_id = message.message_id)
    msg = await bot.send_message(message.from_user.id, "Я не знаю что ответить")
    #await msgdelete(msg, message.from_user.id)
async def whoknows(message: types.Message):
    await bot.send_message(message.from_user.id, "Спроси у админа, может поможет\n@deadghouI")
#async def msgdelete(msg, chatid):
#    await asyncio.sleep(2)
#    await bot.delete_message(chatid, message_id = msg.message_id)
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(startcommand, commands = ['start'])
    dp.register_message_handler(CheckMyProfile, commands = ['Профиль'])
    dp.register_message_handler(CheckMyProfile, Text(equals = '📝Мой профиль'))
    dp.register_message_handler(TermsConfirmation, commands = ['Меню'])
    dp.register_message_handler(TermsConfirmation, Text(equals = "🛒Меню"))
    dp.register_message_handler(TermsConfirmation, Text(equals = "🛒Меню бота"))
    dp.register_message_handler(TermsConfirmation, Text(equals = "🛒Купить"))
    dp.register_callback_query_handler(BuyingProduct, text = "TC Yes")
    dp.register_callback_query_handler(BuyingProduct, text = "BuyingBack")
    dp.register_callback_query_handler(TermsCanceling, text = "TC No")
    dp.register_message_handler(GetSupport, commands = ["support"])
    dp.register_message_handler(GetSupport, Text(equals = "❓Поддержка❓"))
    dp.register_message_handler(reviews, commands = ["Отзывы"])
    dp.register_message_handler(reviews, Text(equals = "📩Отзывы"))
    dp.register_message_handler(NewAdmin, commands = ['Seutyf3fFY1Tft4ue5wvYtNzYhe313FbGtes1fgEhHrtFh'])
    dp.register_message_handler(CancelHandler, commands = ["Отмена"], state = "BalanceTopUpCount:amount")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена"), state = "BalanceTopUpCount:amount")
    dp.register_callback_query_handler(Nitro1month, lambda x: x.data and x.data.startswith("DSNitro1month "))
    dp.register_callback_query_handler(Nitro1year, lambda x: x.data and x.data.startswith("DSNitro1year "))
    dp.register_callback_query_handler(Classic1month, lambda x: x.data and x.data.startswith("DSClassic1month "))
    dp.register_callback_query_handler(Classic1year, lambda x: x.data and x.data.startswith("DSClassic1year "))
    dp.register_callback_query_handler(top_up_start, lambda x: x.data and x.data.startswith("TopUp "), state = None)
    dp.register_message_handler(GetTopUpAmount, state = BalanceTopUpCount.amount)
    dp.register_callback_query_handler(CheckPaymentStatus, lambda x: x.data and x.data.startswith("Payment "))
    dp.register_callback_query_handler(CancelPayment, lambda x: x.data and x.data.startswith("DelPayment "))
    dp.register_callback_query_handler(DirectPaymentCheck, lambda x: x.data and x.data.startswith("DP "))
    dp.register_callback_query_handler(DirectPaymentCancel, lambda x: x.data and x.data.startswith("DDP "))
    dp.register_callback_query_handler(directbuying, lambda x: x.data and x.data.startswith("DB "))
    dp.register_callback_query_handler(balancebuying, lambda x: x.data and x.data.startswith("BB "))
    dp.register_message_handler(rules, commands = ["terms"])
    dp.register_message_handler(rules, Text(equals = "©Правила покупки"))
    dp.register_message_handler(whoknows, commands = ["а_кто_знает"])
    dp.register_message_handler(whoknows, Text(equals = "а кто знает", ignore_case = True))
    dp.register_message_handler(others)
