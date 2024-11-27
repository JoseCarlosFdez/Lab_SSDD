#!/usr/bin/env python3
import sys
import Ice
from remotetypes import RemoteTypes as rt


def main():
    with Ice.initialize(sys.argv) as communicator:
        # Configuración del proxy de la factoría desde la información del servidor
        factory_proxy = communicator.stringToProxy(
            "factory -t -e 1.1:tcp -h 172.19.171.124 -p 10000 -t 60000:tcp -h 172.17.0.1 -p 10000 -t 60000:tcp -h 172.18.0.1 -p 10000 -t 60000"        )
        
        # Intentamos conectar con la factoría remota
        factory = rt.FactoryPrx.checkedCast(factory_proxy)
        if not factory:
            raise RuntimeError("No se pudo conectar al proxy de la Factory.")
        
        print("Conectado al servidor remoto.")
        
        # Crear identificadores para cada tipo
        rdict_id = "test_dict"
        rlist_id = "test_list"
        rset_id = "test_set"
        
        
        # Prueba de RDict
        rdict = factory.get(rt.TypeName.RDict, rdict_id)
        print("factory")
        rdict = rt.RDictPrx.checkedCast(rdict)
        
        rdict.setItem("clave1", "valor1")
        print(f"Obtenido valor de 'clave1': {rdict.getItem('clave1')}")
        print(f"¿Contiene 'clave1'? {rdict.contains('clave1')}")
        rdict.remove("clave1")
        print(f"¿Contiene 'clave1' tras eliminar? {rdict.contains('clave1')}")
        
        # Prueba de RList
        rlist = factory.get(rt.TypeName.RList, rlist_id)
        rlist = rt.RSetPrx.checkedCast(rlist)
        
        rlist.append("elemento1")
        rlist.append("elemento2")
        print(f"Longitud de RList: {rlist.length()}")
        print(f"Obtenido elemento en índice 0: {rlist.getItem(0)}")
        print(f"Elemento eliminado: {rlist.pop()}")
        print(f"Longitud tras pop: {rlist.length()}")
        
        # Prueba de RSet
        rset = factory.get(rt.TypeName.RSet, rset_id)
        rset = rt.RSetPrx.checkedCast(rset)
        
        rset.add("valor1")
        rset.add("valor2")
        print(f"¿Contiene 'valor1'? {rset.contains('valor1')}")
        print(f"Hash del RSet: {rset.hash()}")
        print(f"Elemento eliminado: {rset.pop()}")
        print(f"Longitud de RSet tras pop: {rset.length()}")
        
        print("\nPruebas finalizadas con éxito.")


if __name__ == "__main__":
    main()
