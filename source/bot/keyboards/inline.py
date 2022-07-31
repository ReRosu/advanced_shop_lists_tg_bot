from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from source.db.repositories.shoplists import ShopListsRep
from source.db.repositories.friends import FriendsRep


async def accept_kb() -> InlineKeyboardMarkup:
    kb_markup = InlineKeyboardMarkup()

    kb_markup.insert(InlineKeyboardButton('Подтвердить', callback_data='accept'))
    kb_markup.insert(InlineKeyboardButton('Продолжить', callback_data='continue'))
    kb_markup.insert(InlineKeyboardButton('Закрыть', callback_data='close'))
    return kb_markup


async def choosing_shop_list_kb(user_tg_id: int) -> InlineKeyboardMarkup:
    all_active_users_sls = [x for x in await ShopListsRep.all_by_user_id(user_tg_id) if not x.is_over]

    kb_markup = InlineKeyboardMarkup()

    for i in all_active_users_sls:
        kb_markup.insert(InlineKeyboardButton(i.name))
        kb_markup.row()

    kb_markup.insert(InlineKeyboardButton('Закрыть'))

    return kb_markup


async def choosing_friend_to_add_to_sl(user_tg_id: int) -> InlineKeyboardMarkup:
    all_user_friends = await FriendsRep.all_friends_by_id(user_tg_id)

    kb_markup = InlineKeyboardMarkup()

    for i in all_user_friends:
        if i.user_id == user_tg_id:
            tmp_id = i.friend_id
        else:
            tmp_id = i.user_id
        kb_markup.insert(InlineKeyboardButton(tmp_id))

    kb_markup.insert(InlineKeyboardButton('Подтвердить'))
    kb_markup.insert(InlineKeyboardButton('Продолжить'))
    kb_markup.insert(InlineKeyboardButton('Закрыть'))

    return kb_markup
