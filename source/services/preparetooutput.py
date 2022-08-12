from source.services.jsonService import from_json

from source.models.shoplist import ShopListInDb
from source.db.repositories.shopliststousers import ShopListsToUsersRep
from source.db.repositories.users import UsersRep
from source.db.repositories.bugreports import BugReportsRep
from source.db.repositories.wishes import WishesRep
from source.models.wish import WishInDb
from source.models.bugreport import BugReportInDb


async def prepare_shoplist(shoplist: ShopListInDb) -> str:
    result_str: str = shoplist.name + '\nСписок покупок:\n' + \
                      '\n'.join([f"{item['name']} - {item['volume']}"
                                 for item in (await from_json(shoplist.shop_list))]) + \
                      '\nДрузья прикрепленные к списку покупок:\n' + \
                      '\n'.join(['@' + str((await UsersRep.by_id(x)).user_name)
                                 for x in await ShopListsToUsersRep.all_by_shop_list_id(shoplist.id)]) + '\n'
    return result_str


async def prepare_bug_report(bug_report: BugReportInDb):
    result_str: str = '<b>Bug report id:</b> ' + str(bug_report.id) + '\nUser: @' + \
                      (await UsersRep.by_id(bug_report.user_id)).user_name + '\n\nBug report message:\n' \
                      + bug_report.message
    return result_str


async def prepare_wish_report(wish_report: WishInDb):
    result_str: str = '<b>Wish report id:</b> ' + str(wish_report.id) + '\nUser: @' + \
                      (await UsersRep.by_id(wish_report.user_id)).user_name + '\n\nBug report message:\n\n' \
                      + wish_report.message
    return result_str
