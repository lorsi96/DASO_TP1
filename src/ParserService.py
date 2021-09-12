import json
import logging
import argparse

from threading import Timer
from currencylib.moneda import Moneda
from currencylib.cliente import Cliente, ClienteUdp, ServerUnavailableError 

class ParserService():
    CSV_SKIP_HEADER = 1  # From where to start reading data from the .csv

    def __init__(self, report_period_s=30., cfgpath='./files/config.txt', cliente:Cliente=ClienteUdp()) -> None:
        self._currencies = []
        self._client = cliente
        self._period = report_period_s
        self._timer = Timer(self._period, self.__timer_cb)

        try:
            with open(cfgpath, 'r') as f:
                self._data_path = f.read()
                logging.debug(f'Archivo de configuración encontrado, el csv está en: ({self._data_path})')
        except FileNotFoundError:
            raise FileNotFoundError(f'Archivo de configuración no encontrado en "{cfgpath})"')
    
    def start(self):
        logging.info(f'Inicializando comunicación con servidor')
        self.__timer_cb()

    def stop(self):
        logging.debug(f'Finalizando comunicación con servidor')
        self._timer.cancel()
        self._client.close()

    def _read_currencies(self):
        try:
            with open(self._data_path, 'r') as f:
                currencies_str_lines = f.readlines()[self.CSV_SKIP_HEADER:]
                self._currencies = [Moneda.from_csv_entry(e) for e in currencies_str_lines]
        except FileNotFoundError:
            raise FileNotFoundError(f'CSV de tipos de cambio no encontrado en "{self._data_path})"')
        except ValueError:
            raise ValueError('Error al parsear monedas')
    
    def _serialize_currencies_json(self):
        try:
            return json.dumps([moneda.as_dict() for moneda in self._currencies])
        except Exception:
            raise ValueError('Error al convertir monedas en .json')
    
    def _send_currencies(self):
        logging.debug(f'Enviando tipos de cambio al servidor')
        try:
            self._client.send(self._serialize_currencies_json())
        except ServerUnavailableError:
            logging.warning('El servidor no está disponible')

    def __timer_cb(self): 
        # Read and send currencies.
        self._read_currencies()
        self._send_currencies()
        
        # Reset timer.
        self._timer = Timer(self._period, self.__timer_cb)
        self._timer.start()
        
# ******************************************************************************************************************** #
#                                                  Command Line Parser                                                 #
# ******************************************************************************************************************** #
def get_args():
    parser = argparse.ArgumentParser(description='Envía tipos de cambio por UDP en formato JSON')
    parser.add_argument('--config', default='./files/config.txt',
                    help='Directorio de un arhivo .txt con el path del archivo .csv con los tipos de cambio')
    
    parser.add_argument('--port', default=8081, type=int,
                    help='Puerto en Localhost del servidor')
    
    parser.add_argument('--period', default=30, type=int,
                    help='Tiempo en segundos entre cada refresco de datos (lectura del archivo de tipos de cambio)')
    return parser.parse_args()


# ******************************************************************************************************************** #
#                                                      Application                                                     #
# ******************************************************************************************************************** #

if __name__ == '__main__':
    # Parse Service Application.

    ## Logging Settings.
    logging.basicConfig(
        format='(%(levelname)s) %(asctime)s: %(message)s', 
        level = logging.DEBUG
    )

    ## CMD Line Arguments Parsing
    args = get_args()

    ## Main Application
    print(' ***********************************\n',
          '* Presione <Enter> para finalizar *\n',
          '***********************************\n')

    cliente = ClienteUdp(port=args.port)    
    ps = ParserService(args.period, cfgpath=args.config, cliente=cliente)
    try:
        ps.start()
        input('')
    except KeyboardInterrupt as e:
        logging.info('Terminando el programa por interrupción de teclado')
    except Exception as e:
        logging.error('Terminando el programa por un error inesperado')
    else:
        logging.info('Terminando programa normalmente')
    finally:
        ps.stop()
        logging.info('La aplicación ha finalizado correctamente')
    


