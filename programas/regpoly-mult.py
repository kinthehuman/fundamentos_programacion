str_longitud_del_lado=input("Introduzca la longitud del lado: ")
longitud_del_lado=int(str_longitud_del_lado)
str_alpha=input("Introduzca un ángulo: ")
alpha=int(str_alpha)
numero_de_lados=360/alpha
angulo=180-((numero_de_lados-2)*180/numero_de_lados)

def hacer_lado(t):
    t.forward(longitud_del_lado)
    t.left(angulo)

def hacer_poligono(y):
    for n in range (int(numero_de_lados)):
        hacer_lado(y)

import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()

for _ in range(int(numero_de_lados)):
    hacer_poligono(alex)
    alex.left(angulo)

wnd.exitonclick()
