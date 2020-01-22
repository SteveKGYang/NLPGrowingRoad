def remove_dash(wor):
    wo = wor.split("[")
    return "".join(wo)


def deal_num(num):
    if "年" in num or "月" in num or "日" in num or "点钟" in num:
        return 'TIME'
    if "％" in num or "%" in num:
        return 'NUM'
    for cha in num:
        if cha not in '０１２３４５６９７８一二三四五六七八九十零百千万．第：:亿∶·百分之点':
            return num
    return 'NUM'
