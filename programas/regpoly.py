str_numero_de_lados=input("Introduzca el número de lados del polígono: ")
numero_de_lados=int(str_numero_de_lados)
str_longitud_del_lado=input("Introduzca la longitud del lado: ")
longitud_del_lado=int(str_longitud_del_lado)
angulo=180-((numero_de_lados-2)*180/numero_de_lados)

def hacer_lado(t):
    t.forward(longitud_del_lado)
    t.left(angulo)

import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()

for n in range (numero_de_lados):
    hacer_lado(alex)

wnd.exitonclick()
