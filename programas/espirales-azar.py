def dibujarEspiral(t,x):
    for n in range(50):
        t.forward(x)
        t.left(25)
        x=x+0.5

import turtle
import random
wnd = turtle.Screen()
alex = turtle.Turtle()
for y in range(random.randrange(3,7)):
    alex.up()
    alex.goto(200*random.random(),200*random.random())
    alex.down()
    dibujarEspiral(alex,5)

wnd.exitonclick()
