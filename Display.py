import ast
import os
import threading
import time
import tkinter as tk
from tkinter import messagebox
from Game import Game
import customtkinter as ctk
from PIL import Image


WIDTH = 480
HEIGHT = 320

ctk.set_appearance_mode("Dark")


class Display(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.stockfish = None
        self.bitBoard = [[]]
        self.message = [" ", " ", " "]
        self.stop_threads = False
        self.game = None

        self.title("Checkmates")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.level_var = ctk.IntVar(value=1)
        self.color_var = ctk.StringVar(value="w")
        self.theme = ctk.StringVar(value="Dark")
        # self.attributes("-fullscreen", True)

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.load_images()
        self.home()

    def home(self):
        self.home_frame = ctk.CTkFrame(self)
        self.home_frame.grid(row=0, column=0, sticky="ns")

        self.home_background = ctk.CTkLabel(
            self.home_frame, image=self.background, text=""
        )
        self.home_background.grid(row=0, column=0)

        self.btn_start = ctk.CTkButton(
            master=self.home_frame,
            width=200,
            height=50,
            fg_color="#8f5e36",
            hover_color=("gray70", "gray30"),
            corner_radius=0,
            border_width=3,
            text="Iniciar jogo!",
            font=ctk.CTkFont(size=20, weight="bold"),
            image=self.icon_play,
            command=self.start_threads,
        )
        self.btn_start.place(x=220, y=140, anchor="ne")

        self.btn_config = ctk.CTkButton(
            master=self.home_frame,
            width=200,
            height=50,
            fg_color="#8f5e36",
            hover_color=("gray70", "gray30"),
            corner_radius=0,
            border_width=3,
            text="configurar",
            font=ctk.CTkFont(size=20, weight="bold"),
            image=self.icon_config,
            command=self.config,
        )
        self.btn_config.place(x=220, y=220, anchor="ne")

    def config(self):
        self.home_frame.grid_forget()

        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.grid(row=0, column=0, sticky="ns")

        self.config_options_frame = ctk.CTkFrame(master=self.config_frame)
        self.config_options_frame.grid(row=0, column=0, sticky="nsew")
        self.config_options_frame.grid_rowconfigure(6, weight=1)
        self.config_options()

        self.config_select_color()

    def config_options(self):
        self.config_frame_label = ctk.CTkLabel(
            self.config_options_frame,
            text="CHECK    MATES",
            image=self.icon_logo,
            font=ctk.CTkFont(size=17, weight="bold"),
        )
        self.config_frame_label.grid(row=0, column=0, padx=5, pady=5)

        self.home_button = ctk.CTkButton(
            self.config_options_frame,
            corner_radius=0,
            height=30,
            border_spacing=7,
            text="Selecione sua cor",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icon_white_black,
            command=self.config_select_color,
        )
        self.home_button.grid(row=1, column=0, sticky="s")

        self.level_button = ctk.CTkButton(
            self.config_options_frame,
            corner_radius=0,
            height=30,
            border_spacing=7,
            text="Dificuldade da IA",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icon_level,
            command=self.config_select_level,
        )
        self.level_button.grid(row=2, column=0, sticky="s")

        self.theme_switch = ctk.CTkSwitch(
            master=self.config_options_frame,
            text="    Darkmode       ",
            command=self.change_theme,
            variable=self.theme,
            onvalue="Dark",
            offvalue="Light",
        )
        self.theme_switch.grid(row=3, column=0, sticky="s", pady=8)

        self.config_empty_row = ctk.CTkLabel(
            self.config_options_frame,
            text="",
        )
        self.config_empty_row.grid(row=4, column=0, padx=5, pady=18)

        self.back_button = ctk.CTkButton(
            self.config_options_frame,
            corner_radius=0,
            height=30,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("green", "gray30"),
            border_spacing=7,
            text="voltar ao início     ",
            image=self.icon_back,
            command=self.go_to_home,
        )
        self.back_button.grid(row=5, column=0, sticky="s")

    def change_theme(self):
        ctk.set_appearance_mode(self.theme.get())

    def reset_selected_config_option(self):
        try:
            self.config_current_option_frame.grid_forget()
        except:
            e = ""
        finally:
            self.load_images()
            self.config_current_option_frame = ctk.CTkFrame(master=self.config_frame)
            self.config_current_option_frame.grid(row=0, column=1, sticky="nsew")

    def config_select_color(self):
        self.reset_selected_config_option()

        self.config_select_color_frame = ctk.CTkFrame(
            master=self.config_current_option_frame
        )
        self.config_select_color_frame.grid(row=0, column=0, sticky="nsew")
        self.config_select_color_frame.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.white_pieces = ctk.CTkLabel(
            self.config_select_color_frame,
            image=self.white_pieces,
            text="",
        )
        self.white_pieces.grid(row=0, column=0, pady=(65, 15), padx=(10, 5))

        black_pieces_rb = ctk.CTkRadioButton(
            master=self.config_select_color_frame,
            variable=self.color_var,
            value="w",
            text="Peças brancas",
            hover_color="yellow",
        )
        black_pieces_rb.grid(row=0, column=1, pady=(65, 15), padx=(0, 50))

        self.black_pieces = ctk.CTkLabel(
            self.config_select_color_frame,
            image=self.black_pieces,
            text="",
        )
        self.black_pieces.grid(row=1, column=0, pady=(15, 65), padx=(10, 5))

        select_color_rb = ctk.CTkRadioButton(
            master=self.config_select_color_frame,
            variable=self.color_var,
            value="b",
            text="Peças pretas   ",
            hover_color="yellow",
        )
        select_color_rb.grid(row=1, column=1, pady=(15, 65), padx=(0, 50))

    def config_select_level(self):
        self.reset_selected_config_option()

        self.level_frame = ctk.CTkFrame(self.config_current_option_frame)
        self.level_frame.grid(row=0, column=0)
        self.level_frame.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.level_easy = ctk.CTkLabel(
            self.level_frame,
            image=self.level_easy,
            text="",
        )
        self.level_easy.grid(row=0, column=0, pady=(35, 20), padx=10)

        self.level_medium = ctk.CTkLabel(
            self.level_frame,
            image=self.level_medium,
            text="",
        )
        self.level_medium.grid(row=1, column=0, pady=0, padx=10)

        self.level_hard = ctk.CTkLabel(
            self.level_frame,
            image=self.level_hard,
            text="",
        )
        self.level_hard.grid(row=2, column=0, pady=(20, 35), padx=10)

        easy_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value=1,
            text="Iniciante       ",
            hover_color="yellow",
        )

        easy_radio_btn.grid(row=0, column=1, padx=(10, 50))

        medium_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value=3,
            text="Intermediário",
            hover_color="yellow",
        )
        medium_radio_btn.grid(row=1, column=1, padx=(10, 50))

        hard_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value=7,
            text="Avançado      ",
            hover_color="yellow",
        )
        hard_radio_btn.grid(row=2, column=1, padx=(10, 50))

        return

    def game_screen(self):
        self.home_frame.grid_forget()

        self.game_frame = ctk.CTkFrame(self)
        self.game_frame.grid(row=0, column=0)
        self.game_board_frame = ctk.CTkFrame(master=self.game_frame, corner_radius=0)
        self.game_board_frame.pack(side="left", fill="both", expand=True)

        self.bitboard_title = ctk.CTkLabel(
            master=self.game_board_frame,
            text="Leitura da bitboard",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.bitboard_title.grid(row=0, column=0, pady=(10, 5))

        self.game_screen_board()

        self.game_msg_frame = ctk.CTkFrame(master=self.game_frame, corner_radius=0)
        self.game_msg_frame.pack(side="left", fill="both", expand=True)

        self.msg_title = ctk.CTkLabel(
            master=self.game_msg_frame,
            text="Mensagem de feedback",
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        self.msg_title.pack(side="top", pady=(10), padx=(30))

        self.game_screen_msg()

        self.btn_give_up = ctk.CTkButton(
            master=self.game_msg_frame,
            fg_color="red",
            hover_color=("#ff4545", "#ff4545"),
            text="Desistir!",
            command=self.give_up,
            font=ctk.CTkFont(size=12, weight="normal"),
        )
        self.btn_give_up.pack(side="bottom", padx=10, pady=(10, 45))

    def game_screen_board(self):
        self.bitboard_frame = ctk.CTkFrame(master=self.game_board_frame)
        self.bitboard_frame.grid_rowconfigure(8, weight=1)
        self.bitboard_frame.grid_columnconfigure(8, weight=1)

        for x, row in enumerate(self.bitBoard):
            for y, item in enumerate(row):
                newEl = ctk.CTkLabel(master=self.bitboard_frame, text=item, padx=3)
                newEl.grid(row=x, column=y)

        self.bitboard_frame.grid(row=1, column=0, pady=(15, 40), padx=(10, 10))

    def game_screen_msg(self):
        try:
            self.msg_status_title.pack_forget()
            self.msg_status.pack_forget()
            self.msg_IA.pack_forget()
            self.msg_user.pack_forget()
        except:
            e = ""

        self.msg_status_title = ctk.CTkLabel(
            master=self.game_msg_frame,
            text="Status do jogo:",
            font=ctk.CTkFont(size=14, weight="bold"),
            justify=tk.LEFT,
        )
        self.msg_status_title.pack(side="top", pady=(10, 0))

        self.msg_status = ctk.CTkLabel(
            master=self.game_msg_frame,
            text=self.message[0],
            wraplength=220,
            font=ctk.CTkFont(size=14, weight="normal"),
            justify=tk.LEFT,
        )
        self.msg_status.pack(side="top", pady=(2, 5))

        self.msg_IA = ctk.CTkLabel(
            master=self.game_msg_frame,
            text=f"Movimento da IA: {self.message[1]}",
            font=ctk.CTkFont(size=14, weight="bold"),
            justify=tk.LEFT,
        )
        self.msg_IA.pack(side="top", pady=5)

        self.msg_user = ctk.CTkLabel(
            master=self.game_msg_frame,
            text=f"Movimento do usuário: {self.message[2]}",
            font=ctk.CTkFont(size=14, weight="bold"),
            justify=tk.LEFT,
        )
        self.msg_user.pack(side="top", pady=5)

    def give_up(self):
        answer = messagebox.askyesno(
            "1", "Tem certeza que quer desistir do jogo?"
        )
        if answer:
            self.go_to_home()

    def go_to_home(self):
        self.stop_threads = True
        if self.game:
            self.game.stopGame = True
        self.message = ""
        self.bitBoard = [[]]

        try:
            self.config_frame.grid_forget()
        except:
            er = ""
        try:
            self.game_frame.grid_forget()
        except:
            er = ""

        self.home()

    def load_images(self):
        self.background = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/background.png"),
            size=(WIDTH, HEIGHT),
        )

        self.icon_play = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/home/start_game_icon.png"),
            size=(30, 30),
        )

        self.icon_config = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/home/config_icon.png"),
            size=(30, 30),
        )

        self.icon_logo = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/icon_logo.png"),
            size=(35, 35),
        )

        self.icon_white_black = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/color/icon_white_black.png"),
            size=(35, 35),
        )

        self.icon_back = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/icon_back.png"),
            size=(35, 35),
        )

        self.icon_level = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/level/icon_level.png"),
            size=(35, 35),
        )

        self.white_pieces = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/color/white_pieces.png"),
            size=(80, 80),
        )

        self.black_pieces = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/color/black_pieces.png"),
            size=(80, 80),
        )

        self.level_easy = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/level/level_easy.png"),
            size=(70, 70),
        )

        self.level_medium = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/level/level_medium.png"),
            size=(70, 70),
        )

        self.level_hard = ctk.CTkImage(
            Image.open(f"{self.current_path}/assets/config/level/level_hard.png"),
            size=(70, 70),
        )

    def start_threads(self):
        with open("message.txt", "w") as file:
            file.write(str([" ", " ", " "]))
        with open("bitboard.txt", "w") as file:
            file.write(str([[]]))
        self.message = [" ", " ", " "]

        self.game = Game(self.color_var.get(), self.level_var.get())
        self.stop_threads = False
        self.game.stopGame = False

        self.game_frame_th = threading.Thread(target=self.start_game_frame)
        self.game_frame_th.start()

        self.game_th = threading.Thread(target=self.game.start_game)
        self.game_th.start()

    def start_game_frame(self):
        self.game_screen()

        while not self.stop_threads:
            with open("message.txt", "r") as file:
                content = file.read()
            self.message = ast.literal_eval(content)

            with open("bitboard.txt", "r") as file:
                content = file.read()
            self.bitBoard = ast.literal_eval(content)

            self.game_screen_board()
            self.game_screen_msg()
            time.sleep(1)


if __name__ == "__main__":
    display = Display()
    display.mainloop()
