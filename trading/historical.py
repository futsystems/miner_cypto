#!/usr/bin/python
# -*- coding: utf-8 -*-


import asyncio
import websockets
import json
import pandas as pd
import datetime as dt
import pytz
from . import utility



async def call_api(msg):
   async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
       await websocket.send(msg)
       while websocket.open:
           response = await websocket.recv()
           return response



def async_loop(api, message):
    return asyncio.get_event_loop().run_until_complete(api(message))


def retrieve_historic_data(start, end, instrument, timeframe):
    msg = \
        {
            "jsonrpc": "2.0",
            "id": 833,
            "method": "public/get_tradingview_chart_data",
            "params": {
                "instrument_name": instrument,
                "start_timestamp": start,
                "end_timestamp": end,
                "resolution": timeframe
            }
        }
    resp = async_loop(call_api, json.dumps(msg))

    return resp


def json_to_dataframe(json_resp):
    res = json.loads(json_resp)

    df = pd.DataFrame(res['result'])

    df['ticks'] = df.ticks / 1000
    df['timestamp'] = [dt.datetime.fromtimestamp(date, pytz.utc) for date in df.ticks]

    return df


def get_hist_data(instrument, days=365, timeframe='1D'):
    utc_today = utility.utc_today()
    utc_start = utc_today - dt.timedelta(days=days)
    print(utc_today)
    print(utc_start)

    json_resp = retrieve_historic_data(utility.datetime_to_timestamp(utc_start)*1000, utility.datetime_to_timestamp(utc_today)*1000, instrument, timeframe)
    df = json_to_dataframe(json_resp)
    return df


def get_hist_data_2(instrument,date,timeframe='60'):
    utc_start = utility.string_to_datetime(date)
    utc_end = utc_start + dt.timedelta(days=1)-dt.timedelta(microseconds=1)

    print(utc_start)
    print(utc_end)

    json_resp = retrieve_historic_data(utility.datetime_to_timestamp(utc_start)*1000, utility.datetime_to_timestamp(utc_end)*1000, instrument, timeframe)
    df = json_to_dataframe(json_resp)
    return df



if __name__ == '__main__':
    start = 1609430400000
    end = 1632153600000
    #end = 1632100023266573
    instrument = "BTC-PERPETUAL"
    timeframe = '1D'

    json_resp = retrieve_historic_data(start, end, instrument, timeframe)
    print(json_resp)
    df = json_to_dataframe(json_resp)
    print(df.head())

