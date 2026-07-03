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
        for text, cmd_key, relx, rely in button_data:
            button = ctk.CTkButton(
                self,
                text=text,
                command=partial(
                    controller.handle_command, cmd_key
                ),
                **cfg.BTN_PARAMS
            )
            button.place(relx=relx, rely=rely, anchor='c')


class GamePage(ctk.CTkFrame):
    def __init__(self, master, controller, page_name=None):
        super().__init__(master, fg_color=cfg.COLOR_DARK)

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

        cmd_map = {
            'clear': self.delete_char,
            'enter': lambda: self.send_data(self.entry.get()),
            'exit': lambda: controller.handle_command('exit_app'),
            'start': lambda: controller.handle_command('start_app')
        }

        self.buttons = {}
        button_data = cfg.GAME_PAGE_DATA['buttons']
        for name, text, cmd_key, relx, rely in button_data:
            button = ctk.CTkButton(
                self,
                text=text,
                command=cmd_map[cmd_key],
                **cfg.BTN_PARAMS
            )
            button.place(relx=relx, rely=rely, anchor='c')
            self.buttons[name] = button

        self.entry = ctk.CTkEntry(
            self,
            **cfg.ENTRY_PARAMS
        )
        self.entry.place(relx=0.5, rely=0.5, anchor='c')

    def delete_char(self):
        self.entry.delete(len(self.entry.get()) - 1)

    def send_data(self, user_input):
        print('SSS')

    #def update_ui(self):




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


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('hangman')
        self.geometry('600x500+800+450')
        self.resizable(False, False)
        self.attributes('-alpha', 0.9)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill='both', expand=True)
        #self.logic = MainLogic()

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

    def handle_command(self, target, *args, **kwargs):
        if hasattr(self, target):
            method = getattr(self, target)
            if callable(method):
                method(*args, **kwargs)
                return
        self.switch_to(target)

    def switch_to(self, page_name):
        if self.current_frame:
            self.current_frame.pack_forget()
        self.current_frame = self.pages[page_name]
        self.current_frame.pack(fill="both", expand=True)
        #if page_name == 'GamePage':
        #    self.current_frame.get_focus()

    def transfer_data(self, page, info):
        result = self.logic.check_input(page, info)
        if result in cfg.ERROR_MESSAGES:
            self.pages[page].show_error(result)
        elif result in self.pages:
            self.switch_to(result)
        else:
            self.transfer_result(info, result)

    def transfer_result(self, user_input, result):
        self.pages['GamePage'].show_result(user_input, result)

    def exit_app(self):
        self.pages['MessagePage'].change_message('farewell')
        self.switch_to('MessagePage')
        self.after(3000, self.destroy)

    def start_app(self):
        self.pages['MessagePage'].change_message('loading')
        self.switch_to('MessagePage')
        self.pages['GamePage'].update_ui()
        self.after(3000, lambda: self.switch_to('GamePage'))


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()