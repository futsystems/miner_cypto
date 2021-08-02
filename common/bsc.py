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

    def get_chain_balance(self, address):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.async_get_bnb_balance(address))
        loop.run_until_complete(task)
        return float(task.result())*1e-18

    async def async_get_balance_by_token_contact(self, address, contact):
        async with BscScan(self._api_key) as bsc:
            return await bsc.get_acc_balance_by_token_contract_address(contract_address=contact, address=address)


    def _get_token_balance(self, address, token_contact):
        loop = asyncio.get_event_loop()
        task = loop.create_task(self.async_get_balance_by_token_contact(address, token_contact))
        loop.run_until_complete(task)
        return float(task.result())

    def get_zoon_balance(self, address):
        """
        zoon contact address 0x9D173E6c594f479B4d47001F8E6A95A7aDDa42bC
        :param address:
        :return:
        """
        return self._get_token_balance(address, '0x9D173E6c594f479B4d47001F8E6A95A7aDDa42bC')*1e-18

    def get_skill_balance(self, address):
        """
        skill contact address 0x154A9F9cbd3449AD22FDaE23044319D6eF2a1Fab
        :param address:
        :return:
        """
        return self._get_token_balance(address, '0x154A9F9cbd3449AD22FDaE23044319D6eF2a1Fab')*1e-18


    def get_token_balance(self,address,token):
        if token=='ZOON':
            return self.get_zoon_balance(address)
        if token=='SKILL':
            return self.get_skill_balance(address)

        return 0
