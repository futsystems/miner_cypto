#!/usr/bin/python
# -*- coding: utf-8 -*-

import asyncio
from bscscan import BscScan


class BSCAPI(object):
    def __init__(self):
        self._api_key = '5B7Y6IW73Y33Z8TNPR68XD2CHP63I5CVM5'

    async def get_balance(self):
        async with BscScan(self._api_key) as bsc:
            return await bsc.get_bnb_balance(address="0x0000000000000000000000000000000000001004")
