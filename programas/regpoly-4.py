str_numero_de_lados=input("Introduzca el número de lados del polígono: ")
numero_de_lados=int(str_numero_de_lados)
str_longitud_del_lado=input("Introduzca la longitud del lado: ")
longitud_del_lado=int(str_longitud_del_lado)
angulo=180-((numero_de_lados-2)*180/numero_de_lados)

def hacer_lado(t):
    t.forward(longitud_del_lado)
    t.left(angulo)

def hacer_poligono(y):
    for n in range (numero_de_lados):
        hacer_lado(y)


import turtle
wnd = turtle.Screen()
alex = turtle.Turtle()
john = turtle.Turtle()
joey = turtle.Turtle()
luca = turtle.Turtle()
alex.color("green")
john.color("red")
joey.color("blue")
luca.color("purple")

for turtle in (alex,john,joey,luca):
    turtle.up()

alex.goto(100,100)
john.goto(-200,100)
joey.goto(100,-200)
luca.goto(-200,-200)

for turtle in (alex,john,joey,luca):
    turtle.down()

for turtle in (alex,john,joey,luca):
    hacer_poligono(turtle)

wnd.exitonclick()
