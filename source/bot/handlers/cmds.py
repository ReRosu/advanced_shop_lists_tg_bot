from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.text_decorations import html_decoration
import aiogram.utils.markdown as fmt

from source.bot.bot import dp
from source.bot.states import CreateShopListStates, ChangingShopListStates, AddingFriendStates
from source.db.repositories.users import UsersRep
from source.db.repositories.shoplists import ShopListsRep
from source.models.user import AddUserInDb
from source.models.shoplist import AddShopListInDb

# from source.db.repositories.friends import FriendsRep
# from source.db.repositories.shopliststousers import SLStoUsersRep


@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    if not await UsersRep.by_id(message.from_user.id):
        add_usr: AddUserInDb = AddUserInDb(id=message.from_user.id)
        await UsersRep.add(add_usr)
    await message.answer('''Привет, этот бот поможет сделать поход в магазины удобнее для тебя и твоих друзей.
    \nВведи команду /help чтобы увидеть что может бот''')


@dp.message_handler(commands=['help'], state='*')
async def help(message: types.Message):
    await message.reply('''Команды бота:\n 
    <b>1. /create_sl - создание списка покупок </b> 
    <b>2. /watch_my_active_sls - вывод ваших активных списков покупок </b> 
    <b>3. /watch_my_last_sl - вывод вашего последнего списка покупок</b> 
    <b>4. /get_my_id - вывод вашего id </b>
    <b>5. /help - список команд  </b>''', parse_mode=types.ParseMode.HTML)


@dp.message_handler(commands=['get_my_id'])
async def get_my_id(msg: types.Message):
    await msg.reply(f'Ваш id: {msg.from_user.id}')


@dp.message_handler(commands=['watch_my_active_sls'])
async def watch_my_active_shoplists(msg: types.Message):
    shop_lists = ' '.join([str(i.dict()) for i in await ShopListsRep.all_by_user_id(msg.from_user.id)])
    await msg.reply(shop_lists)


@dp.message_handler(commands=['watch_my_last_sl'])
async def watch_my_last_sl(msg: types.Message):
    last_shop_list = await ShopListsRep.all_by_user_id(msg.from_user.id)[-1]
    await msg.reply(str(last_shop_list.dict()))

@dp.message_handler(commands=['create_sl'])
async def create_shop_list(msg: types.Message):
    pass
