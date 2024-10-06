import telebot
import random
import sqlite3
from telebot import types

#добавление токена бота
bot = telebot.TeleBot('5810972790:AAHResGdVjnlfUxAq_6rTH4OeRYfwAeFPgw')
#ССЫЛКА НА БОТА: http://t.me/TVTVTVTVBot

#подключение базы данных
conn = sqlite3.connect('glop.db', check_same_thread=False)
cursor = conn.cursor()

#переменные в которые записываются данные пользователя
us_id = 0;
name = '';
surname = '';
addr = ''
age = '';
phn = '';
eml = ''

pp = 0

#функция добавления данных в таблицу из записаных переменных в БД
def db_table_val(id_customer: int, Name: str, Surname: str, Address: str, Age: str, Phone: str, Email: str):
    cursor.execute('INSERT INTO CUSTOMER (id_customer, Name, Surname, Address, Age, Phone, Email) VALUES (?, ?, ?, ?, ?, ?, ?)',
                   (id_customer, Name, Surname, Address, Age, Phone, Email))
    conn.commit()
#ДЕлаем чтоб бот реагировал на команду старт
@bot.message_handler(commands=['start'])
#Функция старта
def start(message):
    #добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💸 Товари")
    btn2 = types.KeyboardButton("👤 Ваш Кабінет")
    btn3 = types.KeyboardButton("🛒 Кошик")
    btn4 = types.KeyboardButton("🔎 Пункти")
    #это делает так чтоб все кнопки были видны в боте
    markup.add(btn1, btn2, btn3, btn4)
    #отправляет сообщение с текстом и кнопки пользователю
    bot.send_message(message.chat.id,
                     text="Ласкаво прошу до нашого МАГАЗИНУ!".format(
                         message.from_user), reply_markup=markup)
#Делаем чтоб бот реагировал на текст от пользователя
@bot.message_handler(content_types=['text'])
#Функція реагування на те який текст буде відправлено користувачем, тобто яка кнопка буде натиснута
def func(message):
    if (message.text == "💸 Товари"):
        #Це вже трохи іщі кнопки які будут у повідомленні а не знизу екрану
        keyboard = types.InlineKeyboardMarkup();  # наша клавіатура
        key_it1 = types.InlineKeyboardButton(text='IPHONE', callback_data='iphone');  # кнопка Виклику товару
        keyboard.add(key_it1);
        key_it2 = types.InlineKeyboardButton(text='MacBook', callback_data='macbook');
        keyboard.add(key_it2);
        key_it3 = types.InlineKeyboardButton(text='IPAD PRO', callback_data='gamanets');
        keyboard.add(key_it3);
        key_it4 = types.InlineKeyboardButton(text='AIRPODS PRO', callback_data='chohol');
        keyboard.add(key_it4);
        key_it5 = types.InlineKeyboardButton(text='AIRPODS MAX', callback_data='mario');
        keyboard.add(key_it5);
        #Отправляет сообщение с кнопками
        question = "🧩 Оберіть товар:"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    elif (message.text == "🔎 Пункти"):
        #Это вывод информации про отделения магазина
        qwerty = "SELECT * FROM ADDRESS"
        cursor.execute(qwerty)
        rows = cursor.fetchall()
        text = "🔋НАШІ ВІДДІЛЕННЯ🪫\n"
        for row in rows:
            text += f"🏢МІСТО: {row[1]}\n📍АДРЕСА: {row[2]} {row[3]} {row[4]}\n🕒РОБОЧІ ГОДИНИ: {row[5]}\n\n"
        bot.send_message(message.chat.id, text)

    elif (message.text == "ГОЛОВНЕ МЕНЮ"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("💸 Товари")
        button2 = types.KeyboardButton("👤 Ваш Кабінет")
        button3 = types.KeyboardButton("🛒 Кошик")
        button4 = types.KeyboardButton("🔎 Пункти")
        markup.add(button1, button2, button3, button4)
        bot.send_message(message.chat.id, text="Ви знов у головному меню", reply_markup=markup)

    elif (message.text == "👤 Ваш Кабінет"):
        #Снова кнопки для управления в моем кабинете
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("📎 Реєстрація")
        btn2 = types.KeyboardButton("📌 Змінити дані")
        btn3 = types.KeyboardButton("📞 Мої дані")
        back = types.KeyboardButton("ГОЛОВНЕ МЕНЮ")
        markup.add(btn1, btn2, btn3, back)
        bot.send_message(message.chat.id, text="ВАШ КАБІНЕТ", reply_markup=markup)
    elif (message.text == "📌 Змінити дані"):
        #Удаляем данные из таблицы по айди пользователя из телеграм
        people_id = message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        #проверяем есть ли такой пользователь
        if data is None:
            bot.send_message(message.chat.id, 'Спочатку зареєструйтесь))')
        else:
            cursor.execute(f"DELETE FROM CUSTOMER WHERE id_customer = {people_id}")
            bot.send_message(message.chat.id, 'Ваші дані очищено! Можете занести нові!')
            conn.commit()
    elif (message.text == "📞 Мої дані"):
        #Вивод данных из таблицы пользователя за айди
        people_id = message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        #так же проверка на налицие пользователя в базе данных
        if data is None:
            bot.send_message(message.chat.id, 'Спочатку зареєструйтесь))')
        else:
            query = f"SELECT * FROM CUSTOMER WHERE id_customer = {people_id}"
            cursor.execute(query)

            rows = cursor.fetchall()
            text = "Ващі дані:\n"
            for row in rows:
                text += f"Ім'я: {row[1]}\nПрізвище: {row[2]}\nВік: {row[4]}\nАдреса: {row[3]}\nНомер телефону: {row[5]}\nПошта: {row[6]}"

            # Отправляем сообщение
            bot.send_message(message.chat.id, text)
    elif (message.text == "🛒 Кошик"):
        #Снова кнопки для управлением Кошиком
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btttn1 = types.KeyboardButton("🔍 Ваші товари")
        btttn2 = types.KeyboardButton("⛔ Звільнити кошик")
        btttn3 = types.KeyboardButton("🚛Замовлення")
        back = types.KeyboardButton("ГОЛОВНЕ МЕНЮ")
        markup.add(btttn1, btttn2, btttn3, back)
        bot.send_message(message.chat.id, text="🔹ВАШ КОШИК🔹", reply_markup=markup)
    elif (message.text == "🔍 Ваші товари"):
        #Смотрим товары какие добавили в Кошик
        people_id = message.chat.id
        cursor.execute(f"SELECT id_customer FROM BASKET WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        #Проверяем за айди пользователя есть ли у него товары
        if data is None:
            bot.send_message(message.chat.id, '❎ ВАШ КОШИК ЩЕ ПУСТИЙ ❎')
        else:
            #вот тут собственно и происходит выбор товаров и их вывод в сообщение
            qwerty = f"SELECT * FROM PRODUCT, BASKET WHERE PRODUCT.ISBN_product_code = BASKET.ISBN_product_code AND id_customer == {people_id}"
            cursor.execute(qwerty)
            rows = cursor.fetchall()
            text = "📦ВАШ КОШИК📦\n"
            for row in rows:
                text += f"📌Назва товару: {row[1]}\n💵Ціна: {row[4]}\n⚖Вага товару: {row[3]}\n\n"
            keyboard = types.InlineKeyboardMarkup();  # наша клавіатура
            orderr = types.InlineKeyboardButton(text='ЗАМОВИТИ', callback_data='order');
            keyboard.add(orderr);
            bot.send_message(message.chat.id, text, reply_markup=keyboard)
    elif (message.text == "⛔ Звільнити кошик"):
        #Удаляем Товары из кошика по айди пользователя
        people_id = message.chat.id
        cursor.execute(f"SELECT id_customer FROM BASKET WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(message.chat.id, '❎ ТОВАРІВ НЕ ЗНАЙДЕНО ❎')
        else:
            cursor.execute(f"DELETE FROM BASKET WHERE id_customer = {people_id}")
            bot.send_message(message.chat.id, "Кошик очищено!")
            conn.commit()
    elif (message.text == "🚛Замовлення"):
        #Выводит данные о заказах пользователя
        people_id = message.chat.id
        qwertyy = f"SELECT * FROM ORDERR, ADDRESS WHERE id_customer == {people_id} AND ORDERR.ID_PUNKT = ADDRESS.ID_PUNKT GROUP BY order_id"
        cursor.execute(qwertyy)
        rows = cursor.fetchall()
        text = "📦ВАШЕ ЗАМОВЛЕННЯ📦\n"
        for row in rows:
            if row[7] == 0:
                st = "ВИКОНУЄТЬСЯ"
                text += f"📌Номер замовлення: {row[0]}\n💵Ціна: {row[4]}\n⚖Вага:{row[5]}\n🗺️Адреса: {row[9]}, {row[10]} {row[11]}\n📪Статус: {st}\n\n"
            if row[7] == 1:
                st = "ГОТОВО"
                text += f"📌Номер замовлення: {row[0]}\n💵Ціна: {row[4]}\n⚖Вага:{row[5]}\n🗺️Адреса: {row[9]}, {row[10]} {row[11]}\n📫Статус: {st}\n\n"
        bot.send_message(message.chat.id, text)
    elif (message.text == "📎 Реєстрація"):
        #Регшестрация пользователя
        #Каждая вункция отвечает за то чтобы автоматически после ответа пользователя на вопрос отправлялось новое сообщение
        people_id = message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            #обявляем нашу п5еременную из начала
            global us_id;
            us_id = message.from_user.id
            bot.send_message(message.from_user.id, "Как тебя зовут?");
            #Это делает чтоб активировалась новая функция
            bot.register_next_step_handler(message, get_name);  # следующий шаг – функция get_name
        else:
            bot.send_message(message.chat.id, 'Вы уже зарегестрированы :)')

def get_name(message):  # получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    age = message.text  # проверяем, что возраст введен корректно
    bot.send_message(message.from_user.id, 'Ваш адрес?');
    bot.register_next_step_handler(message, get_adr);

def get_adr(message):
    global addr;
    addr = message.text
    bot.send_message(message.from_user.id, 'Ваш телефон?');
    bot.register_next_step_handler(message, get_phone);

def get_phone(message):
    global phn;
    phn = message.text
    bot.send_message(message.from_user.id, 'Ваш Емейл?');
    bot.register_next_step_handler(message, get_email);

def get_email(message):
    global eml;
    eml = message.text
    #Проверка введенных данных
    keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes');  # кнопка «Да»
    keyboard.add(key_yes);  # добавляем кнопку в клавиатуру
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебе ' + age + ' лет, тебя зовут ' + name + ' ' + surname + '?\nВаш адресс: ' + addr + '?\nНомер телефона: ' + phn + '?\nЕмеил: ' + eml + '?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)




#Пишем логику для кнопок
@bot.callback_query_handler(func=lambda call: True)
#Для каждой кнопики написана логика лействий, которые она выполняет
#Сначала логика для вывода информации о товарах
def callback_workere(call):
    if call.data == "iphone":  # call.data это callback_data, которую мы указали при объявлении кнопки
        qwerty = "SELECT * FROM 'PRODUCT' WHERE ISBN_product_code == 111"
        cursor.execute(qwerty)
        file = open('фото\iphon.jfif', 'rb')

        rows = cursor.fetchall()
        text = "ІНФОРМАЦІЯ\n"
        for row in rows:
            text += f"Назва товару: {row[1]}\nТип товару: {row[2]}\nВага товару: {row[3]}\nЦіна товару: {row[4]}"
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_zakaz_iphone = types.InlineKeyboardButton(text='Замовити', callback_data='zakaz_iphon');  # кнопка «Да»
        keyboard.add(key_zakaz_iphone);  # добавляем кнопку в клавиатуру
        bot.send_photo(call.message.chat.id, file, text, reply_markup=keyboard)
    elif call.data == "macbook":
        qwerty = "SELECT * FROM 'PRODUCT' WHERE ISBN_product_code == 222"
        cursor.execute(qwerty)
        file = open('фото\macbook.jfif', 'rb')

        rows = cursor.fetchall()
        text = "ІНФОРМАЦІЯ\n"
        for row in rows:
            text += f"Назва товару: {row[1]}\nТип товару: {row[2]}\nВага товару: {row[3]}\nЦіна товару: {row[4]}"
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_zakaz_mcb = types.InlineKeyboardButton(text='Замовити', callback_data='zakaz_mcb');  # кнопка «Да»
        keyboard.add(key_zakaz_mcb);  # добавляем кнопку в клавиатуру
        bot.send_photo(call.message.chat.id, file, text, reply_markup=keyboard)
    elif call.data == "gamanets":
        qwerty = "SELECT * FROM 'PRODUCT' WHERE ISBN_product_code == 333"
        cursor.execute(qwerty)
        file = open('фото\koshelek.webp', 'rb')

        rows = cursor.fetchall()
        text = "ІНФОРМАЦІЯ\n"
        for row in rows:
            text += f"Назва товару: {row[1]}\nТип товару: {row[2]}\nВага товару: {row[3]}\nЦіна товару: {row[4]}"
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_zakaz_gam = types.InlineKeyboardButton(text='Замовити', callback_data='zakaz_gam');  # кнопка «Да»
        keyboard.add(key_zakaz_gam);  # добавляем кнопку в клавиатуру
        bot.send_photo(call.message.chat.id, file, text, reply_markup=keyboard)
    elif call.data == "chohol":
        qwerty = "SELECT * FROM 'PRODUCT' WHERE ISBN_product_code == 444"
        cursor.execute(qwerty)
        file = open('фото\chehol.jpg', 'rb')

        rows = cursor.fetchall()
        text = "ІНФОРМАЦІЯ\n"
        for row in rows:
            text += f"Назва товару: {row[1]}\nТип товару: {row[2]}\nВага товару: {row[3]}\nЦіна товару: {row[4]}"
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_zakaz_choh = types.InlineKeyboardButton(text='Замовити', callback_data='zakaz_choh');  # кнопка «Да»
        keyboard.add(key_zakaz_choh);  # добавляем кнопку в клавиатуру
        bot.send_photo(call.message.chat.id, file, text, reply_markup=keyboard)
    elif call.data == "mario":
        qwerty = "SELECT * FROM 'PRODUCT' WHERE ISBN_product_code == 555"
        cursor.execute(qwerty)
        file = open('фото\mario.jpg', 'rb')

        rows = cursor.fetchall()
        text = "ІНФОРМАЦІЯ\n"
        for row in rows:
            text += f"Назва товару: {row[1]}\nТип товару: {row[2]}\nВага товару: {row[3]}\nЦіна товару: {row[4]}"
        keyboard = types.InlineKeyboardMarkup();  # наша клавиатура
        key_zakaz_mario = types.InlineKeyboardButton(text='Замовити', callback_data='zakaz_mario');  # кнопка «Да»
        keyboard.add(key_zakaz_mario);  # добавляем кнопку в клавиатуру
        bot.send_photo(call.message.chat.id, file, text, reply_markup=keyboard)
    #ТУт ответ на регистрацию
    elif call.data == "yes":  # call.data это callback_data, которую мы указали при объявлении кнопки
        db_table_val(id_customer=us_id, Name=name, Surname=surname, Address=addr, Age=age, Phone=phn, Email=eml)
        bot.send_message(call.message.chat.id, 'Запомню : )');
        conn.commit()
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Спробуйте зареєструватись ще раз!");
    #Довабляем товары в кошик
    elif call.data == "zakaz_iphon":
        people_id = call.message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(call.message.chat.id, 'СПОЧАТКУ ЗАРЕЄСТРУЙТЕСЬ')
        else:
            ISBN = 111
            num = 1
            people_id = call.message.chat.id
            cursor.execute('INSERT INTO BASKET (id_customer, ISBN_product_code, NumberofThings) VALUES(?, ?, ?)', (people_id, ISBN, num))
            cursor.execute(f'UPDATE BASKET SET Price = PRODUCT.Price, Weight = PRODUCT.Weight FROM PRODUCT WHERE BASKET.ISBN_product_code = PRODUCT.ISBN_product_code')
            bot.send_message(call.message.chat.id, "Товар додано до кошику!");
            conn.commit()
    elif call.data == "zakaz_mcb":
        people_id = call.message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(call.message.chat.id, 'СПОЧАТКУ ЗАРЕЄСТРУЙТЕСЬ')
        else:
            ISBN = 222
            num = 1
            people_id = call.message.chat.id
            cursor.execute('INSERT INTO BASKET (id_customer, ISBN_product_code, NumberofThings) VALUES(?, ?, ?)', (people_id, ISBN, num))
            cursor.execute(f'UPDATE BASKET SET Price = PRODUCT.Price, Weight = PRODUCT.Weight FROM PRODUCT WHERE BASKET.ISBN_product_code = PRODUCT.ISBN_product_code')
            bot.send_message(call.message.chat.id, "Товар додано до кошику!");
            conn.commit()
    elif call.data == "zakaz_gam":
        people_id = call.message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(call.message.chat.id, 'СПОЧАТКУ ЗАРЕЄСТРУЙТЕСЬ')
        else:
            ISBN = 333
            num = 1
            people_id = call.message.chat.id
            cursor.execute('INSERT INTO BASKET (id_customer, ISBN_product_code, NumberofThings) VALUES(?, ?, ?)', (people_id, ISBN, num))
            cursor.execute(f'UPDATE BASKET SET Price = PRODUCT.Price, Weight = PRODUCT.Weight FROM PRODUCT WHERE BASKET.ISBN_product_code = PRODUCT.ISBN_product_code')
            bot.send_message(call.message.chat.id, "Товар додано до кошику!");
            conn.commit()
    elif call.data == "zakaz_choh":
        people_id = call.message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(call.message.chat.id, 'СПОЧАТКУ ЗАРЕЄСТРУЙТЕСЬ')
        else:
            ISBN = 444
            num = 1
            people_id = call.message.chat.id
            cursor.execute('INSERT INTO BASKET (id_customer, ISBN_product_code, NumberofThings) VALUES(?, ?, ?)', (people_id, ISBN, num))
            cursor.execute(f'UPDATE BASKET SET Price = PRODUCT.Price, Weight = PRODUCT.Weight FROM PRODUCT WHERE BASKET.ISBN_product_code = PRODUCT.ISBN_product_code')
            bot.send_message(call.message.chat.id, "Товар додано до кошику!");
            conn.commit()
    elif call.data == "zakaz_mario":
        people_id = call.message.chat.id
        cursor.execute(f"SELECT id_customer FROM CUSTOMER WHERE id_customer = {people_id}")
        data = cursor.fetchone()
        if data is None:
            bot.send_message(call.message.chat.id, 'СПОЧАТКУ ЗАРЕЄСТРУЙТЕСЬ')
        else:
            ISBN = 555
            num = 1
            people_id = call.message.chat.id
            cursor.execute('INSERT INTO BASKET (id_customer, ISBN_product_code, NumberofThings) VALUES(?, ?, ?)', (people_id, ISBN, num))
            cursor.execute(f'UPDATE BASKET SET Price = PRODUCT.Price, Weight = PRODUCT.Weight FROM PRODUCT WHERE BASKET.ISBN_product_code = PRODUCT.ISBN_product_code')
            bot.send_message(call.message.chat.id, "Товар додано до кошику!");
            conn.commit()
    #Заказ товаров из кошика
    elif call.data == "order":
        #Добавление кнопок для выбора отделения
        keyboard = types.InlineKeyboardMarkup();  # наша клавіатура
        city1 = types.InlineKeyboardButton(text='ХАРКІВ', callback_data='harkiv');
        keyboard.add(city1);
        city2 = types.InlineKeyboardButton(text='ДНІПРО', callback_data='dnipro');
        keyboard.add(city2);
        city3 = types.InlineKeyboardButton(text='КИЇВ', callback_data='kiev');
        keyboard.add(city3);
        question = "🏙ОБЕРІТЬ ПУНКТ🏙"
        bot.send_message(call.message.chat.id, text=question, reply_markup=keyboard)
    #Сотря какое отделение выбрано такое отделение будет добавлено в заказ
    elif call.data == "harkiv":
        people_id = call.message.chat.id
        #РАндомное число в номер заказа ставиться
        random_numberss = random.randint(1, 1000)
        cursor.execute(f"INSERT INTO ORDERR (id_customer, ISBN_product_code, Total_price, Total_weight, Quantity) SELECT id_customer, ISBN_product_code, SUM(Price) as Total_price, SUM(Weight) as Total_weight, SUM(NumberofThings) as Quantity FROM BASKET WHERE id_customer = {people_id} GROUP BY ISBN_product_code")
        #Из за того что нельзя одновременно вносить данные из таблиц и от пользователя то сначала вносим данные из таблтицы а потом обновляем от пользователя
        cursor.execute(
            f"UPDATE ORDERR SET ID_PUNKT = {1}, order_id = {random_numberss}, Status = FALSE WHERE order_id IS NULL AND id_customer = {people_id}")
        cursor.execute("INSERT INTO admin (Status, order_id) VALUES(?, ?)", (False, random_numberss))
        #Очищаем кошик
        cursor.execute(f"DELETE FROM BASKET WHERE id_customer = {people_id}")
        conn.commit()
        qwerty = f"SELECT order_id, SUM(Total_price), SUM(Total_weight), Status FROM ORDERR WHERE id_customer == {people_id} AND order_id = {random_numberss}"
        cursor.execute(qwerty)
        rows = cursor.fetchall()
        #Вывод данных
        text = "📦ВАШЕ ЗАМОВЛЕННЯ📦\n"

        for row in rows:
            if row[3] == 0:
                st = "ВИКОНУЄТЬСЯ"
                text += f"📌Номер замовлення: {row[0]}\n💵Ціна: {row[1]}\n⚖Вага:{row[2]}\n📪Статус: {st}"
        bot.send_message(call.message.chat.id, text)
    elif call.data == "dnipro":
        people_id = call.message.chat.id
        random_numberss = random.randint(1, 1000)
        cursor.execute(f"INSERT INTO ORDERR (id_customer, ISBN_product_code, Total_price, Total_weight, Quantity) SELECT id_customer, ISBN_product_code, SUM(Price) as Total_price, SUM(Weight) as Total_weight, SUM(NumberofThings) as Quantity FROM BASKET WHERE id_customer = {people_id} GROUP BY ISBN_product_code")
        cursor.execute(f"UPDATE ORDERR SET ID_PUNKT = {2}, order_id = {random_numberss}, Status = FALSE WHERE order_id IS NULL AND id_customer = {people_id}")
        cursor.execute("INSERT INTO admin (Status, order_id) VALUES(?, ?)", (False, random_numberss))
        cursor.execute(f"DELETE FROM BASKET WHERE id_customer = {people_id}")
        conn.commit()
        qwerty = f"SELECT order_id, SUM(Total_price), SUM(Total_weight), Status FROM ORDERR WHERE id_customer == {people_id} AND order_id = {random_numberss}"
        cursor.execute(qwerty)
        rows = cursor.fetchall()
        text = "📦ВАШЕ ЗАМОВЛЕННЯ📦\n"
        for row in rows:
            if row[3] == 0:
                st = "ВИКОНУЄТЬСЯ"
                text += f"📌Номер замовлення: {row[0]}\n💵Ціна: {row[1]}\n⚖Вага:{row[2]}\n📪Статус: {st}"
        bot.send_message(call.message.chat.id, text)
    elif call.data == "kiev":
        people_id = call.message.chat.id
        random_numberss = random.randint(1, 1000)
        cursor.execute(f"INSERT INTO ORDERR (id_customer, ISBN_product_code, Total_price, Total_weight, Quantity) SELECT id_customer, ISBN_product_code, SUM(Price) as Total_price, SUM(Weight) as Total_weight, SUM(NumberofThings) as Quantity FROM BASKET WHERE id_customer = {people_id} GROUP BY ISBN_product_code")
        cursor.execute(
            f"UPDATE ORDERR SET ID_PUNKT = {3}, order_id = {random_numberss}, Status = FALSE WHERE order_id IS NULL AND id_customer = {people_id}")
        cursor.execute("INSERT INTO admin (Status, order_id) VALUES(?, ?)", (False, random_numberss))
        cursor.execute(f"DELETE FROM BASKET WHERE id_customer = {people_id}")
        conn.commit()
        qwerty = f"SELECT order_id, SUM(Total_price), SUM(Total_weight), Status FROM ORDERR WHERE id_customer == {people_id} AND order_id = {random_numberss}"
        cursor.execute(qwerty)
        rows = cursor.fetchall()
        text = "📦ВАШЕ ЗАМОВЛЕННЯ📦\n"

        for row in rows:
            if row[3] == 0:
                st = "ВИКОНУЄТЬСЯ"
                text += f"📌Номер замовлення: {row[0]}\n💵Ціна: {row[1]}\n⚖Вага:{row[2]}\n📪Статус: {st}"
        bot.send_message(call.message.chat.id, text)
bot.polling(none_stop=True)