import os
import tkinter
from tkinter import filedialog, messagebox

import customtkinter as ctk

from . import gui_logger
from . import set_window_configs
from .context import AppContext
from .assets import AppImages, ASSETS_DIR
from .theme import WIN_BG, TRANSPARENTE, WIN_MIN_WIDTH, WIN_MIN_HEIGHT
from .frames import (ConnectionFrame, StepperFrame, ParticipantCard, FilesCard,
                     PlayerBar, GraphPlaceholder, DownFrame)
from .experiment_config_window import ExperimentConfigWindow
from src.core import config_manager

ctk.set_appearance_mode("dark")

class Compasso(ctk.CTk):
    """Janela raiz: cria o `AppContext` e monta o `MainFrame` (tema escuro)."""

    def __init__(self, nome="ComPasso"):
        super().__init__(fg_color=WIN_BG)
        self.title(nome)
        self.minsize(WIN_MIN_WIDTH, WIN_MIN_HEIGHT)
        set_window_configs(self, width_multip=0.5, height_multip=0.6)

        # ícone da janela principal (Windows usa .ico; em outros SOs o ícone vem do bundle)
        try:
            self.iconbitmap(str(ASSETS_DIR / "icon.ico"))
        except Exception as e:
            gui_logger.logger.warning(f"Não foi possível definir o ícone da janela: {e}")

        self.ctx = AppContext(self)
        self.ctx.images = AppImages()   # carregado após o root existir (mantido por compat.)

        self.main_frame = MainFrame(self, self.ctx)
        self.main_frame.pack(fill="both", expand=True)

        # menu "Experimento" + sistema de configuração (.config)
        self._loaded_config_path = None
        self._loaded_config_data = None
        self._build_menu()
        self._auto_load_config()

    # ------------------------------------------------------------------ #
    def _build_menu(self):
        """Cria a barra de menus com o menu 'Experimento' (Novo/Abrir/Editar)."""
        menubar = tkinter.Menu(self)
        self._experimento_menu = tkinter.Menu(menubar, tearoff=0)
        self._experimento_menu.add_command(label="Novo", command=self._on_novo)
        self._experimento_menu.add_command(label="Abrir", command=self._on_abrir)
        self._experimento_menu.add_command(label="Editar", command=self._on_editar, state="disabled")
        menubar.add_cascade(label="Experimento", menu=self._experimento_menu)
        # CTk.configure filtra kwargs desconhecidos; anexa o menu pelo método base do Tk
        tkinter.Tk.config(self, menu=menubar)

    def _enable_editar(self):
        try:
            self._experimento_menu.entryconfigure("Editar", state="normal")
        except Exception as e:
            gui_logger.logger.warning(f"Não foi possível habilitar 'Editar': {e}")

    def _on_novo(self):
        ExperimentConfigWindow(self, mode="novo", on_saved=self._on_config_saved)

    def _on_editar(self):
        if not self._loaded_config_data:
            return
        ExperimentConfigWindow(self, mode="editar", on_saved=self._on_config_saved,
                               initial=self._loaded_config_data, config_path=self._loaded_config_path)

    def _on_abrir(self):
        path = filedialog.askopenfilename(parent=self, title="Abrir configuração",
                                          initialdir=str(config_manager.get_experiment_files_dir()),
                                          filetypes=[("Config files", "*.config")])
        if not path:
            return
        data, errors = config_manager.load_config(path)
        if errors:
            messagebox.showerror("Arquivo inválido", "O arquivo de configuração contém problemas:\n\n" + "\n".join(errors))
            return
        if data is None:
            messagebox.showerror("Erro", "Falha ao carregar o arquivo de configuração.")
            return
        gui_logger.logger.info(f"Configuração carregada: {path}")
        self._set_current_config(path, data)
        self.apply_config(data)
        self._show_temp_status("Configuração carregada com sucesso.", 3000)

    def _on_config_saved(self, path, data):
        """Callback após salvar (Novo/Editar): adota a config, aplica e habilita 'Editar'."""
        self._set_current_config(path, data)
        self.apply_config(data)

    def _set_current_config(self, path, data):
        self._loaded_config_path = path
        self._loaded_config_data = data
        config_manager.set_last_config(path)
        self._enable_editar()

    def _auto_load_config(self):
        """Carrega silenciosamente a última configuração usada, se válida."""
        path = config_manager.get_last_config_path()
        if not path or not os.path.exists(path):
            return
        data, errors = config_manager.load_config(path)
        if errors:
            gui_logger.logger.warning(f"Última configuração ignorada (inválida): {path}")
            return
        if data is None:
            gui_logger.logger.warning(f"Última configuração ignorada (falha ao carregar): {path}")
            return
        self._set_current_config(path, data)
        self.apply_config(data)
        gui_logger.logger.info(f"Configuração carregada automaticamente: {path}")

    def _show_temp_status(self, message, ms):
        """Mostra `message` no rótulo de status por `ms` milissegundos e restaura o texto anterior."""
        previous = self.ctx.status_text.get()
        self.ctx.status_text.set(message)
        self.after(ms, lambda: self.ctx.status_text.set(previous))

    def apply_config(self, data: dict):
        """Aplica os valores da configuração aos campos da janela principal e ao contexto.

        Cada campo é tratado individualmente; campos ausentes na janela são ignorados.
        """
        conn = self.main_frame.connection_frame
        files = self.main_frame.files_card

        # MAC do BITalino
        try:
            mac = str(data.get("bitalino_mac", "")).strip()
            if mac:
                conn.mac_addr_var.set(mac)
                self.ctx.mac_addr = mac
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (MAC): {e}")

        # Canal ativo (A1–A6): grava "A{n}" no optionmenu e o índice no contexto
        try:
            channel = str(data.get("bitalino_channel", "")).strip().upper()
            if channel.startswith("A") and channel[1:].isdigit():
                n = int(channel[1:])
                conn.canal_var.set(f"A{n}")
                self.ctx.signal_channel = n
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (canal): {e}")

        # Pasta de músicas
        try:
            music = str(data.get("music_folder", "")).strip()
            if music:
                files.music_file_folder_var.set(music)
                self.ctx.music_folder = music
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (pasta de músicas): {e}")

        # Arquivo de fatores -> campo de condições
        try:
            factors = str(data.get("factors_file", "")).strip()
            if factors:
                files.conditions_file_var.set(factors)
                self.ctx.conditions_file = factors
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (fatores): {e}")

        # Pasta de salvamento dos dados
        try:
            save_dir = str(data.get("data_save_path", "")).strip()
            if save_dir:
                files.salvar_arquivos_var.set(save_dir)
                self.ctx.save_dir = save_dir
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (pasta de salvamento): {e}")

        # atualiza os checks dos arquivos e o stepper após aplicar a config
        try:
            files._refresh_checks()
        except Exception as e:
            gui_logger.logger.warning(f"apply_config (refresh checks): {e}")
        self.ctx.notify_stepper()


class MainFrame(ctk.CTkFrame):
    """Contêiner do redesign: pilha vertical de seções + rodapé fixo.

    `content` reúne conexão, stepper, cartões, player e o espaço do gráfico;
    o rodapé (`DownFrame`) fica preso embaixo.
    """

    def __init__(self, master, ctx):
        super().__init__(master, fg_color=WIN_BG, corner_radius=0)
        gui_logger.logger.info("MainFrame iniciado.")

        self.ctx = ctx

        content = ctk.CTkFrame(self, fg_color=WIN_BG)
        content.pack(fill="both", expand=True, padx=22, pady=(18, 0))

        self.connection_frame = ConnectionFrame(content, ctx)
        self.connection_frame.pack(fill="x", pady=(0, 16))

        self.stepper_frame = StepperFrame(content, ctx)
        self.stepper_frame.pack(fill="x", pady=(0, 16))

        cards = ctk.CTkFrame(content, fg_color=TRANSPARENTE)
        cards.pack(fill="x", pady=(0, 16))
        cards.grid_columnconfigure(0, weight=2, uniform="c")
        cards.grid_columnconfigure(1, weight=3, uniform="c")

        self.participant_card = ParticipantCard(cards, ctx)
        self.participant_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        self.files_card = FilesCard(cards, ctx)
        self.files_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

        self.player_bar = PlayerBar(content, ctx)
        self.player_bar.pack(fill="x", pady=(0, 16))

        self.graph = GraphPlaceholder(content, ctx)
        self.graph.pack(fill="x", pady=(0, 16))

        # rodapé preso embaixo (criado antes do content para reservar o espaço inferior)
        self.down_frame = DownFrame(self, ctx)
        self.down_frame.pack(fill="x", side="bottom") 

        self.after(100, self.files_card.check_music_file_infos)

if __name__ == "__main__":
    app = Compasso()
    app.mainloop()
