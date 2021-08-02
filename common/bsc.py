#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
from bscscan import BscScan


class BSCAPI(object):
    def __init__(self):
        self._api_key = '5B7Y6IW73Y33Z8TNPR68XD2CHP63I5CVM5'

    async def async_get_bnb_balance(self, address):
        async with BscScan(self._api_key) as bsc:
            return await bsc.get_bnb_balance(address=address)

    def get_bnb_balance(self, address):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.async_get_bnb_balance(address))
        loop.run_until_complete(task)
        return task.result()

    async def async_get_balance_by_token_contact(self, address, contact):
        async with BscScan(self._api_key) as bsc:
            return await bsc.get_acc_balance_by_token_contract_address(contract_address=address, address=address)


    def get_token_balance(self, address, token_contact):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.async_get_balance_by_token_contact(address, token_contact))
        loop.run_until_complete(task)
        return task.result()

