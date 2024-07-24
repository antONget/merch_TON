import aiohttp

import logging as lg

from dataclasses import dataclass


@dataclass
class CryptoBotPayCurrency:
    ton = 'TON'
    usdt = 'USDT'


class CryptoBotPay:
    def __init__(self, token: str, is_testnet: bool = True):
        self.token = token

        self.base_url = "https://testnet-pay.crypt.bot/api" if is_testnet else "https://pay.crypt.bot/api"
        # print(self.base_url)

    
    async def _get_app(self) -> str:
        """
        Get app info.
        """
        async with aiohttp.ClientSession(headers={'Crypto-Pay-API-Token' : self.token}) as session:
            return await (await session.get(f"{self.base_url}/getMe")).json() 
        
    async def _get_balance(self):
        """
        Get bot balance.
        """
        async with aiohttp.ClientSession(headers={'Crypto-Pay-API-Token' : self.token}) as session:
            return await (await session.get(f"{self.base_url}/getBalance")).json()


    async def create_invoice(self,
                             amount,
                             description: str = None,
                             currency: CryptoBotPayCurrency = CryptoBotPayCurrency.ton):
        """
        Create invoice.
        returns (invoice_id, pay_url)
        """
        async with aiohttp.ClientSession(headers={'Crypto-Pay-API-Token' : self.token}) as session:
            resp = await (await session.post(f"{self.base_url}/createInvoice", 
                                             json={
                                                   'asset': currency,
                                                   'amount': amount,
                                                   'description': description or 'Pay for our merch!',
                                                   }
                                                )
                                            ).json()
            return resp['result']['invoice_id'], resp['result']['pay_url']
    
    async def get_status_invoices(self, status_invoices: str):
        """

        Get status ['active' | 'paid'] invoices.
        """
        async with aiohttp.ClientSession(headers={'Crypto-Pay-API-Token' : self.token}) as session:
            return (await (await session.get(
                f"{self.base_url}/getInvoices",
                  json={
                      'status': status_invoices,
                  }
                  
                  )).json() )['result']['items']
        
    async def check_invoice_paid(self, invoice_id: str) -> bool:
        """
        Check invoice paid.
        """
        
        return invoice_id in [invoice['invoice_id'] for invoice in await self.get_status_invoices(status_invoices='paid')]
    
    async def _delete_invoice(self, invoice_id: int):
        """
        Delete invoice.
        """
        async with aiohttp.ClientSession(headers={'Crypto-Pay-API-Token' : self.token}) as session:
            return await (await session.get(f"{self.base_url}/deleteInvoice", params={'invoice_id':invoice_id})).json()








    


import asyncio

crypto_bot_api = CryptoBotPay(token='15584:AAzUkmSPZ27jjquDtrxCTsylixXESnN6ytS')
# crypto_bot_api = CryptoBotPay(token='167586:AAheM5cDZPR0iqM3Qh4YrglgofKSvnjNQJe', is_testnet=False)



# print(asyncio.run(crypto_bot_api._get_app()))
# print(asyncio.run(crypto_bot_api.create_invoice(0.01)))
# print(asyncio.run(crypto_bot_api.get_status_invoices(status_invoices='paid')))
# print(asyncio.run(crypto_bot_api._delete_invoice(248689)))
# print(asyncio.run(crypto_bot_api._get_balance()))
# print(asyncio.run(crypto_bot_api.check_invoice_paid(248689)))