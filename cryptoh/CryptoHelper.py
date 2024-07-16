# import requests as r
import aiohttp
from fake_useragent import UserAgent


import asyncio, logging as lg

from dataclasses import dataclass

from config_data.config import Config, load_config



@dataclass
class XRocketPayCurrency:
    ton = "TONCOIN"
    usdt = "USDT"


@dataclass
class XRocketPayStatus:
    passed = 'None'
    active = "active"
    paid = "paid"
    expired = "expired"




class XRocketPay:
    def __init__(self, token: str, is_testnet: bool = False):
        self.token = token

        self.url = 'https://dev-pay.ton-rocket.com' if is_testnet else 'https://pay.ton-rocket.com'


    async def create_incoice(self, amount, currency: XRocketPayCurrency, description: str = None ):
        """
        create incoice:

            :param amount: amount to pay
            :param currency: currency of payment
            :param description: description for invoice
            :return: invoice id and link to invoice in XRocketPay
        """

        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.post(f'{self.url}/tg-invoices', 
                                      json={
                                          'amount': amount,
                                          'currency': currency,
                                          'description': description
                                          }
                                          ) 
            data = await resp.json()
            # print(data)
            return (data['data']['id'], data['data']['link']) if data['success'] else "INVOICE_DOESNT_CREATED"
        
    async def get_invoice_info(self, invoice_id):
        """
        get invoice info:
        
            :param invoice_id: id of invoice
            :return: invoice info
        """
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.get(f'{self.url}/tg-invoices/{invoice_id}') 
            data = await resp.json()
            return data

    async def delete_invoice(self, invoice_id:int) -> bool:
        """
        delete invoice:
        
            :param invoice_id: id of invoice
            :return: True if invoice deleted else False
        """
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.delete(f'{self.url}/tg-invoices/{invoice_id}') 
            data = await resp.json()
            return data['success']
    
    async def check_invoice_payed(self, invoice_id: int) -> bool:
        """
        check invoice payed:
        
            :param invoice_id: id of invoice
            :return: True if invoice paid else False
        """
        # status codes : active, paid, expired
        data = await self.get_invoice_info(invoice_id)

        if data['success']:
            if data['data']['status'] == XRocketPayStatus.paid:
                await self.delete_invoice(invoice_id)
                return True
            
        return False


config: Config = load_config()


XROCKET_TOKEN =  config.tg_bot.xrocket_token


# is_testnet = True (for tests)
x_roket_pay: XRocketPay = XRocketPay(token=XROCKET_TOKEN)




# tests
# print(asyncio.run(x_roket_pay.create_incoice(amount=0.1, currency=XRocketPayCurrency.ton, description='Pay for our merch!\n')))
# print(asyncio.run(x_roket_pay.get_invoice_info(1295596)))
# print(asyncio.run(x_roket_pay.check_invoice_payed(1311689)))
# print(asyncio.run(x_roket_pay.delete_invoice(1311698)))

















# # Простой датакласс
# class TonCurrencyEnum(str, Enum):
#     nanoton = 'nanoton'
#     ton = 'ton'



# # Словарь для конвертации из nanocoin в coin и обратно.
# units = {
#     TonCurrencyEnum.nanoton:       decimal.Decimal('1'),
#     TonCurrencyEnum.ton:           decimal.Decimal('1000000000'),
# }


# # Данные для функций
# integer_types = (int,)
# string_types = (bytes, str, bytearray)

# MIN_VAL = 0
# MAX_VAL = 2 ** 256 - 1


# def is_integer(value: Any) -> bool:
#     return isinstance(value, integer_types) and not isinstance(value, bool)


# def is_string(value: Any) -> bool:
#     return isinstance(value, string_types)


# # func to make from coin to nanocoin
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





# # func to make from nanocoin to coin
# def from_nano(number: int, unit: str) -> Union[int, decimal.Decimal]:
#     """from nanocoins to coins

#     Args:
#         number (int)
#         unit (str): required unit

#     Raises:
#         ValueError: _description_
#         ValueError: _description_

#     Returns:
#         Union[int, decimal.Decimal]: _description_
#     """
#     if unit.lower() not in units:
#         raise ValueError(
#             "Unknown unit.  Must be one of {0}".format("/".join(units.keys()))
#         )

#     if number == 0:
#         return 0

#     if number < 0 or number > 2 ** 256 - 1:
#         raise ValueError("value must be between 1 and 2**256 - 1")

#     unit_value = units[unit.lower()]

#     with decimal.localcontext() as ctx:
#         ctx.prec = 999
#         d_number = decimal.Decimal(value=number, context=ctx)
#         result_value = d_number / unit_value

#     return result_value





# class TonHelper:
#     def __init__(self):
#         pass
    
#     async def get_balance(self, address: str) -> float:
#         async with aiohttp.ClientSession(headers={'User-Agent': UserAgent().random}) as session:
#             resp = await (await session.get(
#                 f"https://testnet.toncenter.com/api/v2/getWalletInformation?address={address}")).json()
            
#             try:
#                 if resp['ok'] == False and resp['code'] == 429:
                    
#                     #  limit exceeded, waiting and trying again..

#                     await asyncio.sleep(1.5)
#                     lg.info("Limit exceeded, trying again")
#                     return await self.get_balance(address)
                
#                 elif resp['ok']:
#                     return int(resp['result']['balance'])
#                 lg.info(resp)
#                 return resp
            
#             except Exception as e:
#                 return 'ERROR_'+str(e)


#     async def check_valid_address(self, address: str):
#         async with aiohttp.ClientSession(headers={'User-Agent':UserAgent().random}) as session:
#             resp = await (await session.get(
#                 f"https://testnet.toncenter.com/api/v2/getWalletInformation?address={address}")).json()
#             try:
#                 if resp['ok']:
#                     return True
#             except:
#                 return False
#             return False



# ton_helper = TonHelper()







# import asyncio

# print(asyncio.run(ton_helper.get_balance(address='EQAFe_UHOda_RqEn5TSpijG0ZeSN6r7vqtSE36yzMnumM_k5')))
# print(asyncio.run(ton_helper.check_valid_address(address='EQAFe_UHOda_RqEn5TSpijG0ZeSN6r7vqtSE36yzMnumM_k5')))

