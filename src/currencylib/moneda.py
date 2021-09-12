
class Moneda:
    '''Representa un tipo de cambio, con su nombre y valores de compraventa'''
    def __init__(self, id='0', name='?', val_compra=0, val_venta=0) -> None:
        self._id = id
        self._name = name
        self._val_compra = val_compra
        self._val_venta = val_venta

    @classmethod
    def from_csv_entry(cls, val:str) -> object:
        '''Construye una instancia de Moneda a partir de valores separados por coma'''
        try:
            id, name, val_compra, val_venta = val.split(',')
            return cls(int(id), name, float(val_compra) ,float(val_venta))
        except ValueError as e:
            raise ValueError('Error al parsear entrada de CSV de moneda: ({})'.format(val.replace("\n", "")))

    def as_dict(self) -> dict:
        '''Obtiene una representación en forma de diccionario de la moneda'''
        return {
            'id':self._id,
            'value1':self._val_compra,
            'value2':self._val_venta,
            'name':self._name,
        }

    def serialize_csv(self):
        '''Serializa la moneda en una entrada separada por comas'''
        return f'{self._id},{self._name},{self._val_compra},{self._val_venta}'

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
    


