from app.constants.currency_list import CURRENCY_LIST

def checkIfCurrencyInList(currency):
    for currency_info in CURRENCY_LIST:
        if currency_info["code"] == currency:
            return True

    return False