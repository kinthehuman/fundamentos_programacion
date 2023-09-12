import turtle

def drawSquare(t, sz):
    for i in range(4):
        t.forward(sz)
        t.left(90)
def CuadradosConcentricos(t,cuadrados,variacion,lado):
    for n in range(cuadrados):
        drawSquare(t,lado)
        t.up()
        t.right(90)
        t.forward(variacion/2)
        t.left(90)
        t.forward(-variacion/2)
        t.down()
        lado=lado+variacion

wn = turtle.Screen()


alex = turtle.Turtle()
alex.color("blue")
alex.shape("turtle")
alex.pensize(3)
alex.up()
alex.goto(-200,200)
alex.down()
CuadradosConcentricos(alex,10,-20,200)
alex.up()
alex.goto(100,100)
alex.down()
CuadradosConcentricos(alex,10,24,100)

wn.exitonclick()
