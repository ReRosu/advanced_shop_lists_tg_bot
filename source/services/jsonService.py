import json


# подготовка строки к превращению в json
async def str_preparation(shop_list_s: str) -> list:
    list_from_s: list = list(shop_list_s.split('\n'))
    result_list: list = []
    for i in range(0, len(list_from_s)):
        t = list_from_s[i].split('-')
        result_list.append({"name": t[0], "volume": t[1], 'is_byed': False})
    return result_list


# превращение в json
async def shop_list_to_json(shop_list_l: list) -> str:
    json_s: str = json.dumps(shop_list_l)
    return json_s


# добавление к json строке новых элементов
async def add_items_to_json_shop_list(shop_list_json: str, items_to_add: list) -> list:
    list_from_j: list = list(json.loads(shop_list_json))
    result_list: list = [*list_from_j, *items_to_add]
    return result_list


async def add_items_to_shop_list(shop_list: list, items_to_add: list) -> list:
    result_list: list = [*shop_list, *items_to_add]
    return result_list


async def from_json(json_shoplist: str) -> list:
    result_shoplsit: list = json.loads(json_shoplist)
    return result_shoplsit
