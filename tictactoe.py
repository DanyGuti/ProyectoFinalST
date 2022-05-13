"""Tres en raya

Ejercicios

1. Dale a la X y la O un color y un ancho diferentes.
2. ¿Qué sucede cuando alguien toca un lugar ocupado?
3. ¿Cómo detectaría si alguien ha ganado?
4. ¿Cómo podrías crear un jugador de computadora?
"""

"""Importamos las librerias"""
from turtle import update, setup, hideturtle, tracer, onscreenclick, done
from turtle import up, goto, down, circle
from freegames import line


def grid():
    """Dibuja una cuadrícula de tres en raya."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Dibuja el jugador X"""
    line(x+25, y+25, x + 100, y + 100)
    line(x+25, y + 100, x + 100, y+25)


def drawo(x, y):
    """Dibuja el jugador O"""
    up()
    goto(x + 65, y + 20)
    down()
    circle(50)#diametro del circulo


def floor(value):
    """Redondee el valor a la cuadrícula con tamaño cuadrado 133."""
    return ((value + 200) // 133) * 133 - 200


state = {'player': 1}
players = [drawx, drawo]


def tap(x, y):
    """Dibuje X u O en el cuadrado tocado."""
    x = floor(x)
    y = floor(y)
    player = state['player']
    draw = players[player]
    draw(x, y)
    update()
    state['player'] = not player
        
    


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
grid()
update()
onscreenclick(tap)    
done()
