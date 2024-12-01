import unittest
from remotetypes.iterable import Iterable


class TestIterable(unittest.TestCase):
    """Test cases for the Iterable class."""
    
    def setUp(self):
        """Set up a fresh instance of Iterable for each test."""
        self.data = ["a", "b", "c"]
        self.iterable = Iterable(self.data)

    def test_iter_returns_an_iterable_object(self):
        """Test that iter() returns an object of type Iterable."""
        # Verifica que el objeto devuelto por `iter` sea de tipo Iterable
        iter_obj = iter(self.iterable)
        self.assertIsInstance(iter_obj, Iterable)

    def test_next_returns_next_element(self):
        """Test that next() returns the next element."""
        self.assertEqual(next(self.iterable), "a")


    def test_next_raises_stop_iteration(self):
        """Test that next() raises StopIteration when the end is reached."""
        self.iterable.__next__()
        self.iterable.__next__()
        self.iterable.__next__()
        with self.assertRaises(StopIteration):
            self.iterable.__next__()

    def test_reset_resets_iteration(self):
        """Test that reset() resets the iteration index."""
        self.iterable.__next__()  # "a"
        self.iterable.__next__()  # "b"
        self.iterable.reset()
        self.assertEqual(self.iterable.__next__(), "a")

    def test_update_data_resets_and_updates_version(self):
        """Test that update_data resets the iteration and updates the version."""
        self.iterable.update_data(["x", "y", "z"])
        self.assertEqual(self.iterable.__next__(), "x")
        self.assertEqual(self.iterable.__next__(), "y")
        self.assertEqual(self.iterable.__next__(), "z")
        with self.assertRaises(StopIteration):
            self.iterable.__next__()


if __name__ == "__main__":
    unittest.main()
