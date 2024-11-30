# Requisitos específicos por tipos

## Requisitos RDict

| **ID** | **Requisito**                            | **Descripción**                                         | **Estado** |
|--------|------------------------------------------|---------------------------------------------------------|------------|
| 1.1    | RDict.remove borra un elemento por clave | Se borra un elemento existente                          | Hecho      |
| 1.2    | RDict.remove devuelve excepción          | Se lanza KeyError por no existir                        | Hecho      |
| 1.3    | RDict.length devuelve la longitud        | Devuelve la longitud correcta                           | Hecho      |
| 1.4    | RDict.contains devuelve False            | Devuelve False si no está la clave                      | Hecho      |
| 1.5    | RDict.contains devuelve True             | Devuelve True si la clave existe                        | Hecho      |
| 1.6    | RDict.hash devuelve enteros iguales      | Si el RDict no se modifica, devuelve el mismo valor     | Hecho      |
| 1.7    | RDict.hash devuelve enteros diferentes   | Si el RDict se modifica, devuelve valor diferente       | Hecho      |
| 1.8    | RDict.setItem invocado correctamente     | Tras hacer setItem, se puede recuperar dicha clave      | Hecho      |
| 1.9    | RDict.getItem lanza KeyError             | Se lanza la excepción si se hace getItem clave inválida | Hecho      |
| 1.10.1 | RDict.getItem devuelve el valor          | Se devuelve el valor si se hace getItem clave válida    | Hecho      |
| 1.10.2 | RDict.getItem mantiene el valor          | El RDict sigue teniendo la clave y su valor             | Hecho      |
| 1.11   | RDict.pop lanza KeyError                 | Se lanza la excepción si se hace pop clave inválida     | Hecho      |
| 1.12.1 | RDict.pop devuelve el valor              | Se devuelve el valor si se hace pop clave válida        | Hecho      |
| 1.12.2 | RDict.pop elimina el valor               | La clave solicitada se elimina del RDict                | Hecho      |

## Requisitos RList

| **ID** | **Requisito**                               | **Descripción**                                     | **Estado** |
|--------|---------------------------------------------|-----------------------------------------------------|------------|
| 2.1    | RList.remove borra un elemento por valor    | Se borra un elemento existente                      | Hecho      |
| 2.2    | RList.remove devuelve excepción             | Se lanza KeyError por no existir                    | Hecho      |
| 2.3    | RList.length devuelve la longitud           | Devuelve la longitud correcta                       | Hecho      |
| 2.4    | RList.contains devuelve False               | Devuelve False si no está el valor                  | Hecho      |
| 2.5    | RList.contains devuelve True                | Devuelve True si el valor existe                    | Hecho      |
| 2.6    | RList.hash devuelve enteros iguales         | Si el RList no se modifica, devuelve el mismo valor | Hecho      |
| 2.7    | RList.hash devuelve enteros diferentes      | Si el RList se modifica, devuelve valor diferente   | Hecho      |
| 2.8    | RList.append añade un elemento al final     | Se añade un elemento al final del RList             | Hecho      |
| 2.9.1  | RList.pop devuelve un elemento del final    | Se devuelve el elemento del final del RList         | Hecho      |
| 2.9.2  | RList.pop elimina el elemento del final     | Se elimina el elemento del final del RList          | Hecho      |
| 2.10.1 | RList.pop devuelve el elemento indicado     | Se devuelve el elemento de la posición indicada     | Hecho      |
| 2.10.2 | RList.pop elimina el elemento indicado      | Se elimina el elemento de la posición indicada      | Hecho      |
| 2.11   | RList.pop lanza la excepción IndexError     | Se lanza la excepción si la posición no existe      | Hecho      |
| 2.12.1 | RList.getItem devuelve el elemento indicado | Se devuelve el elemento de la posición indicada     | Hecho      |
| 2.12.2 | RList.getItem mantiene el elemento indicado | El elemento de la posición indicada se mantiene     | Hecho      |
| 2.13   | RList.getItem lanza la excepcion IndexError | Se lanza la excepción si la posición no existe      | Hecho      |

## Requisitos RSet

| **ID** | **Requisito**                           | **Descripción**                                    | **Estado** |
|--------|-----------------------------------------|----------------------------------------------------|------------|
| 3.1    | RSet.remove borra un elemento por valor | Se borra un elemento existente                     | Hecho      |
| 3.2    | RSet.remove devuelve excepción          | Se lanza KeyError por no existir                   | Hecho      |
| 3.3    | RSet.length devuelve la longitud        | Devuelve la longitud correcta                      | Hecho      |
| 3.4    | RSet.contains devuelve False            | Devuelve False si no está el valor                 | Hecho      |
| 3.5    | RSet.contains devuelve True             | Devuelve True si el valor existe                   | Hecho      |
| 3.6    | RSet.hash devuelve enteros iguales      | Si el RSet no se modifica, devuelve el mismo valor | Hecho      |
| 3.7    | RSet.hash devuelve enteros diferentes   | Si el RSet se modifica, devuelve valor diferente   | Hecho      |
| 3.8.1  | RSet.add añade un elemento              | Se añade un nuevo elemento al RSet                 | Hecho      |
| 3.8.2  | RSet.add no añade un elemento existente | No se añade un elemento si ya estaba añadido       | Hecho      |
| 3.9.1  | RSet.pop devuelve un elemento           | Se devuelve un elemento del RSet                   | Hecho      |
| 3.9.2  | RSet.pop elimina el elemento devuelto   | Se elimina el elemento del RSet                    | Hecho      |
| 3.10   | RSet.pop lanza la excepción KeyError    | Si el RSet está vacío, se lanza la excepción       | Hecho      |

# Requisitos de Iterable, comunes a los tipos

| **ID** | **Requisito**                              | **Descripción**                                 | **Estado** |
|--------|--------------------------------------------|-------------------------------------------------|------------|
| 4.1    | `iter` devuelve un objeto de tipo Iterable | El método devuelve siempre un proxy válido      | Hecho      |
| 4.2    | `next` devuelve el elemento siguiente      | Se devuelve el siguiente elemento               | Hecho      |
| 4.3    | `next` lanza `StopIteration`               | Si se alcanza el final, se lanza la excepción   | Hecho      |
| 4.4    | `next` lanza `CancelIteration`             | Se lanza cuando el objeto iterado es modificado | Hecho      |

# Requisitos factoría

| **ID** | **Requisito**                           | **Descripción**                         | **Estado** |
|--------|-----------------------------------------|-----------------------------------------|------------|
| 5.1    | Factory.get devuelve un RDict           | Crea un RDict nuevo                     | Hecho      |
| 5.2    | Factory.get devuelve un RList           | Crea un RList nuevo                     | Hecho      |
| 5.3    | Factory.get devuelve un RSet            | Crea un RSet  nuevo                     | Hecho      |
| 5.4    | Factory.get devuelve un RDict existente | Devuelve un RDict existente previamente | Hecho      |
| 5.5    | Factory.get devuelve un RList existente | Devuelve un RList existente previamente | Hecho      |
| 5.6    | Factory.get devuelve un RSet existente  | Devuelve un RSet  existente previamente | Hecho      |


