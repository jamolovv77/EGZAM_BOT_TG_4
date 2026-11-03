from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from service import *
from keyboards import *


router = Router()


def product_text(product):
    text = (
        f"🆔 ID: {product['id']}\n"
        f"📱 {product['title']}\n"
        f"📂 Категория: {product['category']}\n"
        f"💵 Нарх: {product['price']} сомонӣ\n"
        f"📦 Миқдор: {product['stock']} дона"
    )
    return text


async def send_product(message, product):
    await message.answer_photo(
        photo=product['photo_file_id'],
        caption=product_text(product),
        reply_markup=get_product_buttons(product['id'], product['stock'])
    )


@router.message(F.text == "🛍 Каталог")
@router.message(Command("catalog"))
async def show_catalog(message: Message):
    products = await get_all_products()

    if not products:
        await message.answer("😔 Ҳоло ягон маҳсулот нест.")
        return

    for product in products:
        if product['owner_id'] == message.from_user.id:
            await message.answer_photo(
                photo=product['photo_file_id'],
                caption=product_text(product) + "\n\n👤 Ин маҳсулоти шумост"
            )
        else:
            await send_product(message, product)


@router.message(F.text == "📦 Маҳсулотҳои ман")
@router.message(Command("my_products"))
async def show_my_products(message: Message):
    products = await get_my_products(message.from_user.id)

    if not products:
        await message.answer(
            "😔 Шумо ҳоло маҳсулот илова накардаед.\n"
            "➕ Тугмаи «Илова кардани маҳсулот»-ро пахш кунед."
        )
        return

    for product in products:
        count = await get_sales_count(product['id'])
        await message.answer_photo(
            photo=product['photo_file_id'],
            caption=product_text(product) + f"\n📊 Фурӯхта шуд: {count} дона"
        )


@router.message(Command("product"))
async def show_product(message: Message, command: CommandObject):
    if not command.args or not command.args.isdigit():
        await message.answer("❗ Истифода: /product 5")
        return

    product = await get_product(int(command.args))

    if not product:
        await message.answer("😔 Маҳсулот ёфт нашуд!")
        return

    await send_product(message, product)


@router.message(F.text == "🧾 Харидҳои ман")
@router.message(Command("my_orders"))
async def show_my_orders(message: Message):
    orders = await get_user_orders(message.from_user.id)

    if not orders:
        await message.answer("😔 Шумо ҳоло ягон чиз нахаридаед.")
        return

    text = "🧾 Харидҳои шумо:\n\n"

    for order in orders:
        text += (
            f"🆔 {order['product_id']} 📱 {order['title']} - "
            f"💵 {order['purchase_price']} сомонӣ - "
            f"📅 {order['purchased_at'].strftime('%d.%m.%Y')}\n"
        )

    await message.answer(text)


@router.message(Command("sales"))
async def show_sales(message: Message, command: CommandObject):
    if not command.args or not command.args.isdigit():
        await message.answer("❗ Истифода: /sales 5")
        return

    product = await get_product(int(command.args))

    if not product:
        await message.answer("😔 Маҳсулот ёфт нашуд!")
        return

    if product['owner_id'] != message.from_user.id:
        await message.answer("🚫 Ин маҳсулот аз они шумо нест!")
        return

    count = await get_sales_count(product['id'])
    await message.answer(f"📊 {product['title']} — {count} дона фурӯхта шуд")


@router.message(Command("spending"))
async def show_spending(message: Message):
    total = await get_user_spending(message.from_user.id)
    await message.answer(f"💰 Шумо дар маҷмӯъ {total} сомонӣ сарф кардаед.")


@router.callback_query(F.data.startswith("product_info_"))
async def product_info(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])
    product = await get_product(product_id)

    if not product:
        await callback.answer("😔 Маҳсулот ёфт нашуд!", show_alert=True)
        return

    if product['stock'] > 0:
        status = "Мавҷуд аст ✅"
    else:
        status = "Тамом шудааст ❌"

    await callback.message.answer(
        f"{product_text(product)}\n"
        f"📌 Ҳолат: {status}"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("buy_"))
async def buy(callback: CallbackQuery):
    product_id = int(callback.data.split("_")[-1])
    status, product = await buy_product(product_id, callback.from_user.id)

    if status == "not_found":
        await callback.answer("😔 Маҳсулот ёфт нашуд!", show_alert=True)

    elif status == "own_product":
        await callback.answer("🚫 Шумо маҳсулоти худатонро харида наметавонед!", show_alert=True)

    elif status == "out_of_stock":
        await callback.answer("❌ Маҳсулот тамом шудааст!", show_alert=True)
        await update_card(callback, product)

    elif status == "ok":
        await callback.answer("✅ Харид анҷом ёфт! 🎉", show_alert=True)
        await update_card(callback, product)

    else:
        await callback.answer("❌ Хатогӣ ҳангоми харид!", show_alert=True)


async def update_card(callback, product):
    try:
        await callback.message.edit_caption(
            caption=product_text(product),
            reply_markup=get_product_buttons(product['id'], product['stock'])
        )
    except Exception as Error:
        print(f"❌ Update card Error: {Error}")