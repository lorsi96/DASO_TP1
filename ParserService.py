import json
import logging
import argparse

from threading import Timer
from Moneda import Moneda
from Cliente import Cliente, ClienteUdp, ServerUnavailableError 

class ParserService():
    DATA_START_IND = 1

    def __init__(self, report_period_s=30., cfgpath='./files/config.txt', cliente:Cliente=ClienteUdp()) -> None:
        self._monedas = []
        self._cliente = cliente
        self._period = report_period_s
        self.timer = Timer(self._period, self.__timer_cb)

        try:
            with open(cfgpath, 'r') as f:
                self._data_path = f.read()
                logging.debug(f'Archivo de configuración encontrado: ({self._data_path})')
        except FileNotFoundError:
            raise FileNotFoundError(f'Archivo de configuración no encontrado en "{cfgpath})"')
    
    def start(self):
        logging.info(f'Inicializando comunicación con servidor')
        self.__timer_cb()

    def stop(self):
        logging.debug(f'Finalizando comunicación con servidor')
        self.timer.cancel()
        self._cliente.close()

    def _leer_monedas(self):
        try:
            with open(self._data_path, 'r') as f:
                lineas_monedas = f.readlines()[self.DATA_START_IND:]
                self._monedas = [Moneda.from_csv_entry(e) for e in lineas_monedas]
        except FileNotFoundError:
            raise FileNotFoundError(f'CSV de tipos de cambio no encontrado en "{self._data_path})"')
        except ValueError:
            raise ValueError('Error al parsear monedas')
    
    def _serializar_monedas_json(self):
        try:
            return json.dumps([moneda.as_dict() for moneda in self._monedas])
        except Exception:
            raise ValueError('Error al convertir monedas en .json')
    
    def _enviar_monedas(self):
        logging.debug(f'Envíando tipos de cambio al servidor')
        try:
            self._cliente.send(self._serializar_monedas_json())
        except ServerUnavailableError:
            logging.warning('El servidor no está disponible')

    def __timer_cb(self):
        self._leer_monedas()
        self._enviar_monedas()
        self.timer.cancel()
        self.timer = Timer(self._period, self.__timer_cb)
        self.timer.start()
        
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
    


