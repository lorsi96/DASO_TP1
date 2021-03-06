import unittest
import tempfile

from unittest.mock import create_autospec
from ParserService import ParserService
from currencylib.cliente import Cliente
from currencylib.moneda import Moneda

TEST_MONEDAS = '''id,nombre,compra,venta
1,Dolar,58.63,61.61
2,Euro,65.12,68.93
3,Real,13.45,14.23'''

class TestParserService(unittest.TestCase):

    def setUp(self) -> None:
        self.client = create_autospec(Cliente)
        self.cfgfile = tempfile.NamedTemporaryFile()
        self.cambiosfile = tempfile.NamedTemporaryFile()
        self.cambiosfile.write(TEST_MONEDAS.encode())
        self.cambiosfile.seek(0)
        self.cfgfile.write(self.cambiosfile.name.encode())
        self.cfgfile.seek(0)
        self.parser_service = ParserService(0., self.cfgfile.name, self.client)
    

    def test_read_currencies(self):
        MONEDAS_ESPERADAS = (
            Moneda(1, 'Dolar', 58.63, 61.61),
            Moneda(2, 'Euro', 65.12, 68.93),
            Moneda(3, 'Real', 13.45, 14.23)
        )
        
        self.parser_service._read_currencies()
        for i, moneda in enumerate(self.parser_service._currencies):
            self.assertEqual(MONEDAS_ESPERADAS[i], moneda)

    def test_serialize_currencies_json(self):
        JSON_ESPERADO = '''[{"id": 1, "value1": 58.63, "value2": 61.61, "name": "Dolar"}, {"id": 2, "value1": 65.12, "value2": 68.93, "name": "Euro"}, {"id": 3, "value1": 13.45, "value2": 14.23, "name": "Real"}]'''
        self.parser_service._read_currencies()
        res = self.parser_service._serialize_currencies_json()
        self.assertEqual(JSON_ESPERADO, res)

    def tearDown(self) -> None:
        self.cfgfile.close()
        self.cambiosfile.close()

   


if __name__ == '__main__':
    unittest.main()