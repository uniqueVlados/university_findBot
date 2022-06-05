from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


TOKEN = "5353856334:AAHh050ulalH8t_aIUTFN-JUAv99SmiYCeQ"


# FUNCTION
def get_univ(dir, points):
    # information about universities (names of specialties, passing scores and a link to the picture)
    univ_1 = {"Менеджмент МГУ": [260, 280, "img/msu.jpg"],
             "Бизнес-аналитика ВШЭ": [280, 300, "img/hse.jpg"],
             "Управление предприятиями РУДН": [240, 260, "img/rudn.jpg"]}
    univ_2 = {"Экономическое право ФинУниверситет": [260, 280, "img/fin.jpg"],
              "Юриспруденция РГУ нефти и газа": [240, 260, "img/rgu.jpg"],
              "Факультет права ВШЭ": [280, 300, "img/hse.jpg"]}
    univ_3 = {"Физика НИЯУ МИФИ": [260, 280, "img/mifi.jpg"],
              "Прикладная математика МГТУ им. Баумана": [280, 300, "img/mgtu.jpg"],
              "Биохимическая физика СПбГУ": [240, 260, "img/spbgu.jpg"]}
    univ_4 = {"Информационные системы и технологии ИТМО": [260, 280, "img/itmo.jpg"],
              "Информационные системы и телекоммуникации МГТУ им. Баумана": [280, 300, "img/mgtu.jpg"],
              "Информационные системы и технологии в строительстве МГСУ": [240, 260, "img/mgsu.jpg"]}
    univ_list = []
    photo_link = []
    # add to list right universities and right image
    if dir == "Управление и бизнес🤝":
        for u, p in univ_1.items():
            if p[0] <= points <= p[1]:
                univ_list.append(u)
                photo_link.append(p[-1])
    elif dir == "Юриспреденция и право📚":
        for u, p in univ_2.items():
            if p[0] <= points <= p[1]:
                univ_list.append(u)
                photo_link.append(p[-1])
    elif dir == "Физ-мат науки📐":
        for u, p in univ_3.items():
            if p[0] <= points <= p[1]:
                univ_list.append(u)
                photo_link.append(p[-1])
    elif dir == "Информационные технологии🖥":
        for u, p in univ_4.items():
            if p[0] <= points <= p[1]:
                univ_list.append(u)
                photo_link.append(p[-1])
    return univ_list, photo_link


# BUTTONS
DIR_1 = KeyboardButton('Управление и бизнес🤝')
DIR_2 = KeyboardButton('Юриспреденция и право📚')
DIR_3 = KeyboardButton('Физ-мат науки📐')
DIR_4 = KeyboardButton('Информационные технологии🖥')

POINTS_240 = "240-260🌚"
POINTS_260 = "260-280🎓"
POINTS_280 = "280-300🕶"

# KEYBOARDS
KB_DIR = ReplyKeyboardMarkup(resize_keyboard=True)
KB_DIR.add(DIR_1, DIR_2, DIR_3, DIR_4)

KB_POINTS = ReplyKeyboardMarkup(resize_keyboard=True)
KB_POINTS.add(POINTS_240, POINTS_260, POINTS_280)


users = {}


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# bot launch handling
@dp.message_handler(commands=['start'])
async def start_(message: types.Message):
    user_id = str(message.from_user.id)
    # dictionary for each individual user
    users[user_id] = {"dir": None, "points": None, "state_point": False, "photo": None}
    await message.reply(f"Здравствуйте, {message.from_user.first_name}\nЭтот бот поможет Вам выбрать наиболее "
                        f"подходящий вуз по заданной специальности и баллам")
    await message.reply(f"Выберите нужное направление", reply_markup=KB_DIR)


# handling incoming messages
@dp.message_handler()
async def info(message: types.Message):
    user_id = str(message.from_user.id)
    if message.text == 'Управление и бизнес🤝':
        users[user_id]["dir"] = 'Управление и бизнес🤝'
        users[user_id]["state_point"] = True
        await message.reply(f"Выберите кол-во баллов за 3 предмета(ОБЩ/АНГЛ/РУС) или введите ДРУГОЕ(ПРИМЕР: 234)",
                            reply_markup=KB_POINTS)
    if message.text == 'Юриспреденция и право📚':
        users[user_id]["dir"] = 'Юриспреденция и право📚'
        users[user_id]["state_point"] = True
        await message.reply(f"Выберите кол-во баллов за 3 предмета(ОБЩ/ИСТ/РУС) или введите ДРУГОЕ(ПРИМЕР: 234)",
                            reply_markup=KB_POINTS)
    if message.text == 'Физ-мат науки📐':
        users[user_id]["dir"] = 'Физ-мат науки📐'
        users[user_id]["state_point"] = True
        await message.reply(f"Выберите кол-во баллов за 3 предмета(МАТ/ФИЗ/РУС) или введите ДРУГОЕ(ПРИМЕР: 234)",
                            reply_markup=KB_POINTS)
    if message.text == 'Информационные технологии🖥':
        users[user_id]["dir"] = 'Информационные технологии🖥'
        users[user_id]["state_point"] = True
        await message.reply(f"Выберите кол-во баллов за 3 предмета(ИНФ/МАТ/РУС) или введите ДРУГОЕ(ПРИМЕР: 234)",
                            reply_markup=KB_POINTS)
    if users[user_id]["state_point"]:
        if message.text.isdigit():
            users[user_id]["points"] = int(message.text)
            users[user_id]["state_point"] = True
            users[user_id]["photo"] = False
            await message.reply(f'{"".join(get_univ(users[user_id]["dir"], users[user_id]["points"])[0])}',
                                reply_markup=KB_DIR)
            for link in get_univ(users[user_id]["dir"], users[user_id]["points"])[1]:
                await bot.send_photo(user_id, open(link, 'rb'))
        if (message.text == '240-260🌚' or message.text == '260-280🎓' or message.text == '280-300🕶'
            or message.text.isdigit()):
            users[user_id]["points"] = int(message.text.split("-")[0]) + 10
            users[user_id]["state_point"] = False
            users[user_id]["photo"] = False
            await message.reply(f'{"".join(get_univ(users[user_id]["dir"], users[user_id]["points"])[0])}',
                                reply_markup=KB_DIR)
            for link in get_univ(users[user_id]["dir"], users[user_id]["points"])[1]:
                await bot.send_photo(user_id, open(link, 'rb'))


if __name__ == '__main__':
    executor.start_polling(dp)