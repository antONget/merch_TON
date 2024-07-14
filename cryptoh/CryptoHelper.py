# import requests as r
import aiohttp
import decimal
from enum import Enum
from typing import Any, Union
from fake_useragent import UserAgent


class TonCurrencyEnum(str, Enum):
    nanoton = 'nanoton'
    ton = 'ton'


units = {
    TonCurrencyEnum.nanoton:       decimal.Decimal('1'),
    TonCurrencyEnum.ton:           decimal.Decimal('1000000000'),
}

integer_types = (int,)
string_types = (bytes, str, bytearray)

MIN_VAL = 0
MAX_VAL = 2 ** 256 - 1


def is_integer(value: Any) -> bool:
    return isinstance(value, integer_types) and not isinstance(value, bool)


def is_string(value: Any) -> bool:
    return isinstance(value, string_types)


# Эта функция для перевода из нормального вида в nano
# (это нужно для переводов) пусть просто будет, может пригодиться

# def to_nano(number: Union[int, float, str, decimal.Decimal], unit: str) -> int:
#     """from coins to nanocoins

#     Args:
#         number (Union[int, float, str, decimal.Decimal])
#         unit (str): unit of the number

#     Returns:
#         int: nanoton
#     """
#     if unit.lower() not in units:
#         raise ValueError(
#             "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
#         )

#     if is_integer(number) or is_string(number):
#         d_number = decimal.Decimal(value=number)
#     elif isinstance(number, float):
#         d_number = decimal.Decimal(value=str(number))
#     elif isinstance(number, decimal.Decimal):
#         d_number = number
#     else:
#         raise TypeError(
#             "Unsupported type.  Must be one of integer, float, or string")

#     s_number = str(number)
#     unit_value = units[unit.lower()]

#     if d_number == decimal.Decimal(0):
#         return 0

#     if d_number < 1 and "." in s_number:
#         with decimal.localcontext() as ctx:
#             multiplier = len(s_number) - s_number.index(".") - 1
#             ctx.prec = multiplier
#             d_number = decimal.Decimal(
#                 value=number, context=ctx) * 10 ** multiplier
#         unit_value /= 10 ** multiplier

#     with decimal.localcontext() as ctx:
#         ctx.prec = 999
#         result_value = decimal.Decimal(
#             value=d_number, context=ctx) * unit_value

#     if result_value < MIN_VAL or result_value > MAX_VAL:
#         raise ValueError(
#             "Resulting nanoton value must be between 1 and 2**256 - 1")

#     return int(result_value)


def from_nano(number: int, unit: str) -> Union[int, decimal.Decimal]:
    """from nanocoins to coins

    Args:
        number (int)
        unit (str): required unit

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        Union[int, decimal.Decimal]: _description_
    """
    if unit.lower() not in units:
        raise ValueError(
            "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
        )

    if number == 0:
        return 0

    if number < MIN_VAL or number > MAX_VAL:
        raise ValueError("value must be between 1 and 2**256 - 1")

    unit_value = units[unit.lower()]

    with decimal.localcontext() as ctx:
        ctx.prec = 999
        d_number = decimal.Decimal(value=number, context=ctx)
        result_value = d_number / unit_value

    return result_value





class TonHelper:
    def __init__(self):
        pass
    
    async def get_balance(self, address: str):
       async with aiohttp.ClientSession(headers={'User-Agent':UserAgent().random}) as session:
            resp = await (await session.get(f"https://testnet.toncenter.com/api/v2/getWalletInformation?address={address}")).json()
            try:
                if resp['ok'] == True:
                    return from_nano(int(resp['result']['balance']), TonCurrencyEnum.ton)
            except Exception as e:
                return 'ERROR_'+str(e)
            return 'SMTH_WRONG', resp
    
    async def check_valid_address(self, address: str):
        async with aiohttp.ClientSession(headers={'User-Agent':UserAgent().random}) as session:
            resp = await (await session.get(f"https://testnet.toncenter.com/api/v2/getWalletInformation?address={address}")).json()
            try:
                if resp['ok'] == True:
                    return True
            except:
                return False
            return False



ton_helper = TonHelper()








import asyncio

# print(asyncio.run(ton_helper.get_balance(address='EQAFe_UHOda_RqEn5TSpijG0ZeSN6r7vqtSE36yzMnumM_k5')))
# print(asyncio.run(ton_helper.check_valid_address(address='EQAFe_UHOda_RqEn5TSpijG0ZeSN6r7vqtSE36yzMnumM_k5')))

