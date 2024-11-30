import unittest
import os
from remotetypes import RemoteTypes as rt
from remotetypes.remoteset import RemoteSet

class TestRemoteSet(unittest.TestCase):

    def setUp(self):
        """Set up the test environment before each test."""
        self.rset = RemoteSet(identifier="test_set")
        # Limpiar el archivo de persistencia antes de cada prueba
        if os.path.exists(self.rset._persist_file):
            os.remove(self.rset._persist_file)
        self.rset = RemoteSet("test_set")
        self.rset.add("item1")
        self.rset.add("item2")
        self.rset.add("item3")


    def test_length(self):
        """Test that length returns the correct number of items."""
        self.assertEqual(self.rset.length(), 3)
        self.rset.remove("item1")
        self.assertEqual(self.rset.length(), 2)

    def test_contains_false(self):
        """Test that contains returns False if the item is not in the set."""
        self.assertFalse(self.rset.contains("item4"))

    def test_contains_true(self):
        """Test that contains returns True if the item is in the set."""
        self.assertTrue(self.rset.contains("item2"))

    def test_hash_unchanged(self):
        """Test that hash remains the same if the set is not modified."""
        original_hash = self.rset.hash()
        self.assertEqual(self.rset.hash(), original_hash)

    def test_hash_changed(self):
        """Test that hash changes after modifying the set."""
        original_hash = self.rset.hash()
        self.rset.add("item4")
        self.assertNotEqual(self.rset.hash(), original_hash)

    def test_pop_item(self):
        """Test that pop removes and returns an item."""
        item = self.rset.pop()
        self.assertNotIn(item, self.rset._data)
        self.assertEqual(self.rset.length(), 2)

    def test_pop_empty_set(self):
        """Test that pop raises KeyError if the set is empty."""
        self.rset.pop()
        self.rset.pop()
        self.rset.pop()
        with self.assertRaises(rt.KeyError):
            self.rset.pop()  # Debería lanzar KeyError porque el conjunto está vacío

if __name__ == "__main__":
    unittest.main()
