str_numero_de_cuadrados=input("Introduzca el número de cuadrados a dibujar: ")
numero_de_cuadrados=int(str_numero_de_cuadrados)
str_longitud_del_lado=input("Introduzca la longitud del lado: ")
longitud_del_lado=int(str_longitud_del_lado)
str_angulo=input("Introduzca el ángulo entre cuadrados: ")
angulo=int(str_angulo)

def hacer_cuadrado(t):
    for n in range(4):
        t.backward(longitud_del_lado)
        t.left(90)

import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()

for _ in range (numero_de_cuadrados):
    hacer_cuadrado(alex)
    alex.left(angulo)

wnd.exitonclick()
