from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from bot_body import bot, dp
from keyboards.admin_kb import AdminButtons, UpgradedButtons
from database.userlistDB import InsertBalance, get_users_id, ProfileData
from database.adminDB import take_admins_id
from database.ProductsDB import InsertProducts, TakeProductsList, AllProductList
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

async def AdminMode(message: types.Message):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, "Вход в админ панель", reply_markup = AdminButtons)
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def back_to_clientmode(message: types.Message):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        await bot.send_message(message.from_user.id, "Возврат в клиентский режим", reply_markup = UpgradedButtons)
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")

class GivingBalance(StatesGroup):
    currentuser = State()
    moneyamount = State()
async def BalanceGiving_Start(message: types.Message):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        await GivingBalance.currentuser.set()
        await bot.send_message(message.from_user.id, "Внесите telegramid пользователя")
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def TakeUserID(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    userlist = await get_users_id()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            try:
                if str(message.text) in userlist:
                    data["currentuser"] = message.text
                    await GivingBalance.next()
                    await bot.send_message(message.from_user.id, text = "На сколько увеличить/изменить баланс?")
                else:
                    await message.answer("Такого пользователя нет в БД бота")
                    await BalanceGiving_Start(message)
            except:
                await message.answer("Это не telegramID")
                await BalanceGiving_Start(message)
        
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def ChangeBalance(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            data["moneyamount"] = int(message.text)
        currentuser = list(data.values())[0]
        moneyamount = int(list(data.values())[1])
        await InsertBalance(currentuser, moneyamount)
        userdata = await ProfileData(currentuser)
        username = userdata[0]
        balance = userdata[2]
        await bot.send_message(message.from_user.id, f"Баланс пользователя {currentuser} с ником @{username} изменён на {moneyamount}₽. Теперь его баланс {balance}")
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")

class InsertingProducts(StatesGroup):
    ProductType = State()
    supplier = State()
    Products = State()
async def InsertingProducts_start(message: types.Message):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        await InsertingProducts.ProductType.set()
        await bot.send_message(message.from_user.id, "Введите тип товара (Nitro/Classic)")
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def EnterProductType(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        try:
            if "Nitro" in message.text.capitalize():
                async with state.proxy() as data:
                    data["ProductType"] = "DSNitro1month"
                await InsertingProducts.next()
                await bot.send_message(message.from_user.id, "Введите имя поставщика\n username\\telegram ID")
            if "Classic" in message.text.capitalize():
                async with state.proxy() as data:
                    data["ProductType"] = "DSClassic1month"
                await InsertingProducts.next()
                await bot.send_message(message.from_user.id, "Введите имя поставщика\n username\\telegram ID")
            elif "Classic" not in message.text.capitalize() and "Nitro" not in message.text.capitalize():
                await bot.send_message(message.from_user.id, "Это не тип подписки")
                await InsertingProducts_start(message)
        except:
            await bot.send_message(message.from_user.id, "Нужно ввести либо nitro либо classic")
            await InsertingProducts_start(message)
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def EnterSupplier(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            data["supplier"] = message.text
        await InsertingProducts.next()
        await bot.send_message(message.from_user.id, "Введите товар разделяя пробелом каждый ключ")
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def EnterProducts(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            data["products"] = message.text.split(" ")
        supplier = data.get("supplier")
        ProductType = data.get("ProductType")
        Products = data.get("products")
        NewProducts = []
        NotInserted = []
        for Product in Products:
            ProductList = await AllProductList(ProductType)
            if Product == " " or Product == "":
                continue
            if Product not in ProductList:
                DuplicatedKeys = await InsertProducts(supplier, Product, ProductType)
                NewProducts.append(Product)
            else:
                await bot.send_message(message.from_user.id, f"Ключ {Product} уже есть в базе данных")
                NotInserted.append(Product)
        await state.finish()
        newcount = await TakeProductsList(ProductType)
        await bot.send_message(message.from_user.id, f"Внесено {len(NewProducts)} товаров, не внесены {len(NotInserted)} товаров из предоставленных.\nТеперь пользователям доступно {len(newcount)} товаров типа {ProductType}")
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def CancelHandler(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        currentstate = await state.get_state()
        if currentstate == None:
            return
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, "Действие отменено", reply_markup = UpgradedButtons)
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")

class SendMessage(StatesGroup):
    message = State()
    confirmation = State()
async def SendMessage_Start(message: types.Message):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        await SendMessage.message.set()
        await bot.send_message(message.from_user.id, "Напишите сообщение которое будет отправлено всем пользователям")
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")

async def GetMessageForSending(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    if message.from_user.id in admins:
        async with state.proxy() as data:
            data["msg"] = message.text
        await SendMessage.next()
        await bot.send_message(message.from_user.id, "Вы уверены что хотите отправить это сообщение всем пользователям?",
                               reply_markup = ReplyKeyboardMarkup(resize_keyboard = True)
                               .add(KeyboardButton("Да"), KeyboardButton("Нет")).add(KeyboardButton("Отмена")))
    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
async def GetMessageConfirmation(message: types.Message, state: FSMContext):
    admins = await take_admins_id()
    userlist = await get_users_id()
    if message.from_user.id in admins:
        confirmation = message.text
        if confirmation == "Да":
            async with state.proxy() as data:
                msg = data.get("msg")
            sending = await bot.send_message(message.from_user.id, "Сообщение отправляется.....", reply_markup = AdminButtons)
            for user in userlist:
                if str(message.from_user.id) != user:
                    try:
                        await bot.send_message(user, msg)
                    except:
                        pass
                else:
                    pass
            await bot.delete_message(message.from_user.id, message_id = sending.message_id)
            await bot.send_message(message.from_user.id, "Сообщение отправлено всем пользователям", reply_markup = AdminButtons)
            await state.finish()
        if confirmation == "Нет":
            await bot.send_message(message.from_user.id, "Отправка сообщения отменена", reply_markup = AdminButtons)
            await state.finish()

    else:
        await bot.send_message(message.from_user.id, "Я не знаю что ответить")
        await state.finish()
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(AdminMode, commands = ["Admin"])
    dp.register_message_handler(AdminMode, Text(equals = "Админ панель"))
    dp.register_message_handler(BalanceGiving_Start, commands = ["Изменить_баланс_пользователя"], state = None)
    dp.register_message_handler(BalanceGiving_Start, Text(equals = "Изменить баланс пользьзователя"))
    dp.register_message_handler(CancelHandler, commands = ["Отмена"])
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "GivingBalance:currentuser")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "GivingBalance:moneyamount")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "InsertingProducts:ProductType")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "InsertingProducts:supplier")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "InsertingProducts:Products")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "SendMessage:message")
    dp.register_message_handler(CancelHandler, Text(equals = "Отмена", ignore_case = True), state = "SendMessage:confirmation")
    dp.register_message_handler(SendMessage_Start, commands = ["Написать_всем_пользователям"], state = None)
    dp.register_message_handler(SendMessage_Start, Text(equals = "Написать всем пользователям", ignore_case = True), state = None)
    dp.register_message_handler(GetMessageForSending, state = SendMessage.message)
    dp.register_message_handler(GetMessageConfirmation, state = SendMessage.confirmation)
    dp.register_message_handler(TakeUserID, state = GivingBalance.currentuser)
    dp.register_message_handler(ChangeBalance, state = GivingBalance.moneyamount)
    dp.register_message_handler(InsertingProducts_start, commands = ["Внести_товар"], state = None)
    dp.register_message_handler(InsertingProducts_start, Text(equals = "Внести товар"))
    dp.register_message_handler(EnterProductType, state = InsertingProducts.ProductType)
    dp.register_message_handler(EnterSupplier, state = InsertingProducts.supplier)
    dp.register_message_handler(EnterProducts, state = InsertingProducts.Products)
    dp.register_message_handler(back_to_clientmode, commands = ["Clientmode"])
    dp.register_message_handler(back_to_clientmode, Text(equals = "Клиентский режим"))













