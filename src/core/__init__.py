from src.utils import SetLogger

connection_logger = SetLogger(logfilepath=r'logs\connections.log', namelogger='connectionLogger')
player_logger = SetLogger(logfilepath=r'logs\player.log', namelogger='playerLogger')

from .bitalino_connect import connectar_bitalino, run_scan_devices

__all__ = [
    'connection_logger',
    'player_logger',
    'connectar_bitalino',
    'run_scan_devices'
]