import asyncio

import aioschedule

from service import weather, covid
from sql.crud import create_table, drop_table
from telegram.bot import bot_run


async def scheduler():
    aioschedule.every(15).to(30).seconds.do(weather, greet='Прогноз погоды: ')
    aioschedule.every(30).seconds.do(covid, greet='Коронавирус\nоперативные данные\n\n')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def tasks():
    asyncio.create_task(scheduler())
    # asyncio.create_task(routes.ami_listener())
    await asyncio.sleep(1)
asyncio.get_event_loop().run_until_complete(tasks())


if __name__ == '__main__':
    bot_run(startup=create_table, shutdown=drop_table)
