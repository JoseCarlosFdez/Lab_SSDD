import unittest
from remotetypes.remotelist import RemoteList
from remotetypes import RemoteTypes as rt
import os

class TestRemoteList(unittest.TestCase):

    def setUp(self):
        """Inicializa una nueva lista de prueba antes de cada prueba."""
        # Asegúrate de que el archivo de persistencia esté limpio
        if os.path.exists("test_rlist.json"):
            os.remove("test_rlist.json")

        self.rlist = RemoteList("test_list", "test_rlist.json")
        self.rlist.append("item1")
        self.rlist.append("item2")
        self.rlist.append("item3")

    def tearDown(self):
        """Limpiar el estado después de cada prueba si es necesario."""
        if os.path.exists("test_rlist.json"):
            os.remove("test_rlist.json")

    # 2.1 - RList.remove borra un elemento por valor
    def test_remove(self):
        self.rlist.remove("item1")
        self.assertEqual(self.rlist.length(), 2)
        self.assertRaises(rt.KeyError, self.rlist.remove, "item1")

    # 2.2 - RList.remove devuelve excepción
    def test_remove_exception(self):
        with self.assertRaises(rt.KeyError):
            self.rlist.remove("nonexistent_item")

    # 2.3 - RList.length devuelve la longitud
    def test_length(self):
        self.assertEqual(self.rlist.length(), 3)
        self.rlist.remove("item1")
        self.assertEqual(self.rlist.length(), 2)

    # 2.4 - RList.contains devuelve False
    def test_contains_false(self):
        self.assertFalse(self.rlist.contains("nonexistent_item"))

    # 2.5 - RList.contains devuelve True
    def test_contains_true(self):
        self.assertTrue(self.rlist.contains("item1"))

    # 2.6 - RList.hash devuelve enteros iguales
    def test_hash_unchanged(self):
        hash1 = self.rlist.hash()
        self.rlist.append("item4")
        hash2 = self.rlist.hash()
        self.assertNotEqual(hash1, hash2)

    # 2.7 - RList.hash devuelve enteros diferentes
    def test_hash_changed(self):
        hash1 = self.rlist.hash()
        self.rlist.remove("item1")
        hash2 = self.rlist.hash()
        self.assertNotEqual(hash1, hash2)

    # 2.8 - RList.append añade un elemento al final
    def test_append(self):
        self.rlist.append("item4")
        self.assertEqual(self.rlist.length(), 4)

    # 2.9.1 - RList.pop devuelve un elemento del final
    def test_pop_last(self):
        item = self.rlist.pop()
        self.assertEqual(item, "item3")
        self.assertEqual(self.rlist.length(), 2)

    # 2.9.2 - RList.pop elimina el elemento del final
    def test_pop_last_removes(self):
        self.rlist.pop()
        self.assertEqual(self.rlist.length(), 2)

    # 2.10.1 - RList.pop devuelve el elemento indicado
    def test_pop_index(self):
        item = self.rlist.pop(0)
        self.assertEqual(item, "item1")
        self.assertEqual(self.rlist.length(), 2)

    # 2.10.2 - RList.pop elimina el elemento indicado
    def test_pop_index_removes(self):
        self.rlist.pop(0)
        self.assertEqual(self.rlist.length(), 2)

    # 2.11 - RList.pop lanza la excepción IndexError
    def test_pop_index_error(self):
        self.assertRaises(rt.KeyError, self.rlist.pop, 10)

    # 2.12.1 - RList.getItem devuelve el elemento indicado
    def test_getItem(self):
        item = self.rlist.getItem(0)
        self.assertEqual(item, "item1")

    # 2.12.2 - RList.getItem mantiene el elemento indicado
    def test_getItem_maintain(self):
        item = self.rlist.getItem(0)
        self.assertEqual(item, "item1")
        self.assertEqual(self.rlist.length(), 3)

    # 2.13 - RList.getItem lanza la excepción IndexError
    def test_getItem_exception(self):
        with self.assertRaises(rt.KeyError):
            self.rlist.getItem(10)

if __name__ == "__main__":
    unittest.main()
