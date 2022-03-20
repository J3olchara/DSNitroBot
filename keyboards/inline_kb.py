from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
def ProductBuying_kb(ProductType, ID):
    directbuying = InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}")
    balancebuying = InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}")
    buying_kb = InlineKeyboardMarkup(row_width = 1).add(
        InlineKeyboardButton(text = "Купить прямой оплатой", callback_data = f"DB {ProductType} {ID}"), 
        InlineKeyboardButton(text = "Купить с баланса", callback_data = f"BB {ProductType} {ID}"))
    return buying_kb

def InlineBalanceTopUp(ID):
    return InlineKeyboardMarkup(row_width = 2).\
    row(InlineKeyboardButton(text ='50₽', callback_data = f"TopUp {ID} 50"), \
    InlineKeyboardButton(text = '100₽', callback_data = f"TopUp {ID} 100"))\
    .row( InlineKeyboardButton(text = '300₽', callback_data = f"TopUp {ID} 300"), \
    InlineKeyboardButton(text = '500₽', callback_data = f"TopUp {ID} 500"))


