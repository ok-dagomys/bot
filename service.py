import asyncio

# from asterisk import ami
from covid.prognosis import covid_request
# from phone.dictionary import dictionary_request
from sql import crud
from telegram import bot
from weather.forecast import weather_request


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
            await asyncio.sleep(1)


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
            await asyncio.sleep(1)


# async def phonebook(greet):
#     phone = await dictionary_request()
#     sql_prognosis, sql_id = await asyncio.create_task(crud.select('phone'))
#
#     if phone != sql_prognosis:
#         try:
#             phone_id = await bot.send_message(greet + phone)
#             await asyncio.create_task(crud.update('covid', phone, phone_id))
#         except Exception as ex:
#             print(ex)
#         finally:
#             await asyncio.sleep(1)
#
#
# async def ami_listener():
#     ami.connect(state=False)
#     while True:
#         if ami.event:
#             print(ami.event[0])
#             ami.event = []
#         elif ami.caller and ami.number:
#             call_id = await bot.send_message(f'Incoming call\nfrom number: {ami.number[0]}\nto number: {ami.caller[0]}')
#             ami.number, ami.caller = [], []
#         elif ami.status:
#             await bot.delete_message(call_id)
#             bot.id_list.remove(call_id)
#             ami.status = []
#         await asyncio.sleep(1)
