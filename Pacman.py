"""Pacman, Juego Clásico de tipo Arcade.

Ejercicios

1. Cambiar el tablero.
2. Cambiar el número de fantasmas.
3. Cambiar posición inicial de los fantasmas.
4. Hacer que los fantasmas vayan o más rápido o más lento.
5. Hacer los fantasmas más inteligentes.
"""
# Librería que importa a floor para poder calcular el punto de la
# izquierda dado un valor, tamaño y offset (desplazamiento total).
# Vector para poder dar dirección y sentido (magnitudes)
from freegames import floor, vector
# Librería random, se importa choice para seleccionar
# Número random de secuencia
from random import choice
# Libería turtle que nos ayuda a manipular objetos
# (para que haya movimientos)
from turtle import Turtle, bgcolor, clear, up, goto, dot
from turtle import update, ontimer, setup, hideturtle, tracer
from turtle import listen, onkey, done

# Estado del score como diccionario
state = {'score': 0}
# Estado del camino por pintar sin pintar
path = Turtle(visible=False)
# Estado del camino por pintar sin pintar
writer = Turtle(visible=False)
# Velocidad
aim = vector(5, 0)
# Posiciones del pacman y de fantasmas
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# fmt (formato de paquete): desactivado
# Tablero de 20x20 (matriz de 20x20)
# Los 1 representan el camino por el cual se pueden desplazar
# tanto los fantasmas como pacman en el tablero: tiles
# Los 0 representan "barreras"
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

# fmt (formato de paquete): activado

# Función que dibuja el tablero utilizando
# coordenadas x y y


def square(x, y):
    """Dibujar el cuadrado utilizando path(x,y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)
    # 20 hacia dirección x
    # 90 grados hacia la izquierda
    # Básicameente se crea el tablero aquí

    path.end_fill()


def offset(point):
    """Regresa la distancia del punto en cada
    casilla."""
    x = (floor(point.x, 20) + 200) / 20
    # Pos inicial x=11
    y = (180 - floor(point.y, 20)) / 20
    # Pos inicial y=13
    index = int(x + y * 20)
    return index
    # 480

# Función que checa si hay tiles
# disponibles para que el fantasma
# pueda moverse


def valid(point):
    """Regresa True si el punto es válido
    dentro de las casillas."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Dibujar mundo usando 'path'."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Mover packman y todos los
    fantasmas."""
    writer.undo()
    writer.write(state['score'])

    clear()

    # Llamar a función valid(point) que valida si
    # si hay espacios disponibles o no, si es igual a 0
    # regresa false y no se mueve, si es 1, regresa true, y
    # el pacman se mueve
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    # Si offset regresa un índice en el que la posición
    # de ese índice en el tablero de 1, se convierte el tablero en esa
    # posición en un 2 y se aumenta al score
    # Se cambian coordenadas y se llama a la función square
    # para actualizar como se pinta el tablero
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)


def change(x, y):
    """Cambiar dirección
    de packman si x,y son
    válidas."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
