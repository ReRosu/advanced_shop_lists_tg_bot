from aiogram import types
from aiogram.dispatcher import FSMContext

import source.bot.bot
from source.bot.bot import dp
from source.bot.states import CreateShopListStates
from source.db.repositories.shoplists import ShopListsRep
from source.db.repositories.users import UsersRep
from source.models.shoplist import AddShopListInDb
from source.models.user import AddUserInDb
import source.services.jsonService as jS
from source.bot.keyboards import inline
from source.db.repositories.friends import FriendsRep
from source.db.repositories.shopliststousers import ShopListsToUsersRep


#373740493
#458183945

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    if not await UsersRep.by_id(message.from_user.id):
        add_usr: AddUserInDb = AddUserInDb(id=message.from_user.id)
        await UsersRep.add(add_usr)
    await message.answer('''Привет, этот бот поможет сделать поход в магазины удобнее для тебя и твоих друзей.
    \nВведи команду /help чтобы увидеть что может бот.''')


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    await message.reply('''Команды бота: \n 
    <b>1. /create_sl - создание списка покупок </b> 
    <b>2. /watch_my_active_sls - вывод ваших активных списков покупок </b> 
    <b>3. /watch_my_last_sl - вывод вашего последнего списка покупок </b> 
    <b>4. /get_my_id - вывод вашего id </b>
    <b>5. /get_my_friends - вывод всех ваших друзей</b>
    <b>6. /help - список команд  </b>''')


@dp.message_handler(commands=['get_my_id'])
async def get_my_id(msg: types.Message):
    await msg.reply(f'Ваш id: {msg.from_user.id}')


@dp.message_handler(commands=['get_my_friends'])
async def get_my_friends(msg: types.Message):
    await msg.reply(f"Список ваших друзей, {msg.from_user.full_name}:\n" + '\n'.join(str(x) for x in await FriendsRep.all_friends_by_id(msg.from_user.id)))


@dp.message_handler(commands=['watch_my_active_sls'])
async def watch_my_active_shoplists(msg: types.Message):
    shop_lists = ' '.join([str(i.dict()) for i in await ShopListsRep.all_by_user_id(msg.from_user.id)])
    await msg.reply(shop_lists)


@dp.message_handler(commands=['watch_my_last_sl'])
async def watch_my_last_sl(msg: types.Message):
    last_shop_list = (await ShopListsRep.all_by_user_id(msg.from_user.id))[-1]
    await msg.reply(str(last_shop_list.dict()))


@dp.message_handler(commands=['create_sl'])
async def create_shop_list(msg: types.Message):
    await msg.reply('Введите список покупок несколькими сообщениями формата: [Название продукта] - [Требуемое '
                    'количество продукта]')
    await CreateShopListStates.writing_shop_list.set()


@dp.message_handler(state=CreateShopListStates.writing_shop_list)
async def writing_shop_list(msg: types.Message, state=FSMContext):
    add_shop_list_in_db: AddShopListInDb = AddShopListInDb()
    prepareted_msg = await jS.str_preparation(msg.text)
    add_shop_list_in_db.shop_list = await jS.shop_list_to_json(prepareted_msg)
    await msg.reply('В список покупок будут добавлены:\n' +
                    '/n'.join([f"{t['name']} - {t['volume']}" for t in prepareted_msg]),
                    reply_markup=await inline.accept_kb('sl'+str(msg.from_user.id)))




