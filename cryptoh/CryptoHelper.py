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


    async def create_incoice(self, amount: int | float, currency: XRocketPayCurrency, description: str = None ) -> tuple[str, str]:
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


