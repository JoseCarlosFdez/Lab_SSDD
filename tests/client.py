#!/usr/bin/env python3

import sys
import logging
from typing import List, Optional

import Ice  # noqa: F401; pylint: disable=import-error
import remotetypes


logging.basicConfig(level=logging.INFO)


class Client(Ice.Application):
    def get_factory(self, proxy_str: str) -> remotetypes.RemoteTypes.FactoryPrx:
        """Obtiene la factoría remota a partir del proxy."""
        proxy = self.communicator().stringToProxy(proxy_str)
        factory = remotetypes.RemoteTypes.FactoryPrx.checkedCast(proxy)
        if not factory:
            raise RuntimeError("El proxy proporcionado no es una factoría válida.")
        return factory

    def get_remote_object(
        self,
        factory: remotetypes.RemoteTypes.FactoryPrx,
        obj_type: remotetypes.RemoteTypes.TypeName,
        identifier: Optional[str] = None
    ) -> remotetypes.RemoteTypes.RTypePrx:
        """Obtiene un objeto remoto del tipo solicitado desde la factoría."""
        print(f"[DEBUG] Solicitando objeto remoto: tipo={obj_type}, id={identifier}")
        proxy = factory.get(obj_type, identifier)
        print(f"[DEBUG] Proxy recibido: {proxy}")
        
        if not proxy:
            raise RuntimeError(f"No se obtuvo un proxy válido para {obj_type} con id={identifier}")
        
        obj = None
        if obj_type == remotetypes.RemoteTypes.TypeName.RSet:
            obj = remotetypes.RemoteTypes.RSetPrx.checkedCast(proxy)
            print("[DEBUG] RSet checkedCast:", obj)
        elif obj_type == remotetypes.RemoteTypes.TypeName.RDict:
            obj = remotetypes.RemoteTypes.RDictPrx.checkedCast(proxy)
            print("[DEBUG] RDict checkedCast:", obj)
        elif obj_type == remotetypes.RemoteTypes.TypeName.RList:
            obj = remotetypes.RemoteTypes.RListPrx.checkedCast(proxy)
            print("[DEBUG] RList checkedCast:", obj)

        if not obj:
            raise RuntimeError(f"checkedCast falló para {obj_type} con id={identifier}")
        
        print(f"[DEBUG] Objeto remoto obtenido: {obj}")
        return obj


    def test_rset_requirements(self, rset: remotetypes.RemoteTypes.RSetPrx):
        """Ejecuta las pruebas sobre un RSet remoto."""
        try:
            while rset.length() > 0:
                logging.info("Elementos guardados previamente: %s", rset.pop())

            logging.info("=== INICIO DE PRUEBAS PARA RSet ===")

            # Probar RSet.length (3.3)
            initial_length = rset.length()
            logging.info("Longitud inicial: %d", initial_length)

            # Probar RSet.add (3.8.1, 3.8.2)
            rset.add('item1')
            assert rset.contains("item1"), "Error: item1 no fue añadido (3.8.1)"
            rset.add("item1")
            assert rset.length() == initial_length + 1, "Error: Longitud incorrecta tras añadir duplicado (3.8.2)"

            # Probar RSet.contains (3.4, 3.5)
            assert rset.contains("item1"), "Error: item1 no se detecta como existente (3.5)"
            assert not rset.contains("item2"), "Error: item2 se detecta como existente erróneamente (3.4)"

            # Probar RSet.hash (3.6, 3.7)
            initial_hash = rset.hash()
            rset.add("item2")
            assert rset.hash() != initial_hash, "Error: El hash no cambió tras modificar el RSet (3.7)"

            # Probar RSet.remove (3.1, 3.2)
            rset.remove("item2")
            assert not rset.contains("item2"), "Error: item2 no fue eliminado (3.1)"
            try:
                rset.remove("item3")
            except remotetypes.RemoteTypes.KeyError:
                logging.info("Excepción correcta lanzada al eliminar item inexistente (3.2)")

            # Probar RSet.pop (3.9.1, 3.9.2, 3.10)
            popped_item = rset.pop()
            assert not rset.contains(popped_item), "Error: item no fue eliminado tras pop (3.9.2)"
            while rset.length() > 0:
                rset.pop()
            try:
                rset.pop()
            except remotetypes.RemoteTypes.KeyError:
                logging.info("Excepción correcta lanzada al hacer pop en un RSet vacío (3.10)")

            logging.info("=== INICIO DE PRUEBAS PARA IterableRSet ===")

            rset.add("item1")
            rset.add("item2")
            rset.add("item3")

            # 4.1 `iter` devuelve un objeto de tipo Iterable
            iterable = rset.iter()
            assert isinstance(iterable, remotetypes.RemoteTypes.IterablePrx), "Error: `iter` no devolvió un proxy válido (4.1)"

            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            # 4.2 `next` devuelve el elemento siguiente
            expected_elements = {"item1", "item2", "item3"}
            received_elements = set()

            try:
                while True:
                    element = iterable.next()
                    logging.info("Elemento recibido: %s", element)
                    received_elements.add(element)
            except remotetypes.RemoteTypes.StopIteration:
                logging.info("Excepción correcta lanzada al alcanzar el final del iterador (4.3)")

            assert expected_elements == received_elements, f"Error: los elementos iterados no coinciden con los esperados (4.2), recibidos {received_elements}"

            iterable = rset.iter()
            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            # 4.4 `next` lanza `CancelIteration`
            rset.add("item4")
            try:
                iterable.next()
            except remotetypes.RemoteTypes.CancelIteration:
                logging.info("Excepción correcta lanzada al modificar el objeto iterado (4.4)")

            logging.info("=== FIN DE PRUEBAS PARA IterableRSet ===")

            logging.info("=== FIN DE PRUEBAS PARA RSet ===")
        except AssertionError as e:
            logging.error(f"Prueba fallida: {e}")

    def test_rdict_requirements(self, rdict: remotetypes.RemoteTypes.RDictPrx):
        """Ejecuta las pruebas sobre un RDict remoto."""
        try:
            try:
                keys_to_pop = []
                print("Recopilando claves para eliminar...")
                iterable = rdict.iter()
                print("Iterando...")
                iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)
                print("Casteo correcto...")

                while True:
                    print("Obteniendo siguiente elemento...")
                    key_value = iterable.next()
                    print(f"Elemento recibido: {key_value}")
                    key, _ = key_value.split(":", 1)
                    print(f"Clave: {key}")
                    keys_to_pop.append(key)
                    print(f"Clave añadida a la lista de eliminación: {key}")
            except remotetypes.RemoteTypes.StopIteration:
                logging.info("Fin de iteración para recopilar claves.")

            for key in keys_to_pop:
                print(f"Eliminando clave: {key}")
                value = rdict.pop(key)
                logging.info("Elemento eliminado: %s -> %s", key, value)

            logging.info("=== INICIO DE PRUEBAS PARA RDict ===")

            # 1.3 RDict.length
            initial_length = rdict.length()
            logging.info("Longitud inicial: %d", initial_length)

            # 1.8 RDict.setItem
            rdict.setItem("key1", "value1")
            assert rdict.getItem("key1") == "value1", "Error: No se pudo recuperar el valor establecido (1.8)"
            rdict.setItem("key2", "value2")
            assert rdict.length() == initial_length + 2, "Error: Longitud incorrecta tras agregar elementos (1.3)"

            # 1.10.1 RDict.getItem devuelve el valor
            value = rdict.getItem("key1")
            assert value == "value1", f"Error: Se esperaba 'value1', pero se obtuvo {value} (1.10.1)"

            # 1.10.2 RDict.getItem mantiene el valor
            assert rdict.contains("key1"), "Error: Clave 'key1' debería existir tras getItem (1.10.2)"

            # 1.9 RDict.getItem lanza KeyError
            try:
                rdict.getItem("key3")
            except remotetypes.RemoteTypes.KeyError:
                logging.info("Excepción correcta lanzada al hacer getItem de clave inexistente (1.9)")

            # 1.5 RDict.contains devuelve True
            assert rdict.contains("key1"), "Error: Clave 'key1' no encontrada (1.5)"

            # 1.4 RDict.contains devuelve False
            assert not rdict.contains("key3"), "Error: Clave 'key3' no debería existir (1.4)"

            # 1.6, 1.7 RDict.hash
            initial_hash = rdict.hash()
            rdict.setItem("key3", "value3")
            assert rdict.hash() != initial_hash, "Error: Hash no cambió tras modificar el RDict (1.7)"

            # 1.1 RDict.remove borra un elemento por clave
            rdict.remove("key3")
            assert not rdict.contains("key3"), "Error: Clave 'key3' no fue eliminada correctamente (1.1)"

            # 1.2 RDict.remove lanza excepción KeyError
            try:
                rdict.remove("key3")
            except remotetypes.RemoteTypes.KeyError:
                logging.info("Excepción correcta lanzada al eliminar clave inexistente (1.2)")

            # Probar el Iterable
            logging.info("=== INICIO DE PRUEBAS PARA IterableRDict ===")

            rdict.setItem("key1", "value1")
            rdict.setItem("key2", "value2")
            rdict.setItem("key3", "value3")

            iterable = rdict.iter()
            assert isinstance(iterable, remotetypes.RemoteTypes.IterablePrx), "Error: `iter` no devolvió un proxy válido (4.1)"

            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            expected_items = {"key1": "value1", "key2": "value2", "key3": "value3"}
            received_items = {}

            try:
                while True:
                    item = iterable.next()
                    logging.info("Elemento recibido: %s", item)
                    key, value = item.split(":", 1)
                    received_items[key] = value
            except remotetypes.RemoteTypes.StopIteration:
                logging.info("Excepción correcta lanzada al finalizar la iteración (4.3)")

            assert expected_items == received_items, f"Error: Los elementos iterados no coinciden con los esperados {received_items}"

            iterable = rdict.iter()
            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            # 4.4 Modificación del diccionario durante la iteración
            rdict.setItem("key4", "value4")
            try:
                iterable.next()
            except remotetypes.RemoteTypes.CancelIteration:
                logging.info("Excepción correcta lanzada al modificar el objeto iterado (4.4)")

            logging.info("=== FIN DE PRUEBAS PARA IterableRDict ===")

            logging.info("=== FIN DE PRUEBAS PARA RDict ===")
        except AssertionError as e:
            logging.error(f"Prueba fallida: {e}")

    def test_rlist_requirements(self, rlist: remotetypes.RemoteTypes.RListPrx):
        """Ejecuta las pruebas sobre un RList remoto."""
        try:
            # Eliminar todos los elementos de la lista para iniciar limpio
            while rlist.length() > 0:
                logging.info("Elemento eliminado previamente: %s", rlist.pop())

            logging.info("=== INICIO DE PRUEBAS PARA RList ===")

            # RList.length
            initial_length = rlist.length()
            logging.info("Longitud inicial: %d", initial_length)

            # RList.append
            rlist.append("item1")
            rlist.append("item2")
            assert rlist.length() == initial_length + 2, "Error: Longitud incorrecta tras añadir elementos."

            # RList.getItem
            assert rlist.getItem(0) == "item1", "Error: No se obtuvo el valor esperado en índice 0."
            assert rlist.getItem(1) == "item2", "Error: No se obtuvo el valor esperado en índice 1."

            # RList.remove
            rlist.remove("item1")
            assert rlist.length() == initial_length + 1, "Error: Longitud incorrecta tras eliminar elemento."
            assert rlist.getItem(0) == "item2", "Error: Elemento incorrecto tras eliminar."

            # RList.hash
            initial_hash = rlist.hash()
            rlist.append("item3")
            assert rlist.hash() != initial_hash, "Error: Hash no cambió tras modificar la lista."

            # RList.pop
            popped_item = rlist.pop()
            assert popped_item == "item3", f"Error: Se esperaba 'item3', pero se obtuvo {popped_item}."
            assert rlist.length() == initial_length + 1, "Error: Longitud incorrecta tras pop."

            logging.info("=== INICIO DE PRUEBAS PARA IterableRList ===")

            while rlist.length() > 0:
                rlist.pop()

            rlist.append("element1")
            rlist.append("element2")
            rlist.append("element3")

            # 4.1 `iter` devuelve un objeto de tipo Iterable
            iterable = rlist.iter()
            assert isinstance(iterable, remotetypes.RemoteTypes.IterablePrx), "Error: `iter` no devolvió un proxy válido (4.1)"

            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            # 4.2 `next` devuelve el siguiente elemento
            expected_elements = ["element1", "element2", "element3"]
            received_elements = []

            try:
                while True:
                    element = iterable.next()
                    logging.info("Elemento recibido: %s", element)
                    received_elements.append(element)
            except remotetypes.RemoteTypes.StopIteration:
                logging.info("Excepción correcta lanzada al alcanzar el final del iterador (4.3)")

            assert expected_elements == received_elements, f"Error: los elementos iterados no coinciden con los esperados (4.2), recibidos {received_elements}"

            iterable = rlist.iter()
            iterable = remotetypes.RemoteTypes.IterablePrx.checkedCast(iterable)

            # 4.4 Modificación de la lista durante la iteración
            rlist.append("element4")
            try:
                element = iterable.next()
                logging.info("Elemento recibido: %s", element)
            except remotetypes.RemoteTypes.CancelIteration:
                logging.info("Excepción correcta lanzada al modificar el objeto iterado (4.4)")

            logging.info("=== FIN DE PRUEBAS PARA IterableRList ===")

            logging.info("=== FIN DE PRUEBAS PARA RList ===")
        except AssertionError as e:
            logging.error(f"Prueba fallida: {e}")

    def run(self, argv: List[str]) -> int:
        if len(argv) < 2:
            logging.error("Se requiere un proxy y un identificador opcional")
            return 1

        try:
            proxy_str = argv[1]
            identifier = argv[2] if len(argv) > 2 else None

            factory = self.get_factory(proxy_str)

            rdict = self.get_remote_object(factory, remotetypes.RemoteTypes.TypeName.RDict, identifier)
            self.test_rdict_requirements(rdict)
            print("empezar")

            rset = self.get_remote_object(factory, remotetypes.RemoteTypes.TypeName.RSet, identifier)
            print("medio")
            self.test_rset_requirements(rset)

            rlist = self.get_remote_object(factory, remotetypes.RemoteTypes.TypeName.RList, identifier)
            self.test_rlist_requirements(rlist)

            self.communicator().destroy()
            return 0
        except Exception as e:
            logging.error(f"Error durante la ejecución del cliente: {e}")
            self.communicator().destroy()
            return 1


if __name__ == "__main__":
    client = Client()
    sys.exit(client.main(sys.argv))