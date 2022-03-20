from aiogram.utils import executor
from bot_body import bot, dp
import bot_body
from database.userlistDB import SafeShutdown_users, startdb_users
from database.adminDB import SafeShutdown_admins, startdb_admins
from database.ProductsDB import SafeShutdown_products, startdb_products
from database.receiptsDB import SafeShutdown_receipts, startdb_receipts
from handlers import admin, client
import os

async def on_startup(dp):
    await bot.set_webhook(bot_body.BOT_URL)
    startdb_users()
    startdb_admins()
    startdb_products()
    startdb_receipts()
    print("-------------------------------BOT IS ONLINE-------------------------------\n")


async def on_shutdown(dp):
    await SafeShutdown_admins()
    await SafeShutdown_products()
    await SafeShutdown_users()
    await SafeShutdown_receipts()
    print("-------------------------------BOT IS OFFLINE-------------------------------")
    await bot.delete_webhook()

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)

#executor.start_polling(dp,
#                       skip_updates = True,
#                       on_startup = on_startup,
#                       on_shutdown = on_shutdown)
executor.start_webhook(dispatcher = dp, 
                       skip_updates = True, on_startup=on_startup, 
                       on_shutdown=on_shutdown, 
                       webhook_path = '', 
                       host = "0.0.0.0",
                       port = int(os.environ.get("PORT", 5000)))