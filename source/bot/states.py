from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateShopListStates (StatesGroup):
    writing_shop_list = State()
    adding_friends = State()
    giving_name = State()
    checking_shop_list = State()


class ChangingShopListStates (StatesGroup):
    noticing_purchase = State()
    changing_added_friends = State()
    checking_shop_list = State()


class AddingFriendStates (StatesGroup):
    writing_friend_id = State()
