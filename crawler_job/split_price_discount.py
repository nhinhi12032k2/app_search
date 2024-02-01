import re


def split_price_discount(lst):
    prices = []
    discounts = []
    for item in lst:
        price, *discount = re.findall(r'(\d+\.?\d*₫)(?:\n-(\d+)%)*', item)[0]
        prices.append(price)
        discounts.append(f"{discount[0]}%" if discount else None)
    return prices, discounts