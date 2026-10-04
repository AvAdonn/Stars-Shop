import logging
import os
from logging.handlers import RotatingFileHandler
from typing import ClassVar


class ColorFormatter(logging.Formatter):
    COLORS: ClassVar[dict[int, str]] = {
        logging.DEBUG: '\033[94m',
        logging.INFO: '\033[92m',
        logging.WARNING: '\033[93m',
        logging.ERROR: '\033[91m',
        logging.CRITICAL: '\033[1;91m'
    }
    
    RESET = '\033[0m'
    
    def format(self, record):
        color = self.COLORS.get(record.levelno, self.RESET)
        
        format_str = f'{color}%(levelname)-8s{self.RESET} | %(asctime)s | %(name)s:%(lineno)d | %(message)s'
        formatter = logging.Formatter(format_str, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)
    
def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColorFormatter())
    
    file_handler = RotatingFileHandler(
        filename='logs/bot.log',
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    
    file_formatter = logging.Formatter(
        '%(levelname)-8s | %(asctime)s | %(name)s:%(lineno)d | %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger