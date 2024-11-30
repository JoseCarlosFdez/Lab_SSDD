import unittest
from remotetypes import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict



class TestRemoteDict(unittest.TestCase):
    def setUp(self):
        """Configuración inicial antes de cada prueba."""
        # Crea un nuevo RDict para las pruebas
        self.rdict = RemoteDict("test")
        self.rdict.setItem("key1", "value1")
        self.rdict.setItem("key2", "value2")

    def test_remove(self):
        """Prueba el método remove para borrar un elemento por clave."""
        self.rdict.remove("key1")
        self.assertFalse(self.rdict.contains("key1"))

    def test_remove_throws_exception_for_invalid_key(self):
        """Prueba que remove lanza excepción KeyError cuando la clave no existe."""
        with self.assertRaises(rt.KeyError):
            self.rdict.remove("invalid_key")

    def test_length(self):
        """Prueba el método length para obtener la longitud del diccionario."""
        self.rdict.remove("key1")  # Asegúrate de eliminar alguna clave
        print(f"[DEBUG] Estado del RDict después de eliminar: {self.rdict._data}")
        self.assertEqual(self.rdict.length(), 2)  # Verifica si la longitud es la esperada


    def test_contains_false(self):
        """Prueba que contains devuelve False cuando la clave no está en el diccionario."""
        if self.rdict.contains("key3"):  # Solo elimina si la clave existe
            self.rdict.remove("key3")
        self.assertFalse(self.rdict.contains("key3"))



    def test_contains_true(self):
        """Prueba que contains devuelve True cuando la clave está en el diccionario."""
        self.assertTrue(self.rdict.contains("key1"))

    def test_hash_same_value(self):
        """Prueba que el hash no cambia si no se modifican los datos."""
        hash1 = self.rdict.hash()
        hash2 = self.rdict.hash()
        self.assertEqual(hash1, hash2)

    def test_hash_different_value(self):
        """Prueba que el hash cambia cuando se modifica el diccionario."""
        hash1 = self.rdict.hash()
        self.rdict.setItem("key3", "value3")
        hash2 = self.rdict.hash()
        self.assertNotEqual(hash1, hash2)

    def test_setItem(self):
        """Prueba el método setItem para añadir una clave-valor."""
        self.rdict.setItem("key3", "value3")
        self.assertEqual(self.rdict.getItem("key3"), "value3")

    def test_getItem_throws_exception_for_invalid_key(self):
        """Prueba que getItem lanza KeyError para claves no existentes."""
        with self.assertRaises(rt.KeyError):
            self.rdict.getItem("invalid_key")

    def test_getItem_valid_key(self):
        """Prueba que getItem devuelve el valor correcto para una clave válida."""
        self.assertEqual(self.rdict.getItem("key1"), "value1")

    def test_getItem_keeps_value(self):
        """Prueba que getItem mantiene el valor en el diccionario."""
        self.rdict.getItem("key1")
        self.assertTrue(self.rdict.contains("key1"))

    def test_pop_throws_exception_for_invalid_key(self):
        """Prueba que pop lanza KeyError si la clave no existe."""
        with self.assertRaises(rt.KeyError):
            self.rdict.pop("invalid_key")

    def test_pop_valid_key(self):
        """Prueba que pop devuelve el valor correcto y elimina la clave."""
        value = self.rdict.pop("key1")
        self.assertEqual(value, "value1")
        self.assertFalse(self.rdict.contains("key1"))

    def tearDown(self):
        """Limpieza después de cada prueba."""
        # Aquí podrías hacer la limpieza si es necesario
        pass

if __name__ == "__main__":
    unittest.main()
