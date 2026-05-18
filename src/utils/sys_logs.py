import logging
import time

from src.utils.configs import ENCODING_FORMAT

class SetLogger():
    def __init__(self, namelogger: str, logfilepath: str, level: str = 'DEBUG') -> None:
        """_summary_

        Args:
            logfilepath (str): _description_
            level (str | None, optional): _description_. Defaults to 'DEBUG'.
        """
        if level.upper() not in logging._nameToLevel:
            level = 'DEBUG'
            
        self.logger: logging.Logger = logging.getLogger(namelogger)
        self.logger.setLevel(logging._nameToLevel[level.upper()])
        
        self.logfilepath: str = rf'{logfilepath.split(".")[0]}_{time.strftime(r"%d_%m_%Y_%H_%M_%S", time.localtime())}.log'

        self.logFormat = logging.Formatter(fmt='%(asctime)s:%(filename)s: %(name)s: %(levelname)s: %(funcName)s -> %(message)s')

        self.logFileHandler = logging.FileHandler(self.logfilepath, encoding=ENCODING_FORMAT)
        self.logFileHandler.setFormatter(self.logFormat)

        self.logStremHandler = logging.StreamHandler()
        self.logStremHandler.setFormatter(self.logFormat)

        self.logger.addHandler(self.logFileHandler)
        self.logger.addHandler(self.logStremHandler)
        
        self.logger.info(f'Logger "{namelogger}" iniciado')

#usage example:  
#guilogger: SetLogger = SetLogger(logfilepath=r'logs\EsquizoCapLogs.log', namelogger='guitoolsLogger')