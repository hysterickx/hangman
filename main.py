# ====================
# РАЗДЕЛ 1. ВЫЗОВ МОДУЛЕЙ, СОЗДАНИЕ ОКНА ПРОГРАММЫ, КЛЮЧЕВЫЕ ПЕРЕМЕННЫЕ
# ====================

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from random import choice

ctk.set_appearance_mode ('dark')

app = ctk.CTk()
app.title ('hangman')
app.geometry ('600x500+800+450')
app.resizable (False, False)
app.attributes ('-alpha', 0.9)

main = ctk.CTkFrame(app)
main.pack(fill = 'both', expand = True)

farewell = ['До новых встреч!', 'Заглядывай ко мне ещё!', 'Был рад поработать с тобой!', 'Ты это, заходи, если что...', 'Надеюсь, еще увидимся!']
repeating = ['Генерирую цикл...', 'Создаю всё с нуля...', 'Очищаю всё лишнее...', 'Отлично! Начинаем...', 'Дай мне пару секундочек...']
right_answers = ['Верно!', 'Отлично!', 'Так держать!', 'Прямо в точку', 'Угадал!']
wrong_answers = ['Мимо', 'Не верно', 'Не угадал', 'Не-а', 'Не то']
chars = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
words = ['человек', 'работа', 'вопрос', 'сторона', 'страна', 'случай', 'голова', 'ребенок', 'система', 'отношение',
'женщина', 'деньги', 'машина', 'проблема', 'решение', 'история', 'власть', 'тысяча', 'возможность', 'результат',
'область', 'статья', 'компания', 'группа', 'развитие', 'процесс', 'условие', 'средство', 'начало', 'уровень', 'минута',
'качество', 'дорога', 'действие', 'государство', 'любовь', 'взгляд', 'общество', 'деятельность', 'организация',
'президент', 'комната', 'порядок', 'момент', 'письмо', 'помощь', 'ситуация', 'состояние', 'квартира', 'внимание', 'смерть',
'программа', 'задача', 'предприятие', 'разговор', 'правительство', 'производство', 'информация', 'положение', 'интерес',
'федерация', 'правило', 'управление', 'мужчина', 'партия', 'сердце', 'движение', 'материал', 'неделя', 'чувство', 'газета',
'причина', 'основа', 'товарищ', 'культура', 'данные', 'мнение', 'документ', 'институт', 'проект', 'встреча', 'директор',
'служба', 'судьба', 'девушка', 'очередь', 'состав', 'количество', 'событие', 'объект', 'создание', 'значение', 'период',
'искусство', 'структура', 'пример', 'исследование', 'гражданин', 'начальник', 'принцип', 'воздух', 'характер', 'борьба',
'использование', 'размер', 'образование', 'мальчик', 'представитель', 'участие', 'девочка', 'политика', 'картина', 'доллар',
'территория', 'изменение', 'направление', 'рисунок', 'течение', 'церковь', 'население', 'большинство', 'музыка',
'правда', 'свобода', 'память', 'команда', 'договор', 'дерево', 'хозяин', 'природа', 'телефон', 'позиция', 'писатель',
'самолет', 'солнце', 'спектакль', 'способ', 'журнал', 'руководитель', 'специалист', 'оценка', 'регион', 'процент',
'родитель', 'требование', 'основание', 'половина', 'анализ', 'автомобиль', 'экономика', 'литература', 'бумага', 'степень',
'господин', 'надежда', 'предмет', 'руководство', 'площадь', 'режиссер', 'поверхность', 'ощущение', 'станция', 'революция',
'колено', 'министерство', 'стекло']

# ====================
# РАЗДЕЛ 2. ФУНКЦИИ - ИСПОЛНИТЕЛИ
# ====================

def start_game():

    if '__' not in page3.word_label.cget('text'):

        page5.label.configure(text = choice(repeating))

        switch_to(page5)

        page3.word = choice(words).upper()
        words.remove(page3.word.lower())
        parts = ['stand', 'head', 'neck', 'left_hand', 'right_hand', 'body', 'left_leg', 'right_leg']

        page3.button_end.place_forget()
        page3.button_repeat.place_forget()
        page3.win_label.place_forget()
        page3.lose_label.place_forget()

        base = ['__' for i in page3.word]
        base[0] = page3.word[0]
        base[-1] = page3.word[-1]
        page3.word_label.configure(text = base)

        for i in parts:
            page3.canvas.itemconfig(i, state = 'hidden')

        check_char.it_was = ''
        create_word.error_count = 8
        page3.count_label.configure(text = f'Попыток осталось:\n{create_word.error_count}')

        page3.entry.place(relx = 0.5, rely = 0.7, anchor = 'c')
        page3.button_input.place(relx = 0.8, rely = 0.7, anchor = 'c')
        page3.button_back.place(relx = 0.2, rely = 0.7, anchor = 'c')

        page5.after(5000, lambda: switch_to(page3))
        page3.after(200, lambda: page3.entry.focus_force())

    else:
        switch_to(page3)

def to_end():
    switch_to(page4)
    page4.after(5000, app.destroy)

def switch_to(page):
    for child in main.winfo_children():
        child.pack_forget()
    page.pack(fill = 'both', expand = True)

def check_char():
    input = page3.entry.get().upper()
    entry = page3.entry

    if not hasattr(check_char, 'it_was'):
        check_char.it_was = ''

    if len(input) == 0:
        error = CTkMessagebox (app, width = 300, height = 150, title = 'Ошибочка', message = 'Поле пустое',
        icon = 'info', justify = 'center', button_color = '#ffffff', button_hover_color = '#66ff33', button_text_color = '#000000')
        app.wait_window(error)
        entry.focus_force()

    elif len(input) > 1:
        error = CTkMessagebox (app, width = 300, height = 150, title = 'Ошибочка', message = 'Нужно ввести только одну букву',
        icon = 'info', justify = 'center', button_color = '#ffffff', button_hover_color = '#66ff33', button_text_color = '#000000')
        entry.delete (0, 'end')
        app.wait_window(error)
        entry.focus_force()

    elif input not in chars:
        error = CTkMessagebox (app, width = 300, height = 150, title = 'Ошибочка', message = 'Нужно ввести одну букву русского алфавита',
        icon = 'info', justify = 'center', button_color = '#ffffff', button_hover_color = '#66ff33', button_text_color = '#000000')
        entry.delete (0, 'end')
        app.wait_window(error)
        entry.focus_force()

    elif input in check_char.it_was:
        error = CTkMessagebox (app, width = 300, height = 150, title = 'Ошибочка', message = 'Ты уже вводил эту букву',
        icon = 'info', justify = 'center', button_color = '#ffffff', button_hover_color = '#66ff33', button_text_color = '#000000')
        entry.delete (0, 'end')
        app.wait_window(error)
        entry.focus_force()
    else:
        check_char.it_was += input
        create_word()

def create_word():
    word = page3.word
    input = page3.entry.get().upper()
    entry = page3.entry
    text = page3.word_label.cget('text')
    parts = ['stand', 'head', 'neck', 'left_hand', 'right_hand', 'body', 'left_leg', 'right_leg']

    for i in range(len(word)):
        if input == word[i]:
            text[i] = input

    if not hasattr(create_word, 'error_count'):
        create_word.error_count = 8

    if input in word[1:-1] and '__' in text:
        page3.word_label.configure(text = text)
        page3.comment_label.configure(text = choice(right_answers))
        entry.delete (0, 'end')

    if input in word[1:-1] and '__' not in text:
        page3.word_label.configure(text = text, text_color = '#66ff33')
        page3.entry.place_forget()
        page3.button_back.place_forget()
        page3.button_input.place_forget()
        page3.comment_label.configure(text = '')
        page3.button_end.place(relx = 0.35, rely = 0.9, anchor = 'c')
        page3.button_repeat.place(relx = 0.65, rely = 0.9, anchor = 'c')
        page3.win_label.place(relx = 0.5, rely = 0.7, anchor = 'c')
        entry.delete (0, 'end')

    if input not in word[1:-1] and create_word.error_count > 0:
        create_word.error_count -= 1
        page3.count_label.configure(text = f'Попыток осталось:\n{create_word.error_count}')
        page3.comment_label.configure(text = choice(wrong_answers))
        current_step = parts[7 - create_word.error_count]
        page3.canvas.itemconfig(current_step, state = 'normal')
        entry.delete (0, 'end')

    if input not in word[1:-1] and create_word.error_count == 0:

        for j in range(len(text)):
            if text[j] == '__':
                text[j] = word[j]

        page3.word_label.configure(text = text, text_color = '#66ff33')
        page3.entry.place_forget()
        page3.button_back.place_forget()
        page3.button_input.place_forget()
        page3.comment_label.configure(text = '')
        page3.lose_label.place(relx = 0.5, rely = 0.7, anchor = 'c')
        page3.button_end.place(relx = 0.35, rely = 0.9, anchor = 'c')
        page3.button_repeat.place(relx = 0.65, rely = 0.9, anchor = 'c')
        entry.delete (0, 'end')

# ====================
# РАЗДЕЛ 3. ФУНКЦИИ - СТРОИТЕЛИ
# ====================

def create_page1(main):
    frame1 = ctk.CTkFrame(main, fg_color = '#0d0d0d')
    frame1.pack(fill = 'both', expand = True)

    label = ctk.CTkLabel (frame1, text = 'Приветствую!',
    font = ('Constantia', 30), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.3, anchor = 'c')

    label = ctk.CTkLabel (frame1, text = 'Это игра "Виселица"',
    font = ('Constantia', 27), text_color = '#ffffff')
    label.place(relx = 0.5, rely = 0.45, anchor = 'c')

    label = ctk.CTkLabel (frame1, text = 'Сыграем?',
    font = ('Constantia', 27), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.6, anchor = 'c')

    button = ctk.CTkButton (frame1, height = 50, corner_radius = 50, text = 'Вперёд!', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = lambda: switch_to(page2))
    button.place(relx = 0.65, rely = 0.8, anchor = 'c')

    button = ctk.CTkButton (frame1, height = 50, corner_radius = 50, text = 'Не сейчас', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 20), command = to_end)
    button.place(relx = 0.35, rely = 0.8, anchor = 'c')

    return frame1

def create_page2(main):
    frame2 = ctk.CTkFrame(main, fg_color = '#0d0d0d')
    frame2.pack(fill = 'both', expand = True)

    label = ctk.CTkLabel (frame2, text = 'Правила очень просты:',
    font = ('Constantia', 25), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.1, anchor = 'c')

    label = ctk.CTkLabel (frame2, text = 'Программа загадывает русскоязычное слово',
    font = ('Constantia', 25), text_color = '#ffffff')
    label.place(relx = 0.5, rely = 0.25, anchor = 'c')

    label = ctk.CTkLabel (frame2, text = 'А тебе нужно его отгадать, вводя по одной букве',
    font = ('Constantia', 23), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.4, anchor = 'c')

    label = ctk.CTkLabel (frame2, text = 'У тебя есть право только на 8 ошибок',
    font = ('Constantia', 25), text_color = '#ffffff')
    label.place(relx = 0.5, rely = 0.55, anchor = 'c')

    label = ctk.CTkLabel (frame2, text = 'Иначе человечка повесят',
    font = ('Constantia', 25), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.7, anchor = 'c')

    button = ctk.CTkButton (frame2, height = 50, corner_radius = 50, text = 'Всё понятно', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = start_game)
    button.place(relx = 0.5, rely = 0.85, anchor = 'c')

    return frame2

def create_page3(main):
    frame3 = ctk.CTkFrame(main, fg_color = '#0d0d0d')
    frame3.pack(fill = 'both', expand = True)

    frame3.word = None

    frame3.canvas = ctk.CTkCanvas(frame3, bg = '#0d0d0d', highlightthickness = 0)
    frame3.canvas.place(relx = 0.05, rely = 0.05, relwidth = 0.4, relheight = 0.5)

    frame3.canvas.create_line(50, 350, 50, 20, fill = 'white', tags = ('stand'), state = 'hidden')
    frame3.canvas.create_line(50, 20, 250, 20, fill = 'white', tags = ('stand'), state = 'hidden')
    frame3.canvas.create_line(250, 20, 250, 100, fill = 'white', tags = ('stand'), state = 'hidden')
    frame3.canvas.create_oval(230, 100, 270, 140, outline = 'white', tags = ('head'), state = 'hidden')
    frame3.canvas.create_line(250, 140, 250, 170, fill = 'white', tags = ('neck'), state = 'hidden')
    frame3.canvas.create_line(250, 170, 200, 200, fill = 'white', tags = ('left_hand'), state = 'hidden')
    frame3.canvas.create_line(250, 170, 300, 200, fill = 'white', tags = ('right_hand'), state = 'hidden')
    frame3.canvas.create_line(250, 170, 250, 250, fill = 'white', tags = ('body'), state = 'hidden')
    frame3.canvas.create_line(250, 250, 200, 280, fill = 'white', tags = ('left_leg'), state = 'hidden')
    frame3.canvas.create_line(250, 250, 300, 280, fill = 'white', tags = ('right_leg'), state = 'hidden')

    frame3.count_label = ctk.CTkLabel (frame3, text = None,
    font = ('Constantia', 25), text_color = '#66ff33')
    frame3.count_label.place(relx = 0.7, rely = 0.3, anchor = 'c')

    frame3.word_label = ctk.CTkLabel (frame3, text = '',
    font = ('Constantia', 25), text_color = '#ffffff')
    frame3.word_label.place(relx = 0.5, rely = 0.55, anchor = 'c')

    frame3.entry = ctk.CTkEntry (frame3, width = 100, height = 30, corner_radius = 40, justify = 'c', text_color = '#66ff33',
    font = ('Cambria', 27))
    frame3.entry.place(relx = 0.5, rely = 0.7, anchor = 'c')

    frame3.button_input = ctk.CTkButton (frame3, width = 170, height = 30, corner_radius = 50, text = 'Ввести', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = check_char)
    frame3.button_input.place(relx = 0.8, rely = 0.7, anchor = 'c')

    frame3.button_back = ctk.CTkButton (frame3, width = 170, height = 30, corner_radius = 50, text = 'Назад', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = lambda: switch_to(page2))
    frame3.button_back.place(relx = 0.2, rely = 0.7, anchor = 'c')

    frame3.comment_label = ctk.CTkLabel (frame3, text = None,
    font = ('Constantia', 25), text_color = '#ffffff')
    frame3.comment_label.place(relx = 0.5, rely = 0.85, anchor = 'c')

    frame3.win_label = ctk.CTkLabel (frame3, text = '⬆⬆⬆\nСлово отгадано!\nХочешь сыграть снова?',
    font = ('Constantia', 25), text_color = '#ffffff')

    frame3.lose_label = ctk.CTkLabel (frame3, text = '⬆⬆⬆\nВсе попытки потрачены!\nХочешь сыграть снова?',
    font = ('Constantia', 25), text_color = '#ffffff')

    frame3.button_end = ctk.CTkButton (frame3, width = 170, height = 50, corner_radius = 50, text = 'Не хочу', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = to_end)

    frame3.button_repeat = ctk.CTkButton (frame3, width = 170, height = 50, corner_radius = 50, text = 'Давай!', fg_color = '#66ff33',
    hover_color = '#FFFFFF', text_color = '#000000', font= ('Constantia', 25), command = start_game)

    return frame3

def create_page4(main):
    frame4 = ctk.CTkFrame(main, fg_color = '#0d0d0d')
    frame4.pack(fill = 'both', expand = True)

    label = ctk.CTkLabel (frame4, text = choice(farewell),
    font = ('Constantia', 25), text_color = '#66ff33')
    label.place(relx = 0.5, rely = 0.5, anchor = 'c')

    return frame4

def create_page5(main):
    frame5 = ctk.CTkFrame(main, fg_color = '#0d0d0d')
    frame5.pack(fill = 'both', expand = True)

    frame5.label = ctk.CTkLabel (frame5, text = choice(repeating),
    font = ('Constantia', 25), text_color = '#66ff33')
    frame5.label.place(relx = 0.5, rely = 0.5, anchor = 'c')

    return frame5

page1 = create_page1(main)
page2 = create_page2(main)
page3 = create_page3(main)
page4 = create_page4(main)
page5 = create_page5(main)

switch_to (page1)

app.mainloop()
