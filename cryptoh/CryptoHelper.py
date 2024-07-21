import aiohttp
from dataclasses import dataclass
from config_data.config import Config, load_config

import logging as lg

from cryptoh.nanoton import from_nano, to_nano

from datetime import datetime


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

    async def create_invoice(self, amount, currency: XRocketPayCurrency, description: str = None):
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
                                      })
            data = await resp.json()
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

    async def delete_invoice(self, invoice_id: int) -> bool:
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
                # await self.delete_invoice(invoice_id)
                return True

        return False

    async def transaction_will_be_successful(self, amount, withdrawal: bool = True) -> bool:
        """
        check if transaction will be successful:
            :param amount: amount to pay
            :param withdrawal: default True, uses in transfer_funds_with_wallet_addr()
            :return: True if transaction will be successful else False
        """

        balance = to_nano((await self.get_ton_balance()), 'ton')

        lg.info(f"balance: {from_nano(balance, 'ton')}")

        amount = to_nano(amount, 'ton')

        if withdrawal:

            commission = to_nano((await self._get_ton_fees()), 'ton')

            lg.info(f"commission: {from_nano(commission, 'ton')}")

            lg.info(f"commission+amount: {from_nano(commission + amount, 'ton')}")

            if balance - (amount + commission) > 0:
                lg.info(f"ok, remains: {from_nano(abs(balance - (amount + commission)), 'ton')}")
                return True
            lg.error(f"{from_nano(abs(balance - (amount + commission)), 'ton')} ton missing. TOP UP YOUR BALANCE!!!")
            return False

        if balance - amount > 0:
            lg.info(f"ok, remains: {from_nano(abs(balance - amount), 'ton')}")
            return True

        lg.error(f"{from_nano(abs(balance - amount), 'ton')} ton missing. TOP UP YOUR BALANCE!!!")
        return False

    async def get_ton_balance(self):
        """
        get ton balance:
            :return: ton balance
        """
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.get(f'{self.url}/app/info')
            data = await resp.json()

            if data['success']:
                for i in data['data']['balances']:
                    if i['currency'] == 'TONCOIN':
                        return i['balance']

    async def _get_ton_fees(self):
        """
        get fee (comission) for withdraw:
            :return: fee
        """
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.get(f'{self.url}/app/withdrawal/fees')
            data = await resp.json()

            ton_fees = None
            if data['success']:
                try:
                    ton_fees = [i for i in data['data'] if i['code'] == 'TONCOIN'][0]['fees'][0]['feeWithdraw']['fee']
                    return ton_fees
                except:
                    return None

    async def transfer_funds_with_id(self, user_id: int, amount):
        """
        transfer funds with id:
            :param user_id: tg_id
            :param amount: amount to transfer
            :return: True if transfer done else False
        """

        if not await self.transaction_will_be_successful(amount=amount, withdrawal=False):
            return False

        json = {
            "tgUserId": user_id,
            "currency": XRocketPayCurrency.ton,
            "amount": amount,
            "transferId": datetime.now().strftime('%Y%m%d%H%M%S%f'),
            # "description": "You are awesome!" # can add any description here
        }
        # print(json)
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.post(f'{self.url}/app/transfer',
                                      json=json)
            data = await resp.json()
            # print(data)

            return data['success'] if data['success'] else False

    async def transfer_funds_with_wallet_addr(self, wallet_addr: str, amount):
        """
        transfer funds with wallet address:
            :param wallet_addr: wallet address
            :param amount: amount to transfer
            :return: True if transfer done else False
        """

        if not await self.transaction_will_be_successful(amount=amount):
            return False

        json = {
            "network": "TON",
            "address": wallet_addr,
            "currency": XRocketPayCurrency.ton,
            "amount": amount,
            "withdrawalId": datetime.now().strftime('%Y%m%d%H%M%S%f'),
            # "comment": "You are awesome!" # can add any comment here
        }
        # print(json)
        async with aiohttp.ClientSession(headers={'Rocket-Pay-Key': self.token}) as session:
            resp = await session.post(f'{self.url}/app/withdrawal',
                                      json=json)
            data = await resp.json()
            # print(data)
            return data['success'] if data['success'] else False


config: Config = load_config()
XROCKET_TOKEN = config.tg_bot.xrocket_token
x_roket_pay: XRocketPay = XRocketPay(token=XROCKET_TOKEN)
