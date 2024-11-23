import logging
import os
import traceback
import sys
if __name__ == '__main__':
    package_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    sys.path.append(package_dir)
from config import Config

from utils.m_correos import EnviadorDeCorreos
class Logger():

    def __set_logger(self):
        log_directory = Config.rutalog
        log_filename = 'app.log'

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        log_path = os.path.join(log_directory, log_filename)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', "%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(formatter)

        if (logger.hasHandlers()):
            logger.handlers.clear()

        logger.addHandler(file_handler)

        return logger
    @classmethod
    def correolog(cls, level, message):
        try:
            if Config.email_log:
                correo = EnviadorDeCorreos(Config.email['mail'], Config.email['token'])
                msg = f'{level} Error: hubo un error en el servidor {message}'
                correo.enviar_correo(Config.email_log, f"{level} Debug Api", msg)
                correo.desconectar()
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)

    @classmethod
    def add_to_log(cls, level='error', message_or_error=''):
        try:
            logger = cls.__set_logger(cls)

            if isinstance(message_or_error, Exception):
                # Transforma el objeto de error a una cadena de texto
                traceback.print_exc()
                message = traceback.format_exc()
            else:
                message = str(message_or_error)
                print(message)

            if (level == "critical"):
                cls.correolog(level, message)
                logger.critical(message)
                
            elif (level == "debug"):
                logger.debug(message)
            elif (level == "error"):
                cls.correolog(level, message)
                logger.error(message)
                
            elif (level == "info"):
                logger.info(message)
            elif (level == "warn"):
                logger.warn(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)


#ejemplo de uso 
if __name__ == '__main__':

    try:
        resultado = 5/0
    except Exception as e:
        print(e)
        Logger.add_to_log('error', e)


