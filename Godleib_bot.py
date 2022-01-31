# kittyboyt/kittybot.py
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from telegram import ReplyKeyboardMarkup
import requests
import random
from dotenv import load_dotenv
import os
import app_logger


load_dotenv()

secret_token = os.getenv('TOKEN')

updater = Updater(token=secret_token, use_context=True)


CATS_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://random.dog/woof.json'
FOX_URL = 'https://randomfox.ca/floof/'
SANO = [
    'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-15/e35/p1080x1080/62569922_475831356498386_597951715898557881_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_cat=102&_nc_ohc=Ie-vnzO3kQYAX8fuou5&edm=AABBvjUBAAAA&ccb=7-4&oh=c2b59a6d3223debab19893d3eb1c49db&oe=61493130&_nc_sid=83d603',
    'https://scontent-arn2-1.cdninstagram.com/v/t51.2885-15/e35/32307741_430563424055425_236842587103690752_n.jpg?_nc_ht=scontent-arn2-1.cdninstagram.com&_nc_cat=101&_nc_ohc=yAtkYNWQ5_YAX_nG2zc&edm=AABBvjUBAAAA&ccb=7-4&oh=9ceb9c8791d16938cdd258c8766c0e1e&oe=6148EBC0&_nc_sid=83d603'
]

def buttons():
    buttons = ReplyKeyboardMarkup([
                ['/newcat'], ['/newdog'],
                ['/newfox'],['Смотри, какая...'],
                ['Ну давай, рискни (DANGER, не нажимай сюда!)']
            ],
            resize_keyboard = True
            )
    return buttons


def get_random_pet(pet):
    if pet=='cat':
        try:
            out = requests.get(CATS_URL).json()[0]['url']
        except Exception as error:
            # Печатать информацию в консоль теперь не нужно:
            # всё необходимое будет в логах
            # print(error)
            logger.error(f'Ошибка при запросе к основному API: {error}')
            new_url = 'https://api.thedogapi.com/v1/images/search'
            out = requests.get(new_url).json()[0]['url']
    elif pet=='dog':
        out = requests.get(DOG_URL).json()['url']

    elif pet=='fox':
        out = requests.get(FOX_URL).json()['image']

    #print(out)
    return out


def say_hi(update, context):
    # Получаем информацию о чате, из которого пришло сообщение,
    # и сохраняем в переменную chat
    chat = update.effective_chat
    if update.message.text=='Ну давай, рискни (DANGER, не нажимай сюда!)':
        logger.info('ОНИ СМОТРЯТ НА МЕНЯ!')
        context.bot.send_message(chat_id=chat.id,
                                    text='Ну ты сам этого захотел!')
        context.bot.send_photo(chat.id, 'https://i.ibb.co/RBn9r2D/o-AMix-HQo-Cz-A.jpg')

    elif update.message.text=='Смотри, какая су4ка':
        logger.info('ОНИ СМОТРЯТ НА САНЮ!')
        context.bot.send_message(chat_id=chat.id,
                                    text='По просьбе Сашки...')
        context.bot.send_photo(chat.id, SANO[random.randint(0, len(SANO)-1)])

    else:
        logger.info('Показываем дефолтное сообщение')
        name = update.message.chat.first_name
        # В ответ на любое текстовое сообщение 
        # будет отправлено 'Привет, я KittyBot!'
        context.bot.send_message(chat_id=chat.id,
                                    text=f'Привет {name}, я Godleib!'
                                        f' Я покажу тебе котиков (все же любят кис),'
                                        f'\nНо еще могу собачек или лисичке, кек)',
                                    reply_markup=buttons(),
                                    )

def wake_up(update, context):
    # Каждый вложенный список определяет
    # новый ряд кнопок в интерфейсе бота.
    # Здесь описаны две кнопки в первом ряду и одна - во втором.
    logger.info('Приветствие')
    # В ответ на команду /start 
    # будет отправлено сообщение 'Спасибо, что включили меня'
    chat = update.effective_chat
    #print(update)  # Отправим содержимое update в консоль
    context.bot.send_message(chat_id=chat.id, 
                             text=f'Спасибо, что включили меня, @{chat.username}.'
                                  f' Если хочешь - спроси меня, что я делаю.',
                             # Добавим кнопку в содержимое отправляемого сообщения
                             reply_markup=buttons(),
                             )

# pets={
#     'cat': 'Смотри, какая котейка)',
#     'dog': 'Смотри, какой песель)',
#     'fox': 'Смотри, какая лиса!'
# }

# def new_pet(pet, update, context):
#     chat = update.effective_chat
#     print(update)
#     context.bot.send_message(chat_id=chat.id, 
#                              text=pets[pet]
#                              )
#     context.bot.send_photo(chat.id, get_random_pet(pet))


def new_cat(update, context):
    chat = update.effective_chat
    #print(update)
    if update.message.chat.id==557677465:
        logger.info('Полина детектыд')
        context.bot.send_message(chat_id=chat.id, 
                             text=f'Ага, Полина детектыд!, держи мою фотку!'
                             )
        context.bot.send_photo(chat.id, 'https://i.ibb.co/RBn9r2D/o-AMix-HQo-Cz-A.jpg')
    else:
        logger.info('Отправили кота')
        context.bot.send_message(chat_id=chat.id, 
                                    text=f'Смотри, какая котейка)'
                                    )
        context.bot.send_photo(chat.id, get_random_pet('cat'))

def new_dog(update, context):
    logger.info('Отправили собаку')
    chat = update.effective_chat
    #print(update)
    context.bot.send_message(chat_id=chat.id, 
                             text=f'Смотри, какой песель)'
                             )
    context.bot.send_photo(chat.id, get_random_pet('dog'))

def new_fox(update, context):
    logger.info('Отправили лису')
    chat = update.effective_chat
    #print(update)
    context.bot.send_message(chat_id=chat.id, 
                             text=f'Смотри, какая лиса!'
                             )
    context.bot.send_photo(chat.id, get_random_pet('fox'))

def main():
    # Регистрируется обработчик CommandHandler;
    # он будет отфильтровывать только сообщения с содержимым '/start'
    # и передавать их в функцию wake_up()
    logger.debug('Бот запущен')
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_dog))
    updater.dispatcher.add_handler(CommandHandler('newfox', new_fox))

    # Регистрируется обработчик MessageHandler;
    # из всех полученных сообщений он будет выбирать только текстовые сообщения
    # и передавать их в функцию say_hi()
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    # Метод start_polling() запускает процесс polling, 
    # приложение начнёт отправлять регулярные запросы для получения обновлений.
    updater.start_polling(poll_interval=6.0)
    # Бот будет работать до тех пор, пока не нажмете Ctrl-C
    updater.idle()

if __name__=='__main__':
    logger = app_logger.get_logger(__name__)
    main()
