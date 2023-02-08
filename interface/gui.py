import os
from ipaddress import v6_int_to_packed
from time import sleep
from tkinter import *

import customtkinter
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
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("green")
# "blue","green","dark-blue"


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CHECK MATES - GAME")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        self.resizable(False, False)

        current_path = os.path.dirname(os.path.realpath(__file__))

        # ==============================================================================================
        # IMAGES
        # ==============================================================================================
        self.background = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/menu2_checkmates.png"),
            size=(WIDTH, HEIGHT),
        )

        self.icon_play = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_play4.png"),
            size=(35, 35),
        )

        self.icon_logo = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_logo.png"),
            size=(35, 35),
        )

        self.icon_white_black = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_white_black.png"),
            size=(35, 35),
        )

        self.icon_time = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_time.png"),
            size=(35, 35),
        )

        self.icon_back = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_back.png"),
            size=(35, 35),
        )

        self.icon_level = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_level.png"),
            size=(35, 35),
        )

        self.icon_config = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/icon_config2.png"),
            size=(35, 35),
        )

        self.white_pieces = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/white_pieces3.png"),
            size=(100, 100),
        )

        self.black_pieces = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/black_pieces.png"),
            size=(100, 100),
        )

        self.green_board = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/green_board.png"),
            size=(200, 200),
        )

        # ==============================================================================================
        # INIT FRAME
        # ==============================================================================================
        self.init_frame = customtkinter.CTkFrame(
            self,
            width=WIDTH,
            height=HEIGHT,
            corner_radius=0,
        )

        self.init_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.init_frame.grid(row=0, column=0, sticky="ns")

        self.background_label = customtkinter.CTkLabel(
            self.init_frame, image=self.background, text=""
        )
        self.background_label.grid(row=0, column=0)

        self.btn_start = customtkinter.CTkButton(
            master=self.init_frame,
            width=200,
            height=50,
            corner_radius=5,
            border_width=5,
            border_spacing=15,
            text=" JOGAR",
            hover_color=("gray70", "gray30"),
            font=customtkinter.CTkFont(size=25, weight="bold"),
            image=self.icon_play,
            anchor="w",
            command=self.button_callback_start,
        )
        self.btn_start.place(x=220, y=140, anchor="ne")

        self.btn_config = customtkinter.CTkButton(
            master=self.init_frame,
            width=200,
            height=50,
            corner_radius=5,
            border_width=5,
            border_spacing=15,
            text=" CONFIG",
            font=customtkinter.CTkFont(size=25, weight="bold"),
            image=self.icon_config,
            anchor="w",
            command=self.button_callback_config,
        )
        self.btn_config.place(x=220, y=220, anchor="ne")

        # ==============================================================================================
        # MAIN FRAME
        # ==============================================================================================

        self.main_frame = customtkinter.CTkFrame(
            self,
            corner_radius=0,
            width=WIDTH,
            height=HEIGHT,
            border_color="white"
            # background_corner_colors
        )
        # ------------------------------------------------------------------------------------------
        self.board_main_frame = customtkinter.CTkFrame(
            master=self.main_frame,
            width=240,
            corner_radius=1,
        )
        self.board_main_frame.grid(row=0, column=0, sticky="NSEW")

        self.board_img = customtkinter.CTkLabel(
            master=self.board_main_frame,
            image=self.green_board,
            text="",
        )
        self.board_img.grid(row=1, column=0, padx=(20, 20), pady=15)
        # ------------------------------------------------------------------------------------------
        self.board_text = customtkinter.CTkLabel(
            self.board_main_frame,
            text="BOARD",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, pady=5, sticky="NSEW")
        # ------------------------------------------------------------------------------------------

        self.msg_main_frame = customtkinter.CTkFrame(
            master=self.main_frame, width=240, corner_radius=1
        )
        self.msg_main_frame.grid(row=0, column=1, sticky="NSEW")
        # self.msg_main_frame.grid_rowconfigure(3, weight=1)

        # ------------------------------------------------------------------------------------------
        self.msg_text = customtkinter.CTkLabel(
            self.msg_main_frame,
            text="MENSAGEM",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.msg_text.grid(row=0, column=1, pady=5, sticky="NSEW")
        # ------------------------------------------------------------------------------------------
        # create textbox
        self.textbox = customtkinter.CTkTextbox(self.msg_main_frame, width=200, height=200)
        self.textbox.grid(row=1, column=1, padx=(20, 20), pady=(15, 0), sticky="NSEW")

        # # ------------------------------------------------------------------------------------------
        self.leave_button = customtkinter.CTkButton(
            master=self.main_frame,
            text="Desistir",
            fg_color="red",
            text_color="white",
            hover_color="blue",
            command=self.back_event,
        )
        self.leave_button.grid(row=2, column=0, pady=10)

        # ==============================================================================================
        # Config Frame
        # ==============================================================================================

        self.config_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.config_frame.grid_rowconfigure(5, weight=1)
        self.config_frame_label = customtkinter.CTkLabel(
            self.config_frame,
            text="CHECK    MATES",
            image=self.icon_logo,
            compound="center",
            font=customtkinter.CTkFont(size=17, weight="bold"),
        )
        self.config_frame_label.grid(row=0, column=0, padx=5, pady=5)

        # --------------------------------------------------------------------------------------------------
        self.home_button = customtkinter.CTkButton(
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
        self.frame_2_button = customtkinter.CTkButton(
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
            command=self.frame_2_button_event,
        )
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        # --------------------------------------------------------------------------------------------------
        self.frame_3_button = customtkinter.CTkButton(
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
            command=self.frame_3_button_event,
        )
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        # --------------------------------------------------------------------------------------------------

        self.back_button = customtkinter.CTkButton(
            self.config_frame,
            corner_radius=0,
            height=30,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("green", "gray30"),
            border_spacing=7,
            text="VOLTAR",
            image=self.icon_back,
            command=self.back_event,
            anchor="w",
        )
        self.back_button.grid(row=4, column=0, sticky="ew")
        # --------------------------------------------------------------------------------------------------
        self.appearance_mode_menu = customtkinter.CTkOptionMenu(
            self.config_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
        )
        self.appearance_mode_menu.grid(row=5, column=0, padx=10, pady=10, sticky="s")

        # =============================================================================================================
        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.radiobutton_var = customtkinter.StringVar(value="w")

        self.white_pieces = customtkinter.CTkLabel(
            self.home_frame,
            image=self.white_pieces,
            text="",
        )
        self.white_pieces.grid(row=0, column=0, pady=(20, 0))

        radiobutton_1 = customtkinter.CTkRadioButton(
            master=self.home_frame,
            variable=self.radiobutton_var,
            value="w",
            command=self.radiobutton_event,
            text="Jogar com peças brancas",
            hover_color="yellow",
        )
        radiobutton_1.grid(row=1, column=0, pady=10, padx=10)

        self.black_pieces = customtkinter.CTkLabel(
            self.home_frame,
            image=self.black_pieces,
            text="",
        )
        self.black_pieces.grid(row=2, column=0)

        radiobutton_2 = customtkinter.CTkRadioButton(
            master=self.home_frame,
            variable=self.radiobutton_var,
            value="b",
            command=self.radiobutton_event,
            text="Jogar com peças pretas",
            hover_color="yellow",
        )
        radiobutton_2.grid(row=4, column=0, pady=10, padx=10)

        # ***********************************************************************************************************
        # ***********************************************************************************************************
        # create second frame

        self.level_easy = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/level_easy.png"),
            size=(75, 75),
        )

        self.level_medium = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/level_medium.png"),
            size=(75, 75),
        )

        self.level_hard = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/level_hard3.png"),
            size=(75, 75),
        )

        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(3, weight=1)

        self.board_text = customtkinter.CTkLabel(
            self.second_frame,
            text="LEVEL IA",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, padx=10, pady=5)

        self.level_easy = customtkinter.CTkLabel(
            self.second_frame,
            image=self.level_easy,
            text="",
        )
        self.level_easy.grid(row=1, column=0, pady=(30, 5))

        self.level_medium = customtkinter.CTkLabel(
            self.second_frame,
            image=self.level_medium,
            text="",
        )
        self.level_medium.grid(row=1, column=1, pady=(30, 5))

        self.level_hard = customtkinter.CTkLabel(
            self.second_frame,
            image=self.level_hard,
            text="",
        )
        self.level_hard.grid(row=1, column=2, pady=(30, 5))

        self.level_radio_var = customtkinter.StringVar(value="facil")
        easy_radio_btn = customtkinter.CTkRadioButton(
            master=self.second_frame,
            variable=self.level_radio_var,
            value="facil",
            command=self.level_btn_event,
            text="FACIL",
            hover_color="yellow",
        )

        easy_radio_btn.grid(row=2, column=0, padx=(20, 5), pady=5)

        medium_radio_btn = customtkinter.CTkRadioButton(
            master=self.second_frame,
            variable=self.level_radio_var,
            value="medio",
            command=self.level_btn_event,
            text="MEDIO",
            hover_color="yellow",
        )
        medium_radio_btn.grid(row=2, column=1, pady=10)

        hard_radio_btn = customtkinter.CTkRadioButton(
            master=self.second_frame,
            variable=self.level_radio_var,
            value="dificil",
            command=self.level_btn_event,
            text="DIFICIL",
            hover_color="yellow",
        )
        hard_radio_btn.grid(row=2, column=2, pady=10)

        # ***********************************************************************************************************
        # ***********************************************************************************************************
        # create third frame

        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.dez_min = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/dez_min.png"),
            size=(75, 75),
        )

        self.quinze_min = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/quinze_min.png"),
            size=(75, 75),
        )

        self.vinte_min = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/vinte_min.png"),
            size=(75, 75),
        )

        self.vinte_cinco_min = customtkinter.CTkImage(
            Image.open(f"{current_path}/images/vinte_cinco_min.png"),
            size=(75, 75),
        )

        self.board_text = customtkinter.CTkLabel(
            self.third_frame,
            text="TEMPO DE PARTIDA",
            font=customtkinter.CTkFont(size=16, weight="bold"),
        )
        self.board_text.grid(row=0, column=0, padx=10, pady=10)

        self.dez_min_img = customtkinter.CTkLabel(
            self.third_frame,
            image=self.dez_min,
            text="",
        )
        self.dez_min_img.grid(row=1, column=0, padx=40, pady=(30, 5))

        self.quinze_min_img = customtkinter.CTkLabel(
            self.third_frame,
            image=self.quinze_min,
            text="",
        )
        self.quinze_min_img.grid(row=1, column=1, padx=40, pady=(30, 5))

        self.vinte_min_img = customtkinter.CTkLabel(
            self.third_frame,
            image=self.vinte_min,
            text="",
        )
        self.vinte_min_img.grid(row=2, column=0, padx=40, pady=(30, 5))

        self.vinte_cinco_min_img = customtkinter.CTkLabel(
            self.third_frame,
            image=self.vinte_cinco_min,
            text="",
        )
        self.vinte_cinco_min_img.grid(row=2, column=1, padx=40, pady=(30, 5))

    # =================================================================================================================
    def slider_callback(self, value):
        self.progressbar.set(value)

    def level_btn_event(self):
        print(f"Jogar com: {self.level_radio_var.get()}")

    def radiobutton_event(self):
        print(f"Jogar com: {self.radiobutton_var.get()}")

    def button_callback_start(self):
        print("Jogar Pressionado")

        self.init_frame.grid_forget()  # remove init frame
        self.main_frame.grid(row=0, column=0, sticky="nsew")  # show main frame

    def button_callback_config(self):
        print("config Pressionado")

        self.init_frame.grid_forget()  # remove init frame

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.config_frame.grid(row=0, column=0, sticky="nsew")  # show main frame

    def back_event(self):
        print("Cancelar Pressionado!! ")
        self.main_frame.grid_forget()
        self.config_frame.grid_forget()  # remove dash frame
        self.init_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    # ***********************************************************************************************************************
    def select_frame_by_name(self, name):
        self.home_button.configure(
            fg_color=("gray75", "gray25") if name == "home" else "transparent"
        )
        self.frame_2_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_2" else "transparent"
        )
        self.frame_3_button.configure(
            fg_color=("gray75", "gray25") if name == "frame_3" else "transparent"
        )

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


if __name__ == "__main__":
    app = App()
    app.mainloop()


# def messageScreen(msg):
#     messagebox_window = Tk()
#     messagebox_window.update()
#     messagebox_window.option_add("*font", "Inter  18")
#     messagebox_window.title(msg)
#     w_window = 400
#     h_window = 200
#     pos_right = round(window.winfo_screenwidth() / 2 - w_window / 2)
#     pos_down = round(window.winfo_screenheight() / 2 - h_window / 2)
#     messagebox_window.geometry(
#         "{}x{}+{}+{}".format(w_window, h_window, pos_right, pos_down)
#     )
#     messagebox_window["background"] = color["black1"]
#     messagebox_window.resizable(False, False)
#     frame2 = CTkFrame(
#         master=messagebox_window,
#         corner_radius=5,
#         fg_color=color["black2"],
#         width=360,
#         height=160,
#     )
#     frame2.place(x=20, y=20)
#     lbl = Label(frame2, text=msg, fg=color["white"], bg=color["black2"])
#     lbl.place(x=180 - lbl.winfo_reqwidth() / 2, y=40)
