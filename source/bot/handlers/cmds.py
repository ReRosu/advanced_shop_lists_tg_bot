from aiogram import types
from aiogram.dispatcher import FSMContext

import source.bot.bot
from source.bot.bot import dp
from source.bot.states import CreateShopListStates
from source.db.repositories.shoplists import ShopListsRep
from source.db.repositories.users import UsersRep
from source.models.shoplist import AddShopListInDb
from source.models.user import AddUserInDb, UpdateUserInDb
import source.services.jsonService as jS
from source.bot.keyboards import inline
from source.bot.keyboards import reply
from source.db.repositories.friends import FriendsRep
from source.db.repositories.shopliststousers import ShopListsToUsersRep
from source.models.shoplisttouser import AddShopListToUserInDb


# 373740493
# 458183945

@dp.message_handler(commands=['start'], state="*")
async def start(message: types.Message):
    if not await UsersRep.by_id(message.from_user.id):
        add_usr: AddUserInDb = AddUserInDb(id=message.from_user.id, user_name=message.from_user.username)
        await UsersRep.add(add_usr)
    if (await UsersRep.by_id(message.from_user.id)).user_name is None:
        update_user: UpdateUserInDb = UpdateUserInDb(user_name=message.from_user.username)
        await UsersRep.update_by_id(message.from_user.id, update_user)
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
    await msg.reply(f"Список ваших друзей, {msg.from_user.full_name}:\n" + "\n".join(
        ['@' + str((await UsersRep.by_id(x.friend_id if x.user_id == msg.from_user.id else x.user_id)).user_name)
         for x in await FriendsRep.all_friends_by_id(msg.from_user.id)]))


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
    if msg.text[0] != '/':
        prepareted_msg = await jS.str_preparation(msg.text)
        await state.update_data(add_sl=prepareted_msg)
        await state.update_data(last_msg=msg)
        await msg.reply('В список покупок будут добавлены:\n' +
                        '\n'.join([f"{t['name']} - {t['volume']}" for t in prepareted_msg]),
                        reply_markup=await inline.accept_kb())


@dp.callback_query_handler(text="accept", state=CreateShopListStates.writing_shop_list)
async def accept_shop_list(call: types.CallbackQuery, state=FSMContext):
    msg = (await state.get_data())['last_msg']
    await msg.reply(f'Список покупок был сохранен, @{msg.from_user.username}\n',
                             reply_markup=await reply.choosing_friend_to_add_to_sl(msg.from_user.id))
    await CreateShopListStates.next()


@dp.callback_query_handler(text="continue", state=CreateShopListStates.writing_shop_list)
async def continue_writing_shop_list(call: types.CallbackQuery):
    await create_shop_list(call.message)


@dp.callback_query_handler(text='close', state=CreateShopListStates.writing_shop_list)
async def close_writing_shop_list(call: types.CallbackQuery, state=FSMContext):
    await call.message.reply('Список покупок будет удален.')
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=CreateShopListStates.adding_friends)
async def adding_friends_to_shop_list(msg: types.Message, state=FSMContext):
    data = await state.get_data()
    if data.get('friends_to_add', False):
        friends_to_add = data['friends_to_add']
    else:
        friends_to_add = []
    if msg.text.isdigit() and UsersRep.id_exists(int(msg.text)):
        friends_to_add.append(int(msg.text))

    await state.update_data(friends_to_add=friends_to_add)


@dp.callback_query_handler(text="accept", state=CreateShopListStates.adding_friends)
async def accept_friends_list(call: types.CallbackQuery):
    await call.message.reply('Друзья были прикреплены к списку.\n'
                             'Дайте название списку',
                             reply_markup=await inline.accept_kb())
    await CreateShopListStates.next()


@dp.callback_query_handler(text="continue", state=CreateShopListStates.adding_friends)
async def continue_writing_shop_list(call: types.CallbackQuery):
    await accept_shop_list(call)


@dp.callback_query_handler(text='close', state=CreateShopListStates.adding_friends)
async def close_writing_shop_list(call: types.CallbackQuery, state=FSMContext):
    await call.message.reply('Список покупок будет удален.')
    await state.reset_data()
    await state.finish()


@dp.message_handler(state=CreateShopListStates.giving_name)
async def giving_name(msg: types.Message, state=FSMContext):
    await state.update_data(name=msg.text)
    data = await state.get_data()
    sl_text = data['name'] + '\nСписок покупок:\n' + '\n'.join([f"{t['name']} - {t['volume']}" for t in data['add_sl']]) \
              + '\nДрузья прикрепленные к списку покупок' \
              + '\n'.join(['@' + str((await UsersRep.by_id(x.friend_id if x.user_id == msg.from_user.id else x.user_id)) \
                                     .user_name) for x in data['friends_to_add']])

    await msg.reply(sl_text, reply_markup=await inline.accept_kb())
    await CreateShopListStates.next()


@dp.callback_query_handler(text='accept', state=CreateShopListStates.checking_shop_list)
async def save_shop_list(call: types.CallbackQuery, state=FSMContext):
    data = state.get_data()
    add_sl: AddShopListInDb = AddShopListInDb(shoplist=jS.shop_list_to_json(data['add_sl']),
                                              creator_id=call.message.from_user.id, name=data['name'])
    sl = await ShopListsRep.add(add_sl)
    for i in data['friends_to_add']:
        friendship: AddShopListToUserInDb = AddShopListToUserInDb(shop_list_id=sl.id, user_id=i)
        await ShopListsToUsersRep.add(friendship)

    await call.message.reply('Список покупок был добавлен. С помощью команды /watch_my_last_sl '
                             'вы можете посмотреть последний созданный вами список покупок ')
