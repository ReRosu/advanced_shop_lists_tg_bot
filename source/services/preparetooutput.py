from source.services.jsonService import from_json
from source.models.shoplist import ShopListInDb
from source.db.repositories.shopliststousers import ShopListsToUsersRep
from source .db.repositories.users import UsersRep


async def Prepare_shoplist(shoplist: ShopListInDb) -> str:
    result_str: str = shoplist.name + '\nСписок покупок:\n' +\
                      '\n'.join([f"{item['name']} - {item['volume']}" for item in (await from_json(shoplist.shop_list))]) +\
                        '\nДрузья прикрепленные к списку покупок:\n' +\
                        '\n'.join(['@'+str((await UsersRep.by_id(x)).user_name)
                                   for x in await ShopListsToUsersRep.all_by_shop_list_id(shoplist.id)]) + '\n'
    return result_str

