from telebot import types
from telebot import TeleBot
import folium
import json

bot = TeleBot('5448157489:AAFB43UYy5czZHjSnu1_DncXn6exfXsVlME')

data = {}

admin = 2297660

db_js = json.loads(open('.\db.json', encoding='utf-8').read()) or []

m=folium.Map([35.6892, 51.3890], zoom_start=11)
for n in db_js:
    folium.Marker(location=[float(i) for i in n['3'].split('-')], popup=n['4'],
                  tooltip=json.dumps(n) ,icon=folium.Icon(color='red',
                  icon='cloud')).add_to(m)
m.save('index.html')
@bot.message_handler(commands=['start'])
def start_command_handler(message: types.Message):
    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons.add(types.KeyboardButton('شروع'))

    msg = bot.send_message(message.chat.id,
                          """ سلام وقتتون بخیر باشه. این ربات توسط تیمی از دانشجویان دانشگاه تربیت مدرس طراحی شده
است و جهت جمع آوری اطلاعات مربوط به کانالهای آب سطحی شهر تهران میباشد. همکاری شما کمک شایانی
جهت نظارت هرچه بیشتر بر منابع آبی میباشد""", reply_markup=buttons)

    bot.register_next_step_handler(msg, first)

@bot.message_handler(commands=['help'])
def help_command_handler(message: types.Message):
    bot.send_message(message.chat.id,"""در این ربات تعدادی سوال به شکل گزینه ای و تشریحی مطرح شده است. پس از انتخاب
کانال مورد نظر،پاسخهای مناسب را انتخاب نمایید.""")


def first(message):
    text = message.text
    print(text)

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons.add(types.KeyboardButton('دارآباد'), types.KeyboardButton('دربند'))
    buttons.add(types.KeyboardButton('درکه'), types.KeyboardButton('دیگر نقاط'))
    msg = bot.send_message(message.chat.id, 'لطفا رودخانه مورد بررسی را از میان گزینه ها انتخاب نمایید.',
                               reply_markup=buttons)
    bot.register_next_step_handler(msg, step1)


def step1(message):
    text = message.text
    dic = {1: text}
    data[message.chat.id] = dic

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons.add(types.KeyboardButton('کم'), types.KeyboardButton('متوسط'), types.KeyboardButton('زیاد'))
    msg = bot.send_message(message.chat.id, 'لطفا میزان پسماند تجمع یافته در بستر رودخانه را تعیین نمایید.',
                                reply_markup=buttons)
    bot.register_next_step_handler(msg, step2)


def step2(message):
    text = message.text
    data[message.chat.id][2] = text

    msg = bot.send_message(message.chat.id, 'لطفا لوکیشن محل تجمع پسماند را ارسال نمایید.',
                                reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, step3)


def step3(message):
    text = f'{message.location.latitude}-{message.location.longitude}'
    data[message.chat.id][3] = text

    buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    msg = bot.send_message(message.chat.id, 'در نهایت تصویری از پسماند موجود در کانال آب سطحی موردنظر را ارسال کنید.',
                                reply_markup=buttons)
    bot.register_next_step_handler(msg, step4)


def step4(message):

    msg = bot.send_message(message.chat.id, """از این که دراین پروژه شرکت کردید نهایت تشکر را ازشما داریم.   
    در صورت تمایل لطفااگر پیشنهاد،انتقاد و یا توضیحات بیشتری در رابطه به محل تجمع پسماند دارید، به صورت پیام متنی ارسال نمایید. """)

    file = bot.get_file(message.json['photo'][1]['file_id'])
    downloaded_file = bot.download_file(file.file_path)

    with open(f'pic{message.chat.id}.png', 'wb') as new_file:
        new_file.write(downloaded_file)

    data[message.chat.id][4] = f'pic{message.chat.id}.png'

    db_js.append(data[message.chat.id])
    with open('db.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(db_js, ensure_ascii=False))
        file.close()

    text = ''
    for i in data[message.chat.id]:
        text+=f'{data[message.chat.id][i]}\n'
    bot.send_message(admin, text)
    bot.register_next_step_handler(msg, step5)

    n = data[message.chat.id]
    folium.Marker(location=[float(i) for i in n[3].split('-')], popup=n[4],
                  tooltip=json.dumps(n),icon=folium.Icon(color='red',
                  icon='cloud')).add_to(m)
    m.save('index.html')

def step5(message):
    bot.send_message(admin, message.text)
    msg = bot.send_message(message.chat.id, 'با تشکر')
bot.infinity_polling()













         
         
         
