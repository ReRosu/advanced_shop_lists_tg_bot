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

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('Привет, этот бот поможет сделать поход в магазины удобнее для тебя и твоих друзей.\n Введи '
                         'команду /help чтобы увидеть что может бот')

