import json


def shop_list_to_json(shop_list_s):
    list_from_s = shop_list_s.split('\n')
    for i in range(0, len(list_from_s)):
        t = list_from_s[i].split('-')
        list_from_s[i] = {"name": t[0], "volume": t[1], 'is_byed': False}
    json_s = json.dumps(list_from_s)
    return json_s
