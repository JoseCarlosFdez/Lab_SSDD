import unittest
from unittest.mock import MagicMock, create_autospec
from remotetypes.factory import Factory
from remotetypes import RemoteTypes as rt


class TestFactory(unittest.TestCase):
    def setUp(self):
        self.factory = Factory()
        self.mock_current = MagicMock()
        self.mock_current.adapter = MagicMock()

        # Crear un mock que represente un proxy de RTypePrx
        self.proxy_mock = create_autospec(rt.RTypePrx, instance=True)

        # Configurar el mock del adaptador para que devuelva el proxy
        self.mock_current.adapter.addWithUUID.return_value = self.proxy_mock

        # Configurar checkedCast para devolver el proxy mock
        rt.RTypePrx.checkedCast = MagicMock(return_value=self.proxy_mock)

    def test_get_rdict(self):
        """Test Factory.get creates a new RDict."""
        identifier = "rdict_id"
        obj = self.factory.get(rt.TypeName.RDict, identifier, current=self.mock_current)

        self.assertEqual(obj, self.proxy_mock)  # Validación corregida
        self.mock_current.adapter.addWithUUID.assert_called_once()

    def test_get_existing_rdict(self):
        """Test Factory.get returns an existing RDict."""
        identifier = "rdict_existing"
        # Crear el objeto primero
        self.factory.get(rt.TypeName.RDict, identifier, current=self.mock_current)
        # Recuperar el objeto existente
        obj = self.factory.get(rt.TypeName.RDict, identifier, current=self.mock_current)

        self.assertEqual(obj, self.proxy_mock)  # Validación corregida
        self.assertEqual(self.mock_current.adapter.addWithUUID.call_count, 1)


if __name__ == "__main__":
    unittest.main()
