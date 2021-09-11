import unittest

from Moneda import Moneda

class TestMoneda(unittest.TestCase):

    def test_to_csv_entry(self):
        self.dut = Moneda(3, 'Patacon', 10.0, 11.2)
        self.assertEqual('3,Patacon,10.0,11.2', self.dut.serialize_csv())
    
    def test_equality(self):
        self.dut = Moneda(3, 'Patacon', 10.0, 11.2)
        self.dut2 = Moneda(3, 'Patacon', 10.0, 11.2)
        self.dut3 = Moneda(3, 'Yen', 10.0, 11.2)

        self.assertTrue(self.dut == self.dut2)
        self.assertFalse(self.dut == self.dut3)
    
    def test_from_csv_entry(self):
        self.ex = Moneda(3, 'Patacon', 10.0, 11.2)
        self.dut = Moneda.from_csv_entry('3,Patacon,10.0,11.2')

        self.assertEqual(self.ex, self.dut)

    def test_to_dict(self):
        self.dut = Moneda(1, 'Dolar', 60, 65)
        self.assertEqual(
            {"id": 1, "value1": 60, "value2": 65, "name": "Dolar"},
            self.dut.as_dict()
        )
    


if __name__ == '__main__':
    unittest.main()