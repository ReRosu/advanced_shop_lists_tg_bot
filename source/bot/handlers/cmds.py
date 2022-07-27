from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.utils.text_decorations import html_decoration

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
    await message.reply('aboba')

