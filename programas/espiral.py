import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()

alex.left(30)
x=250
for n in range(30):
    alex.forward(x)
    alex.left(120)
    x=x-8

wnd.exitonclick()
