from aiogram.types import *


categories =[
    ("📱","fhone"),("👕","clothes"),
    ("🍎","dishes"),("🏠","house"),
            ("🚗","cars"),

]


main_key = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛍 Каталог"), KeyboardButton(text="📦 Маҳсулотҳои ман")],
        [KeyboardButton(text="🧾 Харидҳои ман"), KeyboardButton(text="➕ Илова кардани маҳсулот")],
        [KeyboardButton(text="❓ Кумак")]
    ],
    resize_keyboard=True
)


def get_category_buttons():
    keyboards = []

    for i in range( len(categories)):
        row = []
        for j in range(i, min(i+1, len(categories))):
            emoji, name = categories[j]
            row.append(InlineKeyboardButton(
                text=f"{emoji} {name}",
                callback_data=f"cat_{j}"
            ))
        keyboards.append(row)

    return InlineKeyboardMarkup(inline_keyboard=keyboards)


def get_product_buttons(product_id, stock):
    keyboards = [
        [InlineKeyboardButton(
            text="Подробнее",
            callback_data=f"product_info_{product_id}"
        )]
    ]

    if stock >0:
        keyboards.append([InlineKeyboardButton(
            text="🛒 Купить 1 шт.",
            callback_data=f"buy_{product_id}"
        )])

    return InlineKeyboardMarkup(inline_keyboard=keyboards)