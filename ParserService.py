from Moneda import Moneda
from Cliente import Cliente, ClienteUdp

from threading import Timer
import json

class ParserService():
    DATA_START_IND = 1

    def __init__(self, report_period_s=1., cfgpath='./files/config.txt', cliente:Cliente=ClienteUdp()) -> None:
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
        self.timer.start()

    def stop(self):
        self.timer.cancel()
        self._cliente.close()
    
    def spin(self):
        self._leer_monedas()
        self._enviar_monedas()
    
    def __timer_cb(self):
        self.spin()
        self.timer.cancel()
        self.timer = Timer(self._period, self.__timer_cb)
        self.timer.start()
        

if __name__ == '__main__':
    ps = ParserService()
    ps.start()
    input('Press Enter To Finish')
    ps.stop()
    


