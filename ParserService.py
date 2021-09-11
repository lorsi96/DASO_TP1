import json
import logging

from threading import Timer
from Moneda import Moneda
from Cliente import Cliente, ClienteUdp

class ParserService():
    DATA_START_IND = 1

    def __init__(self, report_period_s=30., cfgpath='./files/config.txt', cliente:Cliente=ClienteUdp()) -> None:
        logging.basicConfig(format='(%(levelname)s) %(asctime)s: %(message)s', level = logging.DEBUG)
        self._cliente = cliente
        self._monedas = []
        self._period = report_period_s
        with open(cfgpath, 'r') as f:
            self._data_path = f.read()
        self.timer = Timer(self._period, self.__timer_cb)


    def _leer_monedas(self):
        with open(self._data_path, 'r') as f:
            lineas_monedas = f.readlines()[self.DATA_START_IND:]
            self._monedas = [Moneda.from_csv_entry(e) for e in lineas_monedas]
    
    def _serializar_monedas_json(self):
        return json.dumps([moneda.as_dict() for moneda in self._monedas])
    
    def _enviar_monedas(self):
        self._cliente.send(self._serializar_monedas_json())
    
    def start(self):
        self.__timer_cb()

    def stop(self):
        self.timer.cancel()
        self._cliente.close()
        logging.info('Stopping Application')
    
    def spin(self):
        self._leer_monedas()
        self._enviar_monedas()
    
    def __timer_cb(self):
        self.spin()
        self.timer.cancel()
        self.timer = Timer(self._period, self.__timer_cb)
        self.timer.start()
        

if __name__ == '__main__':

    try:
        ps = ParserService(1.)
        ps.start()
        input('Press Enter To Finish\n')
    except KeyboardInterrupt as e:
        logging.warning('Interrupción por Teclado')
        pass
    finally:
        ps.stop()
    


