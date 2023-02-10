import os
import threading
import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

WIDTH = 480
HEIGHT = 320

COLOR = {
    "BLACK": "#1E1E1E",
    "BLACK1": "#3C3C3C",
    "RED1": "#FF1E1E",
    "RED2": "#FF7878",
    "YELLOW": "#FFFF1E",
    "GREEN": "#64FF64",
    "BLUE1": "#00FFFF",
    "BLUE2": "#5082FF",
    "PURPLE2": "#783CFF",
    "PURPLE1": "#9678FF",
    "ORANGE1": "#FF6400",
    "ORANGE2": "#FFB450",
    "WHITE": "#F0F0F0",
}


# "System", "Dark", "Light"
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")
# "blue","green","dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CHECK MATES - GAME")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)
        self.attributes("-fullscreen", True)

        self.current_path = os.path.dirname(os.path.realpath(__file__))

        self.load_image()
        self.start()
        self.config()
        self.home()
        self.duration()
        self.game()

    # ======================================< INIT FRAME >=============================================
    def start(self):
        print("start")
        self.init_frame = ctk.CTkFrame(
            self,
            width=WIDTH,
            height=HEIGHT,
            corner_radius=0,
        )

        self.init_frame = ctk.CTkFrame(self, corner_radius=0)
        self.init_frame.grid(row=0, column=0, sticky="ns")

        self.background_label = ctk.CTkLabel(self.init_frame, image=self.background, text="")
        self.background_label.grid(row=0, column=0)

        self.btn_start = ctk.CTkButton(
            master=self.init_frame,
            width=200,
            height=50,
            corner_radius=5,
            border_width=5,
            border_spacing=15,
            text=" JOGAR",
            hover_color=("gray70", "gray30"),
            font=ctk.CTkFont(size=25, weight="bold"),
            image=self.icon_play,
            anchor="w",
            command=self.button_callback_start,
        )
        self.btn_start.place(x=220, y=140, anchor="ne")

        self.btn_config = ctk.CTkButton(
            master=self.init_frame,
            width=200,
            height=50,
            corner_radius=5,
            border_width=5,
            border_spacing=15,
            text=" CONFIG",
            font=ctk.CTkFont(size=25, weight="bold"),
            image=self.icon_config,
            anchor="w",
            command=self.config_btn,
        )
        self.btn_config.place(x=220, y=220, anchor="ne")

    # ======================================< RUN GAME >=============================================
    def run_game(self):
        while True:

            # message = função que retorna a mensagem
            jogada = input("Digite a Jogada: ")
            # msg = input("Digite a mensagem: ")

            # message = {"code": code, "text": msg}

            # if message["code"] == 0:  # mostrar um pop up jogada errada
            # print(message["text"])

            self.msg_text = ctk.CTkLabel(
                self.msg_game_frame,
                text="Turno do Jogador",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold",
                ),
            )
            self.msg_text.grid(row=3, column=1, pady=5, sticky="NSEW")

            self.game_frame.update()

            self.msg_text = ctk.CTkLabel(
                self.msg_game_frame,
                text=jogada,
                font=ctk.CTkFont(
                    size=25,
                    weight="bold",
                ),
            )
            self.msg_text.grid(row=4, column=1, pady=5)

            self.game_frame.update()

            self.msg_text = ctk.CTkLabel(
                self.msg_game_frame,
                text="Mensagem final",
                font=ctk.CTkFont(
                    size=15,
                    weight="bold",
                ),
            )
            self.msg_text.grid(row=5, column=1, pady=5, sticky="ew")

            self.game_frame.update()

    # ======================================< GAME FRAME >=============================================
    def game(self):
        self.game_frame = ctk.CTkFrame(
            self, corner_radius=0, width=WIDTH, height=HEIGHT, border_color="white"
        )
        # ------------------------------------------------------------------------------------------

        self.board_game_frame = ctk.CTkFrame(
            master=self.game_frame,
            width=240,
            corner_radius=1,
        )
        self.board_game_frame.grid(row=0, column=0, sticky="NSEW")

        self.board_img = ctk.CTkLabel(
            master=self.board_game_frame,
            image=self.green_board,
            text="",
        )
        self.board_img.grid(row=1, column=0, padx=(20, 20), pady=15)
        # ------------------------------------------------------------------------------------------
        self.board_text = ctk.CTkLabel(
            self.board_game_frame,
            text="BOARD",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, pady=5, sticky="NSEW")

        self.msg_game_frame = ctk.CTkFrame(master=self.game_frame, width=240, corner_radius=1)
        self.msg_game_frame.grid(row=0, column=1, sticky="NSEW")
        # self.msg_game_frame.grid_rowconfigure(3, weight=1)

        self.msg_text = ctk.CTkLabel(
            self.msg_game_frame,
            text="MENSAGEM",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.msg_text.grid(row=0, column=1, pady=5, sticky="NSEW")

        self.leave_button = ctk.CTkButton(
            master=self.board_game_frame,
            text="Desistir",
            fg_color="red",
            text_color="white",
            hover_color="blue",
            command=self.leave_game_btn,
        )
        self.leave_button.grid(row=2, column=0, pady=10)

    # =====================================< CONFIG FRAME >============================================
    def config(self):
        self.config_frame = ctk.CTkFrame(self, corner_radius=0)
        self.config_frame.grid_rowconfigure(5, weight=1)
        self.config_frame_label = ctk.CTkLabel(
            self.config_frame,
            text="CHECK    MATES",
            image=self.icon_logo,
            compound="center",
            font=ctk.CTkFont(size=17, weight="bold"),
        )
        self.config_frame_label.grid(row=0, column=0, padx=5, pady=5)

        # --------------------------------------------------------------------------------------------------
        self.home_button = ctk.CTkButton(
            self.config_frame,
            corner_radius=0,
            height=30,
            border_spacing=7,
            text="PLAY AS",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icon_white_black,
            anchor="w",
            command=self.home_button_event,
        )
        self.home_button.grid(row=1, column=0, sticky="ew")

        # --------------------------------------------------------------------------------------------------
        self.level_button = ctk.CTkButton(
            self.config_frame,
            corner_radius=0,
            height=30,
            border_spacing=7,
            text="LEVEL",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icon_level,
            anchor="w",
            command=self.level_button_event,
        )
        self.level_button.grid(row=2, column=0, sticky="ew")

        # --------------------------------------------------------------------------------------------------
        self.duration_button = ctk.CTkButton(
            self.config_frame,
            corner_radius=0,
            height=30,
            border_spacing=7,
            text="TIME",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            image=self.icon_time,
            anchor="w",
            command=self.duration_button_event,
        )
        self.duration_button.grid(row=3, column=0, sticky="ew")
        # --------------------------------------------------------------------------------------------------

        self.back_button = ctk.CTkButton(
            self.config_frame,
            corner_radius=0,
            height=30,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("green", "gray30"),
            border_spacing=7,
            text="VOLTAR",
            image=self.icon_back,
            command=self.back_init_btn,
            anchor="w",
        )
        self.back_button.grid(row=4, column=0, sticky="ew")
        # --------------------------------------------------------------------------------------------------
        self.appearance_mode_menu = ctk.CTkOptionMenu(
            self.config_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=10, pady=10, sticky="s")

    # =====================================< HOME FRAME >============================================
    def home(self):
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.color_var = ctk.StringVar(value="w")

        self.white_pieces = ctk.CTkLabel(
            self.home_frame,
            image=self.white_pieces,
            text="",
        )
        self.white_pieces.grid(row=0, column=0, pady=(20, 0))

        black_pieces_rb = ctk.CTkRadioButton(
            master=self.home_frame,
            variable=self.color_var,
            value="w",
            command=self.select_color_event,
            text="Jogar com peças brancas",
            hover_color="yellow",
        )
        black_pieces_rb.grid(row=1, column=0, pady=10, padx=10)

        self.black_pieces = ctk.CTkLabel(
            self.home_frame,
            image=self.black_pieces,
            text="",
        )
        self.black_pieces.grid(row=2, column=0)

        select_color_rb = ctk.CTkRadioButton(
            master=self.home_frame,
            variable=self.color_var,
            value="b",
            command=self.select_color_event,
            text="Jogar com peças pretas",
            hover_color="yellow",
        )
        select_color_rb.grid(row=4, column=0, pady=10, padx=10)

        # ***********************************************************************************************************
        # create Level Frame
        # ***********************************************************************************************************

        self.level_easy = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/level_easy.png"),
            size=(75, 75),
        )

        self.level_medium = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/level_medium.png"),
            size=(75, 75),
        )

        self.level_hard = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/level_hard3.png"),
            size=(75, 75),
        )

        self.level_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.level_frame.grid_columnconfigure(3, weight=1)

        self.board_text = ctk.CTkLabel(
            self.level_frame,
            text="LEVEL IA",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, padx=10, pady=5)

        self.level_easy = ctk.CTkLabel(
            self.level_frame,
            image=self.level_easy,
            text="",
        )
        self.level_easy.grid(row=1, column=0, pady=(30, 5))

        self.level_medium = ctk.CTkLabel(
            self.level_frame,
            image=self.level_medium,
            text="",
        )
        self.level_medium.grid(row=1, column=1, pady=(30, 5))

        self.level_hard = ctk.CTkLabel(
            self.level_frame,
            image=self.level_hard,
            text="",
        )
        self.level_hard.grid(row=1, column=2, pady=(30, 5))

        self.level_var = ctk.StringVar(value="facil")
        easy_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value="facil",
            command=self.level_btn_event,
            text="FACIL",
            hover_color="yellow",
        )

        easy_radio_btn.grid(row=2, column=0, padx=(20, 5), pady=5)

        medium_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value="medio",
            command=self.level_btn_event,
            text="MEDIO",
            hover_color="yellow",
        )
        medium_radio_btn.grid(row=2, column=1, pady=10)

        hard_radio_btn = ctk.CTkRadioButton(
            master=self.level_frame,
            variable=self.level_var,
            value="dificil",
            command=self.level_btn_event,
            text="DIFICIL",
            hover_color="yellow",
        )
        hard_radio_btn.grid(row=2, column=2, pady=10)

    #  ===================================< DURATION FRAME >===========================================
    def duration(self):
        self.duration_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.dez_min = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/dez_min.png"),
            size=(75, 75),
        )

        self.quinze_min = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/quinze_min.png"),
            size=(75, 75),
        )

        self.vinte_min = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/vinte_min.png"),
            size=(75, 75),
        )

        self.vinte_cinco_min = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/vinte_cinco_min.png"),
            size=(75, 75),
        )

        self.board_text = ctk.CTkLabel(
            self.duration_frame,
            text="TEMPO DE PARTIDA",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, padx=10, pady=10)

        self.dez_min_img = ctk.CTkLabel(
            self.duration_frame,
            image=self.dez_min,
            text="",
        )
        self.dez_min_img.grid(row=1, column=0, padx=40, pady=(30, 5))

        self.quinze_min_img = ctk.CTkLabel(
            self.duration_frame,
            image=self.quinze_min,
            text="",
        )
        self.quinze_min_img.grid(row=1, column=1, padx=40, pady=(30, 5))

        self.vinte_min_img = ctk.CTkLabel(
            self.duration_frame,
            image=self.vinte_min,
            text="",
        )
        self.vinte_min_img.grid(row=2, column=0, padx=40, pady=(30, 5))

        self.vinte_cinco_min_img = ctk.CTkLabel(
            self.duration_frame,
            image=self.vinte_cinco_min,
            text="",
        )
        self.vinte_cinco_min_img.grid(row=2, column=1, padx=40, pady=(30, 5))

    # =======================================< EVENTS >================================================

    def level_btn_event(self):
        print(f"Jogar com: {self.level_var.get()}")

    def select_color_event(self):
        print(f"Jogar com: {self.color_var.get()}")

    def button_callback_start(self):
        print("Jogar Pressionado")
        print(f"Enviar: {self.level_var.get()}")
        print(f"Enviar: {self.color_var.get()}")

        self.init_frame.grid_forget()
        self.game_frame.grid(row=0, column=0, sticky="nsew")

        # chamar função para enviar os parametros (self.level_var.get(), self.color_var.get())

        game_th = threading.Thread(target=self.run_game)
        game_th.start()

    # ==================================================================================
    def config_btn(self):
        print("config Pressionado")

        self.init_frame.grid_forget()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.config_frame.grid(row=0, column=0, sticky="nsew")

    def back_init_btn(self):
        print("Cancelar Pressionado!! ")
        self.game_frame.grid_forget()
        self.config_frame.grid_forget()
        self.init_frame.grid(row=0, column=0, sticky="ns")

    def leave_game_btn(self):
        print("Sair do Jogo pressionado!!")

        self.confirm_exit()

    def confirm_exit(self):
        answer = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if answer == True:
            self.game_frame.grid_forget()
            self.config_frame.grid_forget()
            self.init_frame.grid(row=0, column=0, sticky="ns")
            # self.game_frame.destroy()
        else:
            self.run_game()

    # =======================================< EVENTS >================================================

    def select_frame_by_name(self, name):
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.level_button.configure(
            fg_color=("gray75", "gray25") if name == "level" else "transparent"
        )
        self.duration_button.configure(
            fg_color=("gray75", "gray25") if name == "duration" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "level":
            self.level_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.level_frame.grid_forget()
        if name == "duration":
            self.duration_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.duration_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def level_button_event(self):
        self.select_frame_by_name("level")

    def duration_button_event(self):
        self.select_frame_by_name("duration")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    # ===================================================================================================
    def load_image(self):
        self.background = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/menu2_checkmates.png"),
            size=(WIDTH, HEIGHT),
        )

        self.icon_play = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_play4.png"),
            size=(35, 35),
        )

        self.icon_logo = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_logo.png"),
            size=(35, 35),
        )

        self.icon_white_black = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_white_black.png"),
            size=(35, 35),
        )

        self.icon_time = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_time.png"),
            size=(35, 35),
        )

        self.icon_back = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_back.png"),
            size=(35, 35),
        )

        self.icon_level = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_level.png"),
            size=(35, 35),
        )

        self.icon_config = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/icon_config2.png"),
            size=(35, 35),
        )

        self.white_pieces = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/white_pieces3.png"),
            size=(100, 100),
        )

        self.black_pieces = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/black_pieces.png"),
            size=(100, 100),
        )

        self.green_board = ctk.CTkImage(
            Image.open(f"{self.current_path}/images/green_board.png"),
            size=(200, 200),
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
