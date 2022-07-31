from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from source.db.repositories.shoplists import ShopListsRep


async def accept_kb(accept_event_callback_data: str):
    kb_markup = InlineKeyboardMarkup()

    kb_markup.insert(InlineKeyboardButton('подтвердить', callback_data=accept_event_callback_data))

    return kb_markup


async def choosing_shop_list_kb(user_tg_id: int):
    all_active_users_sls = [x for x in await ShopListsRep.all_by_user_id(user_tg_id) if not x.is_over]

    kb_markup = InlineKeyboardMarkup()

    for i in all_active_users_sls:
        kb_markup.insert(InlineKeyboardButton(i.name, callback_data=i.name))
        kb_markup.row()

    return kb_markup

