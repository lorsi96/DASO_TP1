
from functools import reduce

class Moneda:
    def __init__(self, id='0', name='?', val_compra=0, val_venta=0) -> None:
        self._id = id
        self._name = name
        self._val_compra = val_compra
        self._val_venta = val_venta

    @classmethod
    def from_csv_entry(cls, val:str):
        try:
            id, name, val_compra ,val_venta = val.split(',')
            return cls(int(id), name, float(val_compra) ,float(val_venta))
        except Exception as e:
            print(e)

    def serialize_csv(self):
        return f'{self._id},{self._name},{self._val_compra},{self._val_venta}'
    
    def as_dict(self):
        return {
            'id':self._id,
            'value1':self._val_compra,
            'value2':self._val_venta,
            'name':self._name,
        }

    def __eq__(self, o: object) -> bool:
        if isinstance(o, Moneda):
            return all((
                self._id == o._id,
                self._name == o._name,
                self._val_compra == o._val_compra,
                self._val_venta == o._val_venta,
            )) 
        else:
            super.__eq__(self, o)
    


