from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from source.db.repositories.friends import FriendsRep
from source.db.repositories.users import UsersRep


async def choosing_friend_to_add_to_sl(user_tg_id: int) -> ReplyKeyboardMarkup:
    all_user_friends = await FriendsRep.all_friends_by_id(user_tg_id)

    kb_markup = ReplyKeyboardMarkup()

    for i in all_user_friends:
        if i.user_id == user_tg_id:
            tmp_id = i.friend_id
        else:
            tmp_id = i.user_id
        kb_markup.insert(KeyboardButton(str(tmp_id)))
        kb_markup.row()

    kb_markup.insert(KeyboardButton('Подтвердить'))
    kb_markup.insert(KeyboardButton('Продолжить'))
    kb_markup.insert(KeyboardButton('Закрыть'))

    return kb_markup
