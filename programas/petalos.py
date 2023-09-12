str_petalos=input("Introduzca el número de pétalos: ")
petalos=int(str_petalos)


def hacer_petalo(t):
    t.circle(100,90)
    t.left(90)
    t.circle(100,90)

import turtle
import random
wnd = turtle.Screen()
alex = turtle.Turtle()

for n in range(petalos):
    alex.up()
    alex.goto(200*random.random(),200*random.random())
    alex.down()
    hacer_petalo(alex)

wnd.exitonclick()
