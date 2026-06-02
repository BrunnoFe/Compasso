from PIL import Image

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from . import gui_logger
from . import set_window_grid, set_window_configs, set_grids
from src.core import connectar_bitalino, run_scan_devices

ctk.set_appearance_mode("system")

BORDER_WIDTH: int = 5
BORDER_WIDTH_INSIDE: int = 8
CORNER: int = 30
AZUL: str = "#99acff"
AZUL_CLARO: str = "#c2cdff"
CINZA: str = "#806e86"
ROSA: str = "#edcbf6"
AMARELO: str = "#ffc700"
AMARELO_ESC: str = "#b68e00"
TRANSPARENTE: str = "transparent"
BASE_FONT: tuple = ("Helvetica", 16, "bold")
BASE_FONT_MED: tuple = ("Helvetica", 14, "bold")
BASE_FONT_MIN: tuple = ("Helvetica", 12, "bold")
NSE: str = "nse"

class Compasso(ctk.CTk):
    def __init__(self, nome="Compasso"):
        super().__init__(fg_color=AZUL)
        self.title(nome)
        self.resizable(False, False)
        set_window_configs(self, width_multip=0.5, height_multip=0.5)
        set_window_grid(self)

        self.main_frame = MainFrame(self)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        set_grids(self, rows_conf={1:[0,2], 4:[1]}, column_conf={1:[0]})
        gui_logger.logger.info("MainFrame iniciado.")

        self.up_frame = UpFrame(self)
        self.mid_frame = MidFrame(self)
        self.down_frame = DownFrame(self)

class UpFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=AZUL, fg_color=ROSA, background_corner_colors=(AZUL, AZUL, AZUL, AZUL))
        set_grids(self, rows_conf={1:[0]}, column_conf={2:[0], 1:[1,2]})

        self.main_frame = master

        logo_img = Image.open(r'assets\logo.png')

        self.logo_img = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(logo_img.width, logo_img.height))
        self.logo = ctk.CTkLabel(self, image=self.logo_img, corner_radius=CORNER, anchor=ctk.W, bg_color=ROSA, fg_color=TRANSPARENTE, text="")
        self.logo.grid(row=0, column=0, pady=15, padx=15, sticky=ctk.NSEW)

        self.mac_addr_var = ctk.StringVar(value="Escolha o dispositivo...")

        self.mac_adress_label = ctk.CTkLabel(self, text="Selecione o endereço MAC do Bitalino:", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.mac_adress_label.grid(row=0, column=1, pady=15, padx=10, sticky=ctk.N)

        self.up_select_macaddr = ctk.CTkComboBox(self, state="normal", corner_radius=CORNER, border_width=BORDER_WIDTH, variable=self.mac_addr_var,
                                                 bg_color=ROSA, fg_color=ROSA,  border_color=AZUL, button_color=AZUL, values=[""],
                                                 button_hover_color=AMARELO, dropdown_fg_color=ROSA, dropdown_hover_color=AZUL_CLARO, 
                                                 text_color=CINZA, dropdown_text_color=CINZA, justify=ctk.CENTER,
                                                 font=BASE_FONT_MED, dropdown_font=BASE_FONT_MIN)
        self.up_select_macaddr.grid(row=0, column=1, pady=10, padx=10, sticky=ctk.EW)

        self.refresh_mac_button = ctk.CTkButton(self, text="Escanear", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=ROSA, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self.update_mac_addresses)
        self.refresh_mac_button.grid(row=0, column=1, pady=15, padx=10, sticky=ctk.S)
        
        conect_bitalino_img = Image.open(r'assets\conect_bitalino.png')
        conect_bitalino_img_dim = Image.open(r'assets\conect_bitalino_dim.png')
        conectado_bitalino = Image.open(r'assets\conectado.png')

        self.button_conectbt_img = ctk.CTkImage(light_image=conect_bitalino_img, dark_image=conect_bitalino_img, size=(conect_bitalino_img.width, conect_bitalino_img.height))
        self.button_conectbt_img_dim = ctk.CTkImage(light_image=conect_bitalino_img_dim, dark_image=conect_bitalino_img_dim, size=(conect_bitalino_img_dim.width, conect_bitalino_img_dim.height))
        self.button_conectbt_img_conectado = ctk.CTkImage(light_image=conectado_bitalino, dark_image=conectado_bitalino, size=(conectado_bitalino.width, conectado_bitalino.height))

        self.button_conect_bitalino = ctk.CTkButton(self, image=self.button_conectbt_img, bg_color=ROSA, fg_color=TRANSPARENTE, 
                                                    text="", border_color=AZUL, border_spacing=0, hover=False, hover_color=AZUL_CLARO,
                                                    command= lambda: self.conect_bitalino(self.mac_addr_var.get()))
        self.button_conect_bitalino.grid(row=0, column=2, pady=20, padx=10, sticky=ctk.NSEW)
        self.button_conect_bitalino.bind('<Enter>', lambda event:self.button_conect_bitalino.configure(image=self.button_conectbt_img_dim))
        self.button_conect_bitalino.bind('<Leave>', lambda event:self.button_conect_bitalino.configure(image=self.button_conectbt_img))
    
    def update_mac_addresses(self):
        """
        Atualiza as opções do ComboBox de endereços MAC com uma nova lista de endereços.

        :param mac_addresses: Uma lista de strings representando os endereços MAC disponíveis.
        :return: None
        """
        mac_addresses = run_scan_devices()
        mac_addresses = mac_addresses if mac_addresses is not None else ["Sem dispositivos encontrados..."]
        self.up_select_macaddr.configure(values=mac_addresses)
    
    def conect_bitalino(self, mac_addr: str):
        """
        Conecta ao dispositivo Bitalino usando o endereço MAC selecionado no ComboBox. 
        O endereço MAC é obtido a partir da variável associada ao ComboBox.

        :return: None
        """
        self.mac_addr: str = mac_addr
        self.bitalino = connectar_bitalino(mac_addr=self.mac_addr)

        if isinstance(self.bitalino, str):
            CTkMessagebox(title="Erro na conexão", message=self.bitalino, icon="warning", option_1="OK",
                          fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO, 
                          font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                          button_text_color=CINZA, corner_radius=CORNER, sound=True,
                          width=500, height=300)
        else:
            self.button_conect_bitalino.configure(state="disabled", image=self.button_conectbt_img_conectado)
    
class MidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, bg_color=AZUL, fg_color=ROSA, border_color=AZUL)
        set_grids(self, rows_conf={3:[0], 1:[1]}, column_conf={1:[0], 3:[1]}, grid_row=1)
        
        self.up_left_mid_frame = UpLeftMidFrame(self)
        self.upright_mid_frame = UpRightMidFrame(self)
        self.down_mid_frame = DownMidFrame(self)

class UpLeftMidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH_INSIDE, bg_color=ROSA, fg_color=AZUL_CLARO, border_color=AZUL, background_corner_colors=(ROSA, ROSA, ROSA, ROSA))
        set_grids(self, rows_conf={1:[0,1,2,3]}, column_conf={0:[0], 3:[1]}, padx=20, pady=20)

        self.name_label = ctk.CTkLabel(self, text="Nome:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.name_label.grid(row=0, column=0, padx=15, pady=15, sticky=ctk.E)
        self.name_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=300, 
                                       bg_color=AZUL_CLARO, fg_color=ROSA, placeholder_text="Digite o nome do participante", 
                                       placeholder_text_color=CINZA, font=BASE_FONT_MIN, text_color=CINZA)
        self.name_entry.grid(row=0, column=1, padx=15, pady=15, sticky=ctk.EW)


        self.idade_label = ctk.CTkLabel(self, text="Idade:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.idade_label.grid(row=1, column=0, padx=15, pady=15, sticky=ctk.E)
        self.idade_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=300,
                                       bg_color=AZUL_CLARO, fg_color=ROSA, placeholder_text="Digite a idade do participante",
                                       placeholder_text_color=CINZA, font=BASE_FONT_MIN, text_color=CINZA)
        self.idade_entry.grid(row=1, column=1, padx=15, pady=15, sticky=ctk.EW)

        self.genero_label = ctk.CTkLabel(self, text="Gênero:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.genero_label.grid(row=2, column=0, padx=15, pady=15, sticky=ctk.E)
        self.genero_entry = ctk.CTkEntry(self, corner_radius=CORNER, width=300, border_width=BORDER_WIDTH, border_color=AZUL,
                                         bg_color=AZUL_CLARO, fg_color=ROSA, placeholder_text="Digite o gênero do participante",
                                         placeholder_text_color=CINZA, font=BASE_FONT_MIN, text_color=CINZA)
        self.genero_entry.grid(row=2, column=1, padx=15, pady=15, sticky=ctk.EW)

        self.save_infos_button = ctk.CTkButton(self, text="Salvar informações", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA)
        self.save_infos_button.grid(row=3, columnspan=2, padx=15, pady=15, sticky=NSE)

class UpRightMidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH_INSIDE, bg_color=ROSA, fg_color=AZUL_CLARO, border_color=AZUL, background_corner_colors=(ROSA, ROSA, ROSA, ROSA))
        set_grids(self, rows_conf={1:[0,1]}, column_conf={1:[0,2], 3:[1]}, grid_column=1, padx=20, pady=20)

        self.load_file_label = ctk.CTkLabel(self, text="Arquivo de músicas:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.load_file_label.grid(row=0, column=0, padx=10, pady=20, sticky=ctk.E)

        self.music_file = ctk.StringVar(value="arquivo/musicas.xlsx")

        self.load_file_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=420, 
                                            placeholder_text="Diretório do arquivo de músicas", placeholder_text_color=CINZA,
                                            bg_color=AZUL_CLARO, fg_color=ROSA, textvariable=self.music_file,  
                                            font=BASE_FONT_MIN, text_color=CINZA, state="readonly")
        self.load_file_entry.grid(row=0, column=1, padx=10, pady=20, sticky=ctk.EW)

        self.load_file_button = ctk.CTkButton(self, text="Carregar", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA)
        self.load_file_button.grid(row=0, column=2, padx=10, pady=20, sticky=ctk.W)

        self.salvar_arquivos_label = ctk.CTkLabel(self, text="Salvar dados em:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.salvar_arquivos_label.grid(row=1, column=0, padx=10, pady=20, sticky=ctk.E)

        self.salvar_arquivos_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=420,
                                            bg_color=AZUL_CLARO, fg_color=ROSA, placeholder_text="Diretório para salvar os dados", 
                                            placeholder_text_color=CINZA, font=BASE_FONT_MIN, text_color=CINZA)
        self.salvar_arquivos_entry.grid(row=1, column=1, padx=10, pady=20, sticky=ctk.EW)

        self.salvar_arquivos_button = ctk.CTkButton(self, text="Escolher", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA)
        self.salvar_arquivos_button.grid(row=1, column=2, padx=10, pady=20, sticky=ctk.W)

        self.flies_infos_label = ctk.CTkLabel(self, text="Esperando a seleção de músicas, pausas e ruídos...", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.flies_infos_label.grid(row=2, column=1, padx=10, pady=20, sticky=ctk.NS)

class DownMidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH_INSIDE, bg_color=ROSA, fg_color=AZUL_CLARO, border_color=AZUL, background_corner_colors=(ROSA, ROSA, ROSA, ROSA))
        set_grids(self, rows_conf={1:[0,1]}, column_conf={1:[0,1,2,3]}, grid_row=1, columnspan=2, padx=20, pady=20)

        self.music_name_label = ctk.CTkLabel(self, text="Música: Nada igual - Terno Rei", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_name_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, ipadx=10, sticky=ctk.W)

        self.music_volume = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=AZUL_CLARO, fg_color=ROSA,
                                          button_color=AMARELO, button_hover_color=AMARELO_ESC, progress_color=AMARELO)
        self.music_volume.grid(row=0, column=3, padx=20, pady=15, sticky=ctk.EW)

        self.music_volume_label = ctk.CTkLabel(self, text="Volume: 50%", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_volume_label.grid(row=0, column=2, padx=10, pady=15, sticky=ctk.E)

        self.music_progress = ctk.CTkProgressBar(self, height=10, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=AZUL_CLARO, fg_color=ROSA, progress_color=CINZA)
        self.music_progress.grid(row=1, column=0, columnspan=4, padx=80, pady=20, sticky=ctk.NSEW)

        self.music_time_begin = ctk.CTkLabel(self, text="00:00", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_time_begin.grid(row=1, column=3, padx=20, pady=10, sticky=ctk.E)

        self.music_time_end = ctk.CTkLabel(self, text="00:00", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_time_end.grid(row=1, column=0, padx=20, pady=10, sticky=ctk.W)

class DownFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, bg_color=AZUL, fg_color=ROSA, border_color=AZUL)
        set_grids(self, rows_conf={1:[0,1,2]}, column_conf={1:[0,1,2]}, grid_row=2)

        self.exp_progress_music_label = ctk.CTkLabel(self, text="Música: 0 de 20", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_music_label.grid(row=0, column=0, padx=15, pady=10, sticky=ctk.W)

        self.exp_progress_pausas_label = ctk.CTkLabel(self, text="Pausa: 0 de 5", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_pausas_label.grid(row=1, column=0, padx=15, pady=10, sticky=ctk.W)

        self.exp_progress_ruido_label = ctk.CTkLabel(self, text="Ruído: 0 de 5", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_ruido_label.grid(row=2, column=0, padx=15, pady=10, sticky=ctk.W)

        self.infos_label = ctk.CTkLabel(self, text="Conecte o Bitalino", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.infos_label.grid(row=1, column=1, padx=15, pady=10, sticky=NSE)

        bt_comeca_img = Image.open(r'assets\comecar.png')
        bt_comeca_img_dim = Image.open(r'assets\comecar_dim.png')

        self.button_comecar_img = ctk.CTkImage(light_image=bt_comeca_img, dark_image=bt_comeca_img, size=(bt_comeca_img.width, bt_comeca_img.height))
        self.button_comecar_img_dim = ctk.CTkImage(light_image=bt_comeca_img_dim, dark_image=bt_comeca_img_dim, size=(bt_comeca_img_dim.width, bt_comeca_img_dim.height))
        self.button_exemple = ctk.CTkButton(self, image=self.button_comecar_img,bg_color=TRANSPARENTE, fg_color=TRANSPARENTE, text="", hover=False)
        self.button_exemple.grid(row=0, rowspan=3, column=2, pady=20, padx=20, sticky=NSE)
        self.button_exemple.bind('<Enter>', lambda event:self.button_exemple.configure(image=self.button_comecar_img_dim))
        self.button_exemple.bind('<Leave>', lambda event:self.button_exemple.configure(image=self.button_comecar_img))

if __name__ == "__main__":
    app = Compasso()
    app.mainloop()