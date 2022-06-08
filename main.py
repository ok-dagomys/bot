import asyncio
from asyncio import set_event_loop, new_event_loop

import aioschedule

from service import weather, covid, ami_listener, phonebook
from sql.crud import create_table, drop_table
from telegram.bot import bot_run


async def scheduler():
    aioschedule.every(15).to(30).minutes.do(weather, greet='Прогноз погоды: ')
    aioschedule.every(30).minutes.do(covid, greet='Коронавирус\nоперативные данные\n\n')
    aioschedule.every(1).hour.do(phonebook, greet='Телефонный справочник обновлен')
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def tasks():
    asyncio.create_task(scheduler())
    asyncio.create_task(ami_listener())
    await asyncio.sleep(0.1)


set_event_loop(new_event_loop())
asyncio.get_event_loop().run_until_complete(tasks())


if __name__ == '__main__':
    bot_run(startup=create_table, shutdown=drop_table)
