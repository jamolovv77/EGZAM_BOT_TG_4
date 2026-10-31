from aiogram.types import *



main_key = ReplyKeyboardMarkup(

    keyboard=[
        [KeyboardButton(text="kаталог 🛍"),  KeyboardButton(text="xаридҳои ман 🧾")],
        [KeyboardButton(text="➕ илова кардани маxсулот"), KeyboardButton(text="❓ kумак")]


    ],
    resize_keyboard=True
)






def get_product_buttons(product_id, stock):
    keyboards = [
        [InlineKeyboardButton(
            text="Подробнее",callback_data=f"product_info_{product_id}")]
    ]




    if stock >0:
        keyboards.append([InlineKeyboardButton(
            text=" kупить 1 шт 🛒",
            callback_data=f"buy_{product_id}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboards)