from src.utils import SetLogger

gui_logger = SetLogger(logfilepath=r'logs\gui.log', namelogger='guiLogger')

from .gui_configs import set_window_grid, set_window_configs, set_grids
from .main import Compasso

__all__ = [
    'gui_logger',
    'set_window_grid',
    'set_window_configs',
    'set_grids',
    'Compasso'
]