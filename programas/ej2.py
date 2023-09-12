import math
numero_de_lados=int(input("Introduzca el número de lados del círculo: "))
radio=int(input("Introduzca el radio del círculo: "))
lado=math.pi*radio*2/numero_de_lados
angulo=180-((numero_de_lados-2)*180/numero_de_lados)

def hacer_circulo(t):
    for n in range(numero_de_lados):
        t.forward(lado)
        t.left(angulo)

import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()

hacer_circulo(alex)

wnd.exitonclick()
