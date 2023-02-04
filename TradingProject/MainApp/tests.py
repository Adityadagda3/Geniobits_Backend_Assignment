# Create your tests here.

import asyncio
import json

from celery import shared_task


@shared_task
def convert_candles_to_timeframe(candles, timeframe):
    async def convert_candle(candle, converted_candle=None):
        # Convert the candle to the given timeframe
        await asyncio.sleep(1)  # Simulate a wait operation
        return converted_candle

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = [convert_candle(candle) for candle in candles]
    converted_candles = loop.run_until_complete(asyncio.gather(*tasks))

    with open('converted_candles.json', 'w') as f:
        json.dump(converted_candles, f)

