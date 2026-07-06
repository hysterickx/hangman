import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import config as cfg
from random import choice
from functools import partial


class StaticPages(ctk.CTkFrame):
    def __init__(self, master, controller, page_name):
        super().__init__(master, fg_color=cfg.COLOR_DARK)

        page_config = cfg.STATIC_PAGES_DATA[page_name]

        label_data = page_config['labels']
        for text, color, font, relx, rely in label_data:
            label = ctk.CTkLabel(
                self,
                text=text,
                text_color=color,
                font=font
            )
            label.place(relx=relx, rely=rely, anchor='c')

        button_data = page_config['buttons']
        for text, info, relx, rely in button_data:
            button = ctk.CTkButton(
                self,
                text=text,
                command=partial(
                    controller.handle_command, page_name, info
                ),
                **cfg.BTN_PARAMS
            )
            button.place(relx=relx, rely=rely, anchor='c')


class GamePage(ctk.CTkFrame):
    def __init__(self, master, controller, page_name=None):
        super().__init__(master, fg_color=cfg.COLOR_DARK)

        self.controller = controller

        self.canvas = ctk.CTkCanvas(
            self,
            bg = cfg.COLOR_DARK,
            highlightthickness = 0
        )
        self.canvas.place(
            relx = 0.05, rely = 0.05,
            relwidth = 0.4, relheight = 0.5
        )

        canvas_data = cfg.GAME_PAGE_DATA['canvas_lines']
        for x1, y1, x2, y2, tags in canvas_data:
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='white',
                tags=tags
            )

        self.canvas.create_oval(
            230, 100, 270, 140,
            outline='white', tags='head'
        )

        self.labels = {}
        label_data = cfg.GAME_PAGE_DATA['labels']
        for name, text, color, font, relx, rely in label_data:
            label = ctk.CTkLabel(
                self,
                text=text,
                text_color=color,
                font=font
            )
            label.place(relx=relx, rely=rely, anchor='c')
            self.labels[name] = label

        self.entry = ctk.CTkEntry(
            self,
            **cfg.ENTRY_PARAMS
        )
        self.entry.place(relx=0.5, rely=0.7, anchor='c')
        self.entry.bind("<Return>", lambda event=None: self.send_data(self.entry.get().upper()))

        cmd_map = {
            'clear': self.delete_char,
            'enter': lambda: self.send_data(self.entry.get().upper()),
            'exit': lambda: self.send_data('exit'),
            'start': lambda: self.send_data('start')
        }

        self.buttons = {}
        button_data = cfg.GAME_PAGE_DATA['buttons']
        for name, text, cmd_key, cfg_key, relx, rely in button_data:
            button = ctk.CTkButton(
                self,
                text=text,
                command=cmd_map[cmd_key],
                **cfg_key
            )
            button.place(relx=relx, rely=rely, anchor='c')
            self.buttons[name] = button

    def delete_char(self):
        self.entry.delete(len(self.entry.get()) - 1)

    def clear_entry(self):
        self.entry.delete(0, 'end')
        self.entry.focus()

    def send_data(self, info):
        self.controller.handle_command(
            'GamePage', info
        )

    def show_error(self, status):
        error_message = CTkMessagebox(
            app,
            message=cfg.ERROR_MESSAGES[status],
            **cfg.MSG_PARAMS
        )
        self.wait_window(error_message)
        self.clear_entry()

    def show_game_info(self, status, word, count, part):
        self.labels['word_lbl'].configure(text=word)
        self.labels['count_lbl'].configure(
            text=f'Попыток осталось\n{count}'
        )
        self.labels['comment_lbl'].configure(
            text=choice(cfg.GAME_MESSAGES[status])
        )
        self.canvas.itemconfigure(part, state='normal')
        self.clear_entry()

    def show_result_info(self, status, word, count, part):
        self.entry.place_forget()
        self.buttons['clear_btn'].place_forget()
        self.buttons['enter_btn'].place_forget()
        self.canvas.itemconfigure(part, state='normal')
        self.labels['word_lbl'].configure(
            text=word, text_color=cfg.COLOR_LIME
        )
        self.labels['count_lbl'].configure(
            text=f'Попыток осталось\n{count}'
        )
        self.labels['comment_lbl'].configure(
            text=cfg.GAME_MESSAGES[status]
        )
        self.labels['comment_lbl'].place(
            relx=0.5, rely=0.7
        )
        self.buttons['exit_btn'].place(
            relx=0.35, rely=0.9, anchor='c'
        )
        self.buttons['start_btn'].place(
            relx=0.65, rely=0.9, anchor='c'
        )

    def update_ui(self, word, count):
        self.buttons['exit_btn'].place_forget()
        self.buttons['start_btn'].place_forget()
        self.canvas.itemconfigure("all", state="hidden")
        self.buttons['clear_btn'].place(
            relx=0.25, rely=0.7, anchor='c'
        )
        self.buttons['enter_btn'].place(
            relx=0.75, rely=0.7, anchor='c'
        )
        self.entry.place(relx=0.5, rely=0.7, anchor='c')
        self.clear_entry()
        self.labels['comment_lbl'].configure(text='')
        self.labels['comment_lbl'].place(
            relx=0.5, rely=0.85, anchor='c'
        )
        self.labels['word_lbl'].configure(
            text=word, text_color=cfg.COLOR_WHITE
        )
        self.labels['count_lbl'].configure(
            text=f'Попыток осталось:\n{count}'
        )


class MessagePage(ctk.CTkFrame):
    def __init__(self, master, controller, page_name=None):
        super().__init__(master, fg_color=cfg.COLOR_DARK)

        self.label = ctk.CTkLabel(
            self,
            text='',
            text_color=cfg.COLOR_LIME,
            font=cfg.FONT_LARGE
        )
        self.label.place(relx=0.5, rely=0.5, anchor='c')

    def change_message(self, stage):
        self.label.configure(
            text=choice(cfg.DELAY_MESSAGES[stage])
        )


class MainLogic:
    def __init__(self):
        self.current_word = ''
        self.hidden_word = []
        self.already_used = ''
        self.count = 8
        self.man_parts = cfg.MAN_PARTS.copy()

    def check_input(self, user_input):
        if not user_input:
            return 'empty'
        if len(user_input) > 1:
            return 'too_many'
        if user_input not in cfg.ALPHABET:
            return 'wrong_char'
        if user_input in self.already_used:
            return 'already_used'
        return None

    def change_word(self, user_input):
        error_status = self.check_input(user_input)
        if error_status:
            return error_status, None, None, None

        current = self.current_word
        hidden = self.hidden_word
        current_cut = self.current_word[1:-1]

        self.already_used += user_input
        for idx, char in enumerate(current):
            if char == user_input:
                hidden[idx] = char

        hidden_str = " ".join(self.hidden_word)

        if user_input in current_cut and '__' in hidden:
            return 'success', hidden_str, self.count, None

        if user_input in current_cut and '__' not in hidden:
            return 'win', hidden_str, self.count, None

        if user_input not in current_cut and self.count > 1:
            self.count -= 1
            man_part = self.man_parts.pop(0)
            return 'wrong', hidden_str, self.count, man_part

        if user_input not in current_cut and self.count == 1:
            self.count -= 1
            man_part = self.man_parts.pop(0)
            return 'lose', " ".join(current), self.count, man_part

    def update_variables(self):
        self.current_word = choice(cfg.WORDS_DATA).upper()
        self.hidden_word = ['__'] * len(self.current_word)
        self.hidden_word[0] = self.current_word[0]
        self.hidden_word[-1] = self.current_word[-1]
        self.already_used = ''
        self.count = 8
        self.man_parts = cfg.MAN_PARTS.copy()
        print(self.current_word)
        return self.hidden_word, self.count


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('hangman')
        self.geometry('600x500+800+450')
        self.resizable(False, False)
        self.attributes('-alpha', 0.9)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)
        self.logic = MainLogic()

        self.pages = {}
        self.current_frame = None
        page_types = [
            ('GreetingsPage', StaticPages),
            ('RulesPage', StaticPages),
            ('GamePage', GamePage),
            ('MessagePage', MessagePage)
        ]

        for page_name, page_class in page_types:
            self.pages[page_name] = page_class(
                self.main_frame,
                self,
                page_name
            )
        self.switch_to("GreetingsPage")

    def handle_command(self, page, info, *args, **kwargs):
        router = {
            ('GreetingsPage', 'exit'):  self.exit_app,
            ('GreetingsPage', 'next'):  lambda: self.switch_to('RulesPage'),

            ('RulesPage', 'exit'):      self.exit_app,
            ('RulesPage', 'start'):     self.start_app,

            ('GamePage', 'exit'):       self.exit_app,
            ('GamePage', 'start'):      self.start_app
        }

        action = router.get((page, info))

        if action:
            action(*args, **kwargs)
            return

        if page == 'GamePage':
            self.transfer_data(info)

    def switch_to(self, page_name):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.pages[page_name]
        self.current_frame.pack(fill="both", expand=True)
        if page_name == 'GamePage':
            self.current_frame.clear_entry()

    def transfer_data(self, user_input):
        status, word, count, part = \
            self.logic.change_word(user_input)
        if status in cfg.ERROR_MESSAGES:
            self.pages['GamePage'].show_error(status)
        elif status in ('win', 'lose'):
            self.pages['GamePage'].show_result_info(
                status, word, count, part
            )
        else:
            self.pages['GamePage'].show_game_info(
                status, word, count, part
            )

    def exit_app(self):
        self.pages['MessagePage'].change_message('farewell')
        self.switch_to('MessagePage')
        self.after(3000, self.destroy)

    def start_app(self):
        self.pages['MessagePage'].change_message('loading')
        self.switch_to('MessagePage')
        word, count = self.logic.update_variables()
        self.pages['GamePage'].update_ui(word, count)
        self.after(3000, lambda: self.switch_to('GamePage'))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()