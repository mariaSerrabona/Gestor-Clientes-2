import copy
import unittest
import database as db

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Se ejecuta antes de cada prueba
        db.Clientes.lista = [db.Cliente('15J', 'Marta', 'Pérez'),
                            db.Cliente('48H', 'Manolo', 'López'),
                            db.Cliente('28Z', 'Ana', 'García')]

    def test_buscar_cliente(self):
        cliente_existente = db.Clientes.buscar('15J')
        cliente_no_existente = db.Clientes.buscar('99X')
        self.assertIsNotNone(cliente_existente)
        self.assertIsNone(cliente_no_existente)

    def test_crear_cliente(self):
        nuevo_cliente = db.Clientes.crear('39X', 'Héctor', 'Costa')
        self.assertEqual(len(db.Clientes.lista), 4)
        self.assertEqual(nuevo_cliente.dni, '39X')
        self.assertEqual(nuevo_cliente.nombre, 'Héctor')
        self.assertEqual(nuevo_cliente.apellido, 'Costa')
    def test_modificar_cliente(self):
        cliente_a_modificar = copy.copy(db.Clientes.buscar('28Z'))
        cliente_modificado = db.Clientes.modificar('28Z', 'Mariana','Pérez')
        self.assertEqual(cliente_a_modificar.nombre, 'Ana')
        self.assertEqual(cliente_modificado.nombre, 'Mariana')
    def test_borrar_cliente(self):
        cliente_borrado = db.Clientes.borrar('48H')
        cliente_rebuscado = db.Clientes.buscar('48H')
        self.assertNotEqual(cliente_borrado, cliente_rebuscado)

if __name__ == '__main__':
    unittest.main()