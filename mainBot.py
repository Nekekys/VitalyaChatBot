import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import re
from random import randint

import gensim
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

f = open('dialoguesVK.txt', 'r', encoding="utf-8")
content = f.read()
dialogs = [line.split('\n') for line in content.split('\n\n')]

main_data = []
import_data = []

for dig in dialogs:
    if len(dig) > 1:
        reDig1 = re.sub('[^А-Яа-яё\s]+', '', dig[0])
        reDig2 = re.sub('[^А-Яа-яё\s]+', '', dig[1])
        reDig1 = ' '.join(reDig1.split())
        reDig2 = ' '.join(reDig2.split())
        main_data.append(reDig1)
        main_data.append(reDig2)


model = Doc2Vec.load('models_doc2vec_200_vector_size_vk/ko_d2v.model')


arrError = ["без цыганских букавак пожалуйста","ты издеваешься чтоле","сколько можно латиницы я же русский","фу убери","да что с тобой не так","ясно."]


bot = Bot(token='ваш токен')
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет, я подобие витали, задавай свои вопрос")

@dp.message_handler()
async def main_message_handler(msg: types.Message):
    message = msg.text
    vecMessage = []

    message = re.sub('[^А-Яа-яё\s]+', '', message)
    message = ' '.join(message.split())
    if len(message) == 0:
        await bot.send_message(msg.from_user.id, arrError[randint(0, len(arrError) - 1)])
        #print(arrError[randint(0, len(arrError) - 1)])
    else:
        vecMessage.append(model.infer_vector(message.split(' ')))
        sims = model.dv.most_similar(vecMessage, topn=10)

        if sims[0][0] % 2 == 0:
            await bot.send_message(msg.from_user.id, main_data[sims[0][0] + 1])
            #print(main_data[sims[0][0] + 1])
        else:
            if message == main_data[sims[0][0]]:
                check = False
                for k in range(1, 10):
                    if message != main_data[sims[k][0]]:
                        await bot.send_message(msg.from_user.id, main_data[sims[k][0]])
                        #print(main_data[sims[k][0]])
                        check = True
                        break
                if not check:
                    await bot.send_message(msg.from_user.id, main_data[sims[0][0]])
                    #print(main_data[sims[0][0]])
            else:
                await bot.send_message(msg.from_user.id, main_data[sims[randint(0, 2)][0]])
                #print(main_data[sims[randint(0, 2)][0]])
    #await bot.send_message(msg.from_user.id,"сомнительный ответ")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)