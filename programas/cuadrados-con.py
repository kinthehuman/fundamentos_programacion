import turtle

def drawSquare(t, sz):
    t.up()
    t.right(90)
    t.forward(3)
    t.left(90)
    t.forward(-3)
    t.down()
    for i in range(4):
        t.forward(sz)
        t.left(90)

wn = turtle.Screen()


alex = turtle.Turtle()
alex.color("black")
alex.shape("turtle")
alex.pensize(5)
x=10
for n in range(10):
    drawSquare(alex,x)
    x=x+6

wn.exitonclick()
