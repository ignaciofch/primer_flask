from queue import Queue
from flask import Flask

def personas(desde: int, hasta: int) -> Queue :
    personas = Queue()
    i: int = desde + 1
    while i <= hasta:
        personas.put(i)
        i += 1
    return personas

def hay_nueva_persona(t) -> bool :
   return (t%4 == 0)

def atiende_caja_1(t) -> bool :
   return (t%10 == 1)

def atiende_caja_2(t) -> bool :
   return (t%4 == 3)

def atiende_caja_3(t) -> bool :
   return (t%4 == 2)

def vuelve_mas_tarde(minuto: int) -> int:
   tres_minutos_mas_tarde: int = minuto + 3
   return tres_minutos_mas_tarde

def hay_persona_perjudicada(esta_persona, t) -> bool :
   res: bool = False
   hay_persona: bool = esta_persona[0]
   minuto_llegada_a_la_fila: int = esta_persona[1]
   if (hay_persona == True) and (minuto_llegada_a_la_fila == t):
      res = True
   return res
   

# El tipo de fila debería ser Queue[int], pero la versión de python del CMS no lo soporta. Usaremos en su lugar simplemente "Queue"
def avanzarFila(fila: Queue, min: int):
  fila_previa: int = fila.qsize()
  ingresa_persona = personas(fila_previa, (fila_previa+2)*min)
  t: int = 0
  esta_persona_perjudicada = [False, 0, 0]
  while not(t == (min + 1)): #si esta por ingresar una persona nueva y una por caja 3, cual entra primero?
     if hay_nueva_persona(t): #prueba ingresa primero persona nueva y luego la persona perjudicada
        fila.put(ingresa_persona.get()) #es siempre una nueva persona?
     if hay_persona_perjudicada(esta_persona_perjudicada, t):
        persona_perjudicada = esta_persona_perjudicada[2]
        fila.put(persona_perjudicada)
        esta_persona_perjudicada[0] = False
     if atiende_caja_1(t):
        if not(fila.empty()):
          fila.get()
     if atiende_caja_2(t):
        if not(fila.empty()):
          fila.get()
     if atiende_caja_3(t):
        if not(fila.empty()):
          persona_perjudicada = fila.get()
          esta_persona_perjudicada[0] = True
          esta_persona_perjudicada[1] = vuelve_mas_tarde(t)
          esta_persona_perjudicada[2] = persona_perjudicada
     t += 1 
  return fila

#if __name__ == '__main__':
#  fila: Queue = Queue()
#  fila_inicial: int = int(input())
#  for numero in range(1, fila_inicial+1):
#    fila.put(numero)
#  min: int = int(input())
#  avanzarFila(fila, min)
#  res = []
#  for i in range(0, fila.qsize()):
#    res.append(fila.get())
#  print(res)


# Caja1: Empieza a atender 10:01, y atiende a una persona cada 10 minutos
# Caja2: Empieza a atender 10:03, atiende a una persona cada 4 minutos
# Caja3: Empieza a atender 10:02, y atiende una persona cada 4 minutos, pero no le resuelve el problema y la persona debe volver a la fila (se va al final y tarda 3 min en llegar. Es decir, la persona que fue atendida 10:02 vuelve a entrar a la fila a las 10:05)
# La fila empieza con las n personas que llegaron antes de que abra el banco. Cuando abre (a las 10), cada 4 minutos llega una nueva persona a la fila (la primera entra a las 10:00)

