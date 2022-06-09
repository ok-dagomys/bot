import asyncio
import logging

from asterisk import ami
from covid.prognosis import covid_request
from phone.dictionary import check_phonebook, caller_recognition, name_recognition
from sql import crud
from telegram import bot
from weather.forecast import weather_request

logging.basicConfig(level=logging.INFO)


@bot.dp.message_handler(commands=['search'])
async def bot_answer(message: bot.types.Message):
    search = await name_recognition(message.text)
    await bot.send_message(search)
    await message.delete()
    await asyncio.sleep(0.1)


async def weather(greet):
    forecast = await weather_request()
    sql_forecast, sql_id = await asyncio.create_task(crud.select('weather'))

    if forecast != sql_forecast:
        try:
            weather_id = sql_id
            await bot.edit_message(greet + forecast, weather_id)
        except Exception as ex:
            print(f'{ex} (id: {sql_id})')
            weather_id = await bot.send_message(greet + forecast)
            await bot.pin_message(weather_id)
        finally:
            await asyncio.create_task(crud.update('weather', forecast, weather_id))
            await asyncio.sleep(0.1)


async def covid(greet):
    prognosis = await covid_request()
    sql_prognosis, sql_id = await asyncio.create_task(crud.select('covid'))

    if prognosis != sql_prognosis:
        try:
            covid_id = await bot.send_message(greet + prognosis)
            await asyncio.create_task(crud.update('covid', prognosis, covid_id))
        except Exception as ex:
            print(ex)
        finally:
            await asyncio.sleep(0.1)


async def phonebook(greet):
    status = await check_phonebook()
    if status == 'Phonebook updated':
        await bot.send_message(greet)
    await asyncio.sleep(0.1)


async def ami_listener():
    ami.connect(state=False)
    while True:
        try:
            if ami.event:
                logging.info(ami.event[0])
                ami.event = []
            elif ami.caller and ami.number:
                call = await caller_recognition(ami.caller[0], ami.number[0])
                call_id = await bot.send_message(call)
                ami.number, ami.caller = [], []
            elif ami.status:
                await bot.delete_message(call_id)
                bot.id_list.remove(call_id)
                ami.status = []
            await asyncio.sleep(0.1)
        except Exception as ex:
            print(f'Aiogram error: {ex}')
            ami.status = []
