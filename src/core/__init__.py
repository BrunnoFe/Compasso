from src.utils import SetLogger

connection_logger = SetLogger(logfilepath=r'logs\connections.log', namelogger='connectionLogger')

from .bitalino_connect import connectar_bitalino, run_scan_devices

__all__ = [
    'connection_logger',
    'connectar_bitalino',
    'run_scan_devices'
]