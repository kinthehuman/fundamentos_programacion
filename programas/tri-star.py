puntas=13
angulo=180/puntas
lado=200

import turtle
wnd=turtle.Screen()
alex=turtle.Turtle()

for n in range(puntas):
    alex.forward(lado)
    alex.right(180-angulo)

wnd.exitonclick()
