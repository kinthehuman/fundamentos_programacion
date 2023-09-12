import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()
alex.speed(0)
x=0.5

for n in range(1000):
    alex.forward(x)
    alex.pensize(alex.pensize()+0.01)
    alex.left(10)
    x=x+0.05

wnd.exitonclick()
