from yookassa import Payment, Configuration
from bot_body import bot, YandexKey, YandexShopId, QiwiPublicKey, QiwiSecretKey
from database.receiptsDB import InsertingBillInformation
import uuid
from pyqiwip2p import QiwiP2P
qiwi = QiwiP2P(auth_key = QiwiSecretKey)
async def YandexCreateTopUpInvoice(ID, amount, payload):
    payamount =  str(amount) +".00"
    Configuration.account_id = YandexShopId
    Configuration.secret_key = YandexKey
    payment = Payment.create({
        "amount":{
            "value": payamount, 
            "currency": "RUB"
            }, 
        "payment_method_data": {
            "type": "yoo_money"
            },
        "confirmation": {
            "type": "rediect", 
            "return_url": ""
            },
        "capture": True, 
        "descritption": f"Пополнение пользователя с telegramID:{ID} на {payamount}"
        })
    print("________________________________", type(payment))
    print(payment)
    url = payment.confirmation.confirmation_url
    return url
async def TGCreateTopUpInvoice(ID, amount, payload):
    amount = int(str(amount) + "00")
    YOOTOKEN = ""
    await bot.send_invoice(ID, 
                           title = "Пополнение баланса", 
                           description = f"Пополнение баланса пользователя {ID} в боте ",
                           payload = payload,
                           provider_token = YOOTOKEN, 
                           currency = "RUB", 
                           start_parameter = "test", 
                           prices = [{"label": "Руб", "amount":amount}])

async def QiwiCreateTopUpInvoice(ID, amount, NewPaymentID):
    description = f"Пополнение баланса пользователя {ID} в магазине  #{NewPaymentID}"
    bill = qiwi.bill(amount = amount, lifetime = 10, comment = description)
    return bill