import telebot
import datetime

import time #с помощью него можно останавливать бот на 60 минут, например
import threading #создает потоки
import random #для генерации случайного факта


bot = telebot.TeleBot("6847858152:AAF6pptRJFoea_9TYXN5jrMf5fDwiiYWh4U")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, 'Здравствуй! Я чат-бот, который будет напоминать тебе про измерение давления.')
    reminder_thread = threading.Thread(target=set_reminder, args=(message.chat.id,))
    reminder_thread.start()


measuring_pressure = False
measured_pressure = 0
def pressure_reminder(chat_id):
    global measuring_pressure
    bot.send_message(chat_id, "Время измерить давление. Какой результат измерения?")
    measuring_pressure = True

def send_buttons(message):
    global medicine
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row('Хорошо', 'Описание лекарства')
    markup1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup1.row('Хорошо', 'Выбрать действие')
    if measured_pressure > 130:
        medicine = random.choice(list(medicine_brandname.keys()))
        bot.send_message(message.chat.id, f"Давление повышенное ({measured_pressure}). Выпейте лекарство {medicine}.",
                         reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"Давление в норме ({measured_pressure}). Пока ничего принимать не нужно.",
                         reply_markup=markup1)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global measuring_pressure, measured_pressure
    if measuring_pressure:
        if message.text.isdigit() and int(message.text) >= 0:
            measured_pressure = int(message.text)
            measuring_pressure = False
            send_buttons(message)
        else:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное число для измерения давления.")
    else:
        if message.text == '/start':
            start_message(message)
        elif message.text == 'Хорошо' or message.text == 'Это всё' or message.text == 'Завершить':
            bot.send_message(message.chat.id, "До встречи в " + get_next_reminder() + " !\n\nЧтобы посмотреть список действий, напечатайте любой символ.")
        elif message.text == 'Описание лекарства':
            global medicine
            if medicine in medicine_brandname:
                markup3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup3.row('Это всё', 'Меню')
                bot.send_message(message.chat.id, f"Название: {medicine}\n\nОписание: {medicine_brandname[medicine][0]}\n\nТип: {medicine_brandname[medicine][1]}\n\nЧтобы вернуться к списку действий, выберите 'Меню'.", reply_markup=markup3)


            else:
                bot.send_message(message.chat.id, "Про какое лекарство?")
        elif message.text.lower() in [medicine.lower() for medicine in medicine_brandname]:
            for medicine in medicine_brandname:
                if medicine.lower() == message.text.lower():
                    markup3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
                    markup3.row('Это всё', 'Меню')
                    bot.send_message(message.chat.id, f"Название: {medicine}\n\nОписание: {medicine_brandname[medicine][0]}\n\nТип: {medicine_brandname[medicine][1]}\n\nЧтобы вернуться к списку действий, введите 'Меню'.", reply_markup=markup3)
                    break

        elif message.text == 'Совет':
            markup3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup3.row('Это всё', 'Меню')
            bot.send_message(message.chat.id, random.choice(tips_for_lowering_blood_pressure), reply_markup=markup3)
        elif message.text == 'Лекарства':
            medicine_names = '\n'.join(medicine_brandname.keys()) #является строкой, содержащей все названия лекарств из словаря medicine_brandname, разделенные символом новой строки.
            bot.send_message(message.chat.id, f'Про какое лекарство Вы хотите узнать?\n\n{medicine_names}')


        else:

            markup2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup2.row('Лекарства', 'Совет', "Завершить")
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup2)





#Setting reminders
now = datetime.datetime.now()
first_rem = '03:05'
second_rem = '03:06'
third_rem = '03:07'
fourth_rem = '03:08'


def get_next_reminder():
    now = datetime.datetime.now()
    current_time = now.strftime('%H:%M')

    if current_time < first_rem:
        return first_rem
    elif current_time < second_rem:
        return second_rem
    elif current_time < third_rem:
        return third_rem
    else:
        return fourth_rem

def set_reminder(chat_id):

    while True:
        #Этот код работает, когда устанавливаем напоминания в виде времени
        now = datetime.datetime.now().strftime('%H:%M')
        if now == first_rem or now == second_rem or now == third_rem or now == fourth_rem:
            pressure_reminder(chat_id)
            time.sleep(61)  # задерживаем на 61 секунду, так как иначе сообщение будет повторятся всю полную минуту.
        time.sleep(1)  # чтобы следующая итерация цикла начала работать черррез секунду





#@bot.message_handler(commands=['fact'])

#def fact_message(message):
types_of_medicines = [
                      "Диуретики. Эти препараты помогают почкам вывести лишнюю соль и воду из организма, уменьшая объем крови и снижая артериальное давление.",
                      "Бета-блокаторы. Эти препараты уменьшают частоту сердечных сокращений и силу сокращения сердца, что приводит к снижению артериального давления",
                      "Ингибиторы АПФ (ангиотензин-превращающего фермента). Эти препараты блокируют действие ангиотензин-превращающего фермента, что приводит к расширению сосудов и снижению артериального давления.",
                      "Антагонисты рецепторов ангиотензина II. Эти препараты также расширяют сосуды и снижают артериальное давление, блокируя действие ангиотензин II.",
                      "Кальциевые антагонисты. Эти препараты помогают расслабить сосуды, что снижает артериальное давление."
                     ]
medicine_brandname = {"Гидрохлортиазид":["Это тиазидный диуретик, который увеличивает выведение соли и воды через почки, что помогает снизить кровяное давление.\n\nПолная инструкция по ссылкеhttps://www.vidal.ru/drugs/hydrochlorothiazide__4402", types_of_medicines[0]],
                      "Фуроземид":["Это петлевой диуретик, который увеличивает выведение соли и воды.\n\nПолная инструкция по ссылке https://www.vidal.ru/drugs/furosemid__3038", types_of_medicines[0]],
                      "Метопролол":["Этот препарат блокирует действие адреналина на сердечно-сосудистую систему, что снижает частоту сердечных сокращений и силу сокращения сердца, что приводит к снижению кровяного давления. \n\nПолная инструкция по ссылкеhttps://www.vidal.ru/drugs/metoprolol__24233", types_of_medicines[1]],
                      "Атенолол":["Блокирует бета-адренорецепторы, которые приводят к снижению кровяного давления. \n\nПолная инструкция по ссылке https://www.vidal.ru/drugs/atenolol__1296", types_of_medicines[1]],
                      "Эналаприл":["Этот препарат блокирует действие ангиотензин-превращающего фермента, что приводит к расширению сосудов и снижению кровяного давления. \n\nПолная инструкция по ссылке https://www.vidal.ru/drugs/enalapril__3775", types_of_medicines[2]],
                      "Лизиноприл":["Аналогично эналаприлу, этот препарат также ингибирует ангиотензин-превращающий фермент для снижения кровяного давления.\n\nПолная инструкция по ссылке https://www.vidal.ru/drugs/lisinopril__13042", types_of_medicines[2]],
                      "Лозартан":["Этот препарат блокирует действие ангиотензин II, что приводит к расширению сосудов и снижению кровяного давления. \n\nПолная инструкция по ссылке https://apteka.ru/product/lozartan-kanon-100-mg-60-sht-tabletki-pokrytye-plenochnoj-obolochkoj-5e326c44ca7bdc000192eda5/", types_of_medicines[3]],
                      "Валсартан":["Этот препарат блокирует действие ангиотензин II, что приводит к расширению сосудов и снижению кровяного давления.\n\nПолная инструкция по ссылке https://apteka.ru/product/valsartan-sz-80-mg-30-sht-tabletki-pokrytye-plenochnoj-obolochkoj-blister-5fcdf83f5af2c40001a1dbfe/", types_of_medicines[3]],
                      "Амлодипин":["Этот препарат блокирует вход кальция в сосудистые гладкие мышцы и миокард, что приводит к их расслаблению и снижению кровяного давления.\n\nПолная инструкция по ссылке https://apteka.ru/product/amlodipin-10-mg-90-sht-tabletki-banka-602e3eaf152591d9cd4dc736/", types_of_medicines[4]],
                      "Дилтиазем": ["Еще один кальциевый антагонист, используемый для снижения кровяного давления путем блокирования входа кальция в клетки сердца и сосудов.\n\nПолная инструкция по ссылке https://www.vidal.ru/drugs/diltiazem__4614", types_of_medicines[4]]
                      }

#Советы по сдерживанию давления
tips_for_lowering_blood_pressure = [
    " Поддерживайте здоровый вес и следите за своим индексом массы тела (ИМТ).",
    " Упражняйтесь регулярно - стремитесь к 150 минутам умеренной активности в неделю.",
    " Питайтесь здоровой, сбалансированной диетой с ограничением соли и жира.",
    " Ограничьте потребление алкоголя до умеренных количеств (не более одного напитка в день для женщин и двух для мужчин).",
    " Избегайте курения и контролируйте уровень потребления кофеина.",
    " Практикуйте методы расслабления, такие как медитация, глубокое дыхание или йога.",
    " Соблюдайте регулярные интервалы приема пищи и избегайте переедания.",
    " Поддерживайте здоровый режим сна, стремясь к 7-9 часам сна в ночь.",
    " Управляйте стрессом, обращая внимание на свои эмоции и практикуя техники релаксации.",
    " Измеряйте свое давление регулярно и ведите журнал, чтобы отслеживать его изменения.",
    " Следите за своим уровнем холестерина и сахара в крови.",
    " Потребляйте достаточное количество калия, магния и кальция в вашей диете.",
    " Избегайте процессированных продуктов и предпочитайте свежие фрукты, овощи и злаки.",
    " Уменьшите потребление пищевых добавок и процессированных продуктов.",
    " Следите за артериальным давлением у членов вашей семьи и обсудите их историю болезни с вашим врачом.",
    " Учитывайте побочные эффекты лекарств, которые вы принимаете, и обсудите их со своим врачом.",
    " Избегайте излишнего употребления кулинарии, консервантов и красителей.",
    " Поддерживайте правильную осанку и избегайте длительного сидения.",
    "Сократите потребление быстрых углеводов и продуктов с высоким содержанием сахара.",
    "Обсудите любые изменения в вашем образе жизни или симптомах с вашим врачом немедленно."
]



bot.polling(none_stop=True)
