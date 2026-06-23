import os
import platform

from PIL import Image

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from pycaw.pycaw import AudioUtilities

from . import gui_logger
from . import set_window_grid, set_window_configs, set_grids
from src.core import connectar_bitalino, run_scan_devices
from src.core.player import Player
from tkinter import filedialog
import threading
import pandas as pd

ctk.set_appearance_mode("system")

WIN_MIN_WIDTH: int = 1280
WIN_MIN_HEIGHT: int = 768
BORDER_WIDTH: int = 5
BORDER_WIDTH_INSIDE: int = 8
CORNER: int = 30

"""Forestgreen #228B22
PaleGoldenrod #EEE8AA
Seashell4 #8B8682"""

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
        self.minsize(WIN_MIN_WIDTH, WIN_MIN_HEIGHT)
        set_window_configs(self, width_multip=0.5, height_multip=0.5)
        set_window_grid(self)

        self.main_frame = MainFrame(self)

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        set_grids(self, rows_conf={1:[0,2], 4:[1]}, column_conf={1:[0]})
        gui_logger.logger.info("MainFrame iniciado.")
        
        self.player = Player()

        self.up_frame = UpFrame(self)
        self.mid_frame = MidFrame(self)
        self.down_frame = DownFrame(self)
        
        self.after(100, self.mid_frame.upright_mid_frame.check_music_file_infos)

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
                                                 font=BASE_FONT_MIN, dropdown_font=BASE_FONT_MIN)
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
        Inicia o escaneamento de dispositivos BLE em uma thread separada, para não
        travar a GUI durante os ~3s do BleakScanner. O ComboBox é atualizado na
        thread principal via after().

        :return: None
        """
        self.refresh_mac_button.configure(state="disabled", text="...")
        threading.Thread(target=self._scan_devices_worker, daemon=True).start()

    def _scan_devices_worker(self):
        """Executa o scan BLE (bloqueante) fora da thread da GUI."""
        try:
            mac_addresses = run_scan_devices()
        except Exception as e:
            gui_logger.logger.error(f"Erro durante o escaneamento de dispositivos: {e}")
            mac_addresses = None
        mac_addresses = mac_addresses if mac_addresses else ["Sem dispositivos encontrados..."]
        self.after(10, lambda: self._update_mac_combobox(mac_addresses))

    def _update_mac_combobox(self, mac_addresses: list):
        """Atualiza o ComboBox e reabilita o botão de scan (thread principal)."""
        self.up_select_macaddr.configure(values=mac_addresses)
        self.refresh_mac_button.configure(state="normal", text="Escanear")

    def conect_bitalino(self, mac_addr: str):
        """
        Conecta ao dispositivo Bitalino em uma thread separada, para não travar a GUI
        durante o timeout do resolve_byprop (até ~2s). O resultado é tratado na thread
        principal via after().

        :param mac_addr: Endereço MAC selecionado no ComboBox.
        :return: None
        """
        gui_logger.logger.info(f"Solicitada conexão ao Bitalino com MAC: {mac_addr}, type: {type(mac_addr)}")
        self.mac_addr: str = mac_addr.split(" - ")[-1]  # extrai o MAC do formato "Nome do dispositivo - MAC"
        gui_logger.logger.info(f"Endereço MAC extraído para conexão: {self.mac_addr}")
        self.button_conect_bitalino.configure(state="disabled")
        threading.Thread(target=self._connect_bitalino_worker, args=(self.mac_addr,), daemon=True).start()

    def _connect_bitalino_worker(self, mac_addr: str):
        """Executa a conexão LSL (bloqueante) fora da thread da GUI."""
        gui_logger.logger.info(f"Conectando ao Bitalino com MAC: {mac_addr}")
        bitalino = connectar_bitalino(mac_addr=mac_addr)
        self.after(10, lambda: self._handle_connection_result(bitalino))

    def _handle_connection_result(self, bitalino):
        """
        Trata o resultado da tentativa de conexão. 
        Se for uma string, é um erro; caso contrário, é o objeto de conexão.
        
        """
        if isinstance(bitalino, str):
            self.button_conect_bitalino.configure(state="normal")
            CTkMessagebox(title="Erro na conexão", message=bitalino, icon="warning", option_1="OK",
                          fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                          font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                          button_text_color=CINZA, corner_radius=CORNER, sound=True,
                          width=500, height=300)
        else:
            self.bitalino = bitalino
            self.bitalino_connected = True
            self.button_conect_bitalino.unbind('<Enter>')
            self.button_conect_bitalino.unbind('<Leave>')
            self.button_conect_bitalino.configure(state="disabled", image=self.button_conectbt_img_conectado)
            self.refresh_mac_button.configure(state="disabled")
            self.up_select_macaddr.configure(state="disabled")
    
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
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self.save_infos)
        self.save_infos_button.grid(row=3, column=1, padx=15, pady=15, sticky=NSE)

    def save_infos(self):

        nome = self.name_entry.get().strip()
        idade = self.idade_entry.get().strip()
        genero = self.genero_entry.get().strip()

        if not self.validade_name_genero(nome, genero):
            CTkMessagebox(title="Erro", message="Nome e gênero devem conter apenas letras e espaços.", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)
            return

        if not self.validade_idade(idade):
            CTkMessagebox(title="Erro", message="Idade deve ser um número entre 0 e 100.", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)
            return

        gui_logger.logger.info(f"Salvando informações do participante - Nome: {nome}, Idade: {idade}, Gênero: {genero}")

        if not nome or not idade or not genero:
            CTkMessagebox(title="Erro", message="Todos os campos são obrigatórios.", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)
            return

        self.nome = nome
        self.idade = idade
        self.genero = genero

        self.save_infos_button.configure(state="disabled")
        self.name_entry.configure(state="disabled")
        self.idade_entry.configure(state="disabled")
        self.genero_entry.configure(state="disabled")

        self.edit_infos_button = ctk.CTkButton(self, text="Editar informações", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self.edit_infos)
        self.edit_infos_button.grid(row=3, column=1, padx=15, pady=15, sticky=ctk.W)

        self.infos_saved = True

        gui_logger.logger.info("Informações do participante salvas com sucesso.")

        return
    
    def edit_infos(self):
        gui_logger.logger.info("Habilitando edição das informações do participante.")
        self.infos_saved = False
        self.save_infos_button.configure(state="normal")
        self.name_entry.configure(state="normal")
        self.idade_entry.configure(state="normal")
        self.genero_entry.configure(state="normal")
        self.edit_infos_button.destroy()
    
    def validade_name_genero(self, name: str, genero: str) -> bool:
        """Valida o nome e gênero do participante. O nome deve conter apenas letras e espaços, e o gênero deve ser 'masculino', 'feminino' ou 'outro'."""
        gui_logger.logger.info(f"Validando nome e gênero - Nome: {name}, Gênero: {genero}")
        if not all(c.isalpha() or c.isspace() for c in name):
            return False
        if not all(c.isalpha() or c.isspace() for c in genero):
            return False
        return True

    def validade_idade(self, idade: str) -> bool:
        """Valida a idade do participante. A idade deve ser um número inteiro entre0 e 100."""
        gui_logger.logger.info(f"Validando idade: {idade}")
        try:
            if not idade.isdigit():
                return False
            idade_int = int(idade)
            if idade_int < 0 or idade_int > 100:
                return False
        except ValueError as e:
            gui_logger.logger.error(f"Erro ao validar idade: {e}")
            return False
        return True

class UpRightMidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH_INSIDE, bg_color=ROSA, fg_color=AZUL_CLARO, border_color=AZUL, background_corner_colors=(ROSA, ROSA, ROSA, ROSA))
        set_grids(self, rows_conf={1:[0,1,2,3]}, column_conf={1:[0,2], 3:[1]}, grid_column=1, padx=20, pady=20)

        self.load_file_label = ctk.CTkLabel(self, text="Arquivos de músicas:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.load_file_label.grid(row=0, column=0, padx=15, pady=15, sticky=ctk.E)

        self.music_file_folder_var = ctk.StringVar(value=r"Pasta contendo os arquivos de música")

        self.load_file_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=420, 
                                            placeholder_text="Diretório do arquivo de músicas", placeholder_text_color=CINZA,
                                            bg_color=AZUL_CLARO, fg_color=ROSA, textvariable=self.music_file_folder_var,  
                                            font=BASE_FONT_MIN, text_color=CINZA, state="readonly")
        self.load_file_entry.grid(row=0, column=1, padx=15, pady=15, sticky=ctk.EW)

        self.load_file_button = ctk.CTkButton(self, text="Carregar", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self.load_music_folder)
        self.load_file_button.grid(row=0, column=2, padx=15, pady=15, sticky=ctk.W)

        self.load_conditions = ctk.CTkLabel(self, text="Condições:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.load_conditions.grid(row=1, column=0, padx=15, pady=15, sticky=ctk.E)

        self.conditions_file_var = ctk.StringVar(value="Excel contendo as condições ou fatores das músicas")

        self.conditions_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=420, 
                                            placeholder_text="Arquivo excel com as condições ou fatores das musicas", placeholder_text_color=CINZA,
                                            bg_color=AZUL_CLARO, fg_color=ROSA, textvariable=self.conditions_file_var,  
                                            font=BASE_FONT_MIN, text_color=CINZA, state="readonly")
        self.conditions_entry.grid(row=1, column=1, padx=15, pady=15, sticky=ctk.EW)

        self.conditions_button = ctk.CTkButton(self, text="Buscar", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self.load_conditions_file)
        self.conditions_button.grid(row=1, column=2, padx=15, pady=15, sticky=ctk.W)


        self.salvar_arquivos_label = ctk.CTkLabel(self, text="Salvar dados em:", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.salvar_arquivos_label.grid(row=2, column=0, padx=15, pady=15, sticky=ctk.E)

        self.salvar_arquivos_var = ctk.StringVar(value="Diretório para salvar os dados")

        self.salvar_arquivos_entry = ctk.CTkEntry(self, corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=420,
                                            bg_color=AZUL_CLARO, fg_color=ROSA, placeholder_text="Diretório para salvar os dados", 
                                            placeholder_text_color=CINZA, font=BASE_FONT_MIN, text_color=CINZA, textvariable=self.salvar_arquivos_var, state="readonly")
        self.salvar_arquivos_entry.grid(row=2, column=1, padx=15, pady=15, sticky=ctk.EW)

        self.salvar_arquivos_button = ctk.CTkButton(self, text="Escolher", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self._choose_save_directory)
        self.salvar_arquivos_button.grid(row=2, column=2, padx=15, pady=15, sticky=ctk.W)

        self.files_infos_label = ctk.CTkLabel(self, text="Selecione as músicas, pausas, ruídos e a pasta para salvar os dados", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.files_infos_label.grid(row=3, column=0, columnspan=3, padx=15, pady=15, sticky=ctk.NS)

    def load_music_folder(self):
        path = filedialog.askdirectory(title="Selecione uma pasta contendo os arquivos de música", initialdir=".")
        if not path:
            return
        try:
            if os.path.exists(path):
                self.music_file_folder_var.set(path)
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar pasta com as músicas: {e}", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)

    def load_conditions_file(self):
        path = filedialog.askopenfilename(title="Selecione um arquivo excel contendo as condições ou fatores das músicas", initialdir=".", filetypes=[("Excel files", "*.xlsx *.xls")])
        if not path:
            return
        try:
            if os.path.exists(path):
                self.conditions_file_var.set(path)
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar arquivo com as condições: {e}", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)

    def _choose_save_directory(self):
        path = filedialog.askdirectory(title="Selecione um diretório para salvar os dados", initialdir=".")
        if not path:
            return
        try:
            if os.path.exists(path):
                self.salvar_arquivos_var.set(path)
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Erro ao carregar diretório para salvar dados: {e}", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)
    
    def check_music_file_infos(self):
        """Verifica se as informações dos arquivos de música, condições e pasta de salvamento foram selecionadas. 
        Se não, exibe mensagens de erro e continua verificando a cada 100ms até que tudo esteja correto."""

        if not self.music_file_folder_var.get() or self.music_file_folder_var.get() == "Pasta contendo os arquivos de música":
            self.files_infos_label.configure(text="Selecione a pasta contendo os arquivos de música.")
            self.after(100, self.check_music_file_infos)
            return
        elif not self.conditions_file_var.get() or self.conditions_file_var.get() == "Excel contendo as condições ou fatores das músicas":
            self.files_infos_label.configure(text="Selecione o arquivo excel contendo as condições ou fatores das músicas.")
            self.after(100, self.check_music_file_infos)
            return
        elif not self.salvar_arquivos_var.get() or self.salvar_arquivos_var.get() == "Diretório para salvar os dados":
            self.files_infos_label.configure(text="Selecione o diretório para salvar os dados.")
            self.after(100, self.check_music_file_infos)
            return
        else:
            threading.Thread(target=self.get_musics_from_folder, daemon=True).start()
            self.files_infos_label.configure(text="Arquivos de música e pasta de salvamento selecionados! Tudo certo.")
            self.music_and_conditions_selected = True

    def get_musics_from_folder(self):
        """
        Obtém os arquivos de música da pasta selecionada e verifica se eles existem. 
        Se algum arquivo estiver faltando, exibe uma mensagem de erro.

        """

        pasta_com_musicas = self.music_file_folder_var.get()

        if not os.path.exists(pasta_com_musicas):
            CTkMessagebox(title="Erro", message=f"Pasta de músicas não encontrada: {pasta_com_musicas}.\nPor favor, verifique o caminho e tente novamente.", icon="cancel", option_1="OK",
                        fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                        font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                        button_text_color=CINZA, corner_radius=CORNER, sound=True,
                        width=500, height=300)
            return
        
        music_files = [os.path.join(pasta_com_musicas, f) for f in os.listdir(pasta_com_musicas) if f.endswith(('.mp3', '.wav', '.ogg'))]

        for music in music_files:
            if os.path.exists(music):
                gui_logger.logger.info(f"Arquivo de música encontrado: {music}")
                continue
            else:
                gui_logger.logger.warning(f"Arquivo de música não encontrado: {music}")
                CTkMessagebox(title="Erro", message=f"Arquivo de música não encontrado: {music}.\nPor favor, verifique o arquivo e tente novamente.", icon="cancel", option_1="OK",
                            fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                            font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                            button_text_color=CINZA, corner_radius=CORNER, sound=True,
                            width=500, height=300)
                return
        self.music_files = music_files
        self.files_infos_label.configure(text="Arquivos de música encontrados! Verificando condições...")
        threading.Thread(target=self.match_condition_with_music_file, args=(music_files,), daemon=True).start()
        return
        
    def match_condition_with_music_file(self, music_files: list):
        
        cond_match_result = {}
        cond_path = self.conditions_file_var.get()

        if os.path.exists(cond_path):
            conditions_file: pd.DataFrame = pd.read_excel(cond_path)
        else:
            CTkMessagebox(title="Erro", message=f"Arquivo de condições não encontrado: {cond_path}.\nPor favor, verifique o arquivo e tente novamente.",
                          icon="cancel", option_1="OK",
                          fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                          font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                          button_text_color=CINZA, corner_radius=CORNER, sound=True,
                          width=500, height=300)
            return
        
        if music_files and not conditions_file.empty and 'musica' in conditions_file.columns and 'fator' in conditions_file.columns:

            for music in music_files:
                music_name = os.path.basename(music)
                condition = conditions_file.loc[conditions_file['musica'] == music_name, 'fator'].values
                if len(condition) > 0:
                    cond_match_result[music] = condition[0]
                    gui_logger.logger.info(f"Condição encontrada para {music_name}: {condition[0]}")
                else:
                    CTkMessagebox(title="Atenção", message=f"Nenhuma condição encontrada para {music_name} no arquivo de condições.\nEssa música será ignorada durante o experimento.",
                                  icon="warning", option_1="OK",
                                  fg_color=ROSA, bg_color=AZUL, text_color=CINZA, button_color=AZUL_CLARO, button_hover_color=AMARELO,
                                  font=BASE_FONT_MIN, border_color=AZUL, border_width=BORDER_WIDTH, title_color=CINZA,
                                  button_text_color=CINZA, corner_radius=CORNER, sound=True,
                                  width=500, height=300)
                    gui_logger.logger.warning(f"Nenhuma condição encontrada para {music_name} no arquivo de condições.")
                    return
                
            self.music_condition_mapping = cond_match_result
            self.after(1000, lambda: self.files_infos_label.configure(text="Mapemento de músicas para condições realizado com sucesso!"))
            gui_logger.logger.info("Mapemento de músicas e condições realizado com sucesso!")
            return
        else:
            self.after(1000, lambda: self.files_infos_label.configure(text="Nenhuma condição encontrada para as músicas selecionadas."))
            gui_logger.logger.warning("Nenhuma condição encontrada para as músicas selecionadas.")
            return

class DownMidFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH_INSIDE, bg_color=ROSA, fg_color=AZUL_CLARO, border_color=AZUL, background_corner_colors=(ROSA, ROSA, ROSA, ROSA))
        set_grids(self, rows_conf={1:[0,1,2]}, column_conf={1:[0,1,2,3]}, grid_row=1, columnspan=2, padx=20, pady=20)

        self.music_name_label = ctk.CTkLabel(self, text="Música: Nada igual - Terno Rei", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_name_label.grid(row=0, column=0, columnspan=2, padx=20, pady=15, ipadx=10, sticky=ctk.W)

        self.music_volume = ctk.CTkSlider(self, from_=0, to=100, number_of_steps=100, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=AZUL_CLARO, fg_color=ROSA,
                                          button_color=AMARELO, button_hover_color=AMARELO_ESC, progress_color=AMARELO, command=self._on_volume_change)
        self.music_volume.grid(row=0, column=3, padx=20, pady=15, sticky=ctk.EW)

        self.music_volume_label = ctk.CTkLabel(self, text="Volume: 50%", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_volume_label.grid(row=0, column=2, padx=10, pady=15, sticky=ctk.E)

        self.music_progress = ctk.CTkProgressBar(self, height=10, border_width=BORDER_WIDTH, border_color=AZUL, bg_color=AZUL_CLARO, fg_color=ROSA, progress_color=CINZA)
        self.music_progress.grid(row=1, column=0, columnspan=4, padx=80, pady=20, sticky=ctk.NSEW)

        self.music_time_begin = ctk.CTkLabel(self, text="00:00", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_time_begin.grid(row=1, column=3, padx=20, pady=10, sticky=ctk.E)

        self.music_time_end = ctk.CTkLabel(self, text="00:00", font=BASE_FONT, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.music_time_end.grid(row=1, column=0, padx=20, pady=10, sticky=ctk.W)

        self.stop_button = ctk.CTkButton(self, text="Parar", corner_radius=CORNER, border_width=BORDER_WIDTH, border_color=AZUL, width=80,
                                              bg_color=AZUL_CLARO, fg_color=ROSA, hover_color=AZUL, font=BASE_FONT_MIN, text_color=CINZA,
                                              command=self._on_stop)
        self.stop_button.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NS)


        self.after(500, self._update_progress)

    def _format_time(self, secs: float) -> str:
        try:
            secs = int(secs)
            m = secs // 60
            s = secs % 60
            return f"{m:02d}:{s:02d}"
        except Exception:
            return "00:00"

    def _get_player(self):
        return getattr(self.master, 'player', None)

    def _set_info(self, text: str):
        """Atualiza o label de informações (definido em DownFrame) de forma segura.

        O label `infos_label` pertence ao DownFrame, não ao DownMidFrame. O caminho é:
        DownMidFrame -> master (MidFrame) -> master (MainFrame) -> down_frame -> infos_label.
        """
        try:
            self.master.master.down_frame.down_infos_label.configure(text=text)
        except Exception:
            gui_logger.logger.warning(f"Não foi possível atualizar infos_label: {text}")

    def _on_stop(self):
        player = self._get_player()
        if not player:
            return
        try:
            if getattr(player, '_playlist_loaded', False):
                player.stop_playlist()
            else:
                player.stop()
        except Exception:
            pass
        
    def set_volume(self, percentage):
        """
        Define o volume do player de música. 
        O valor é garantido para ficar entre 0 e 100.
        """
        # Garante que o valor digitado fique estritamente entre 0 e 100
        percentage = max(0, min(100, percentage))
        os_name = platform.system()

        try:
            if os_name == 'Windows':
                
                
                # Obtém o dispositivo de áudio principal (alto-falantes)
                device = AudioUtilities.GetSpeakers()
                
                # Na nova API do pycaw, acessamos a interface de volume diretamente
                volume = device.EndpointVolume
                
                # Ajusta o volume (aceita escala de 0.0 a 1.0)
                volume.SetMasterVolumeLevelScalar(percentage / 100.0, None)
        except Exception as e:
            gui_logger.logger.error(f"Erro ao ajustar volume no Windows: {e}")

    def _on_volume_change(self, value):
        #gui_logger.logger.info(f"Value = {value}%")
        try:
            self.music_volume_label.configure(text=f"Volume: {int(float(value))}%")
            self.set_volume(int(value))
        except Exception:
            pass

    def _update_progress(self):
        player = self._get_player()
        pos = 0.0
        length = 0.0
        try:
            if player:
                pos = float(player.get_pos() or 0.0)
                length = float(player.get_length() or 0.0)
        except Exception:
            pass
        # update labels
        try:
            self.music_time_begin.configure(text=self._format_time(pos))
            self.music_time_end.configure(text=self._format_time(length))
            if length > 0:
                prog = max(0.0, min(1.0, pos / length))
            else:
                prog = 0.0
            try:
                self.music_progress.set(prog)
            except Exception:
                pass
        except Exception:
            pass
        # reschedule
        try:
            self.after(500, self._update_progress)
        except Exception:
            pass

class DownFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=CORNER, border_width=BORDER_WIDTH, bg_color=AZUL, fg_color=ROSA, border_color=AZUL)
        set_grids(self, rows_conf={1:[0,1,2]}, column_conf={1:[0,1,2]}, grid_row=2)

        self.master = master

        self.exp_progress_music_label = ctk.CTkLabel(self, text="Música: 0 de 20", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_music_label.grid(row=0, column=0, padx=15, pady=10, sticky=ctk.W)

        self.exp_progress_pausas_label = ctk.CTkLabel(self, text="Pausa: 0 de 5", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_pausas_label.grid(row=1, column=0, padx=15, pady=10, sticky=ctk.W)

        self.exp_progress_ruido_label = ctk.CTkLabel(self, text="Ruído: 0 de 5", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.exp_progress_ruido_label.grid(row=2, column=0, padx=15, pady=10, sticky=ctk.W)

        self.down_infos_label = ctk.CTkLabel(self, text="Conecte o Bitalino", font=BASE_FONT_MIN, text_color=CINZA, bg_color=TRANSPARENTE, fg_color=TRANSPARENTE)
        self.down_infos_label.grid(row=1, column=1, padx=15, pady=10, sticky=NSE)

        bt_comeca_img = Image.open(r'assets\comecar.png')
        bt_comeca_img_dim = Image.open(r'assets\comecar_dim.png')
        self.button_comecar_img = ctk.CTkImage(light_image=bt_comeca_img, dark_image=bt_comeca_img, size=(bt_comeca_img.width, bt_comeca_img.height))
        self.button_comecar_img_dim = ctk.CTkImage(light_image=bt_comeca_img_dim, dark_image=bt_comeca_img_dim, size=(bt_comeca_img_dim.width, bt_comeca_img_dim.height))

        self.comecar_bt = ctk.CTkButton(self, image=self.button_comecar_img,bg_color=TRANSPARENTE, fg_color=TRANSPARENTE, text="", hover=False, command=self.comecar_experimento)
        self.comecar_bt.grid(row=0, rowspan=3, column=2, pady=20, padx=20, sticky=NSE)
        self.comecar_bt.bind('<Enter>', lambda event:self.comecar_bt.configure(image=self.button_comecar_img_dim))
        self.comecar_bt.bind('<Leave>', lambda event:self.comecar_bt.configure(image=self.button_comecar_img))

    def comecar_experimento(self):
        self.down_infos_label.configure(text="Iniciando experimento...")
        # aqui você pode chamar a função que inicia o experimento, passando os parâmetros necessários
        # por exemplo: start_experiment(self.music_file_folder.get(), self.conditions_file.get(), self.salvar_arquivos_var.get())

    
    #def pick_one_music(self, music_name: str):
    #    self.music_name_label.configure(text=f"Música: {music_name}")


    def update_experiment_progress(self, music_prog: str, pausas_prog: str, ruido_prog: str):
        self.exp_progress_music_label.configure(text=f"Música: {music_prog}")
        self.exp_progress_pausas_label.configure(text=f"Pausa: {pausas_prog}")
        self.exp_progress_ruido_label.configure(text=f"Ruído: {ruido_prog}")

if __name__ == "__main__":
    app = Compasso()
    app.mainloop()