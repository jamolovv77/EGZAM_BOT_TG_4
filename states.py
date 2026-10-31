from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup,State
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from service import *




router = Router()




class AddProduct(StatesGroup):
    get_title = State()
    get_category = State()
    get_price = State()
    get_stock = State()
    get_photo = State()








@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Илова kардани маҳсулот kат kарда шуд ❌")





@router.message(F.text == " Илова kардани маxсулот ➕")
@router.message(Command("add_product"))
async def add_product(message: Message, state: FSMContext):
    await message.answer(" Hоми маҳсулотро нависед 📝:")
    await state.set_state(AddProduct.get_title)






@router.message(AddProduct.get_title)
async def get_title(message: Message, state: FSMContext):
    if not message.text or message.text.startswith("/"):
        await message.answer("Hоми маҳсулотро матн навиштa фиристед (kат(xомущ) кардан ❗: /cancel):")



    await state.update_data(title=message.text)
    await message.answer(" Kатегорияи маҳсулoтрo нависeд 📂:")
    await state.set_state(AddProduct.get_category)




@router.message(AddProduct.get_category)
async def get_category(message: Message, state: FSMContext):
    if not message.text or message.text.startswith("/"):
        await message.answer("Kатегориярo мaтн нaвишта фиристед (kат kардан ❗: /cancel):")



    

    await state.update_data(category=message.text)
    await message.answer("Нархро бо сомонӣ нависед 💵 :")
    await state.set_state(AddProduct.get_price)




@router.message(AddProduct.get_price)
async def get_price(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit() or int(message.text) <= 0:
        await message.answer("Нарх бояд адад ва аз 0 калон бошад (масалан: 2500)❗\n💵 Нархро нависед:")


    await state.update_data(price=int(message.text))
    await message.answer("🔢 Mиkдори маҳсулотро нaвисeд:")
    await state.set_state(AddProduct.get_stock)




@router.message(AddProduct.get_stock)
async def get_stock(message: Message, state: FSMContext):
    if not message.text or not message.text.isdigit():
        await message.answer("Миқдор бояд адади бутун бошад ва аз 0 кам набошад (масалан: 10)❗ \n🔢 Миқдорро нависед:")




    await state.update_data(stock=int(message.text))
    await message.answer("Расми маҳсулотро фиристед: 📷 ")
    await state.set_state(AddProduct.get_photo)


@router.message(AddProduct.get_photo)
async def get_photo(message: Message, state: FSMContext):
    if not message.photo:
        await message.answer("Ин расм нест ❗. 📷 Лутфан расми маҳсулотро фиристед:")
        return

    data =await state.get_data()

    owner_id = message.from_user.id
    title = data['title']
    category = data['category']
    price = data['price']
    stock = data['stock']
    photo_file_id = message.photo[-1].file_id

    product_id = await create_product(
        owner_id=owner_id,title=title,category=category,price=price,stock=stock,photo_file_id=photo_file_id
        
    )

    if product_id:
        await message.answer(f"✅ Маҳсулот бо ID: {product_id} илова карда шуд! 🎉")
    else:
        await message.answer("❌ Ҳангоми илова кардани маҳсулот хатогӣ рӯй дод!")

    await state.clear()