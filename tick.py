import pygame
import sys
import math

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (231, 76, 60)
AZUL = (52, 152, 219)
GRIS = (189, 195, 199)
VERDE = (46, 204, 113)
FONDO = (236, 240, 241)

ANCHO = 600
ALTO = 600
LINE_WIDTH = 15

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("3 en Raya")

BLOCK_SIZE = ANCHO // 3

fuente = pygame.font.Font(None, 50)

fondo_img = pygame.image.load("fondo_textura.jpg")
fondo_img = pygame.transform.scale(fondo_img, (ANCHO, ALTO))

def dibujar_tablero():
    pantalla.blit(fondo_img, (0, 0))
    for x in range(1, 3):
        pygame.draw.line(pantalla, GRIS, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, ALTO), LINE_WIDTH)
        pygame.draw.line(pantalla, GRIS, (0, x * BLOCK_SIZE), (ANCHO, x * BLOCK_SIZE), LINE_WIDTH)

def dibujar_x(row, col):
    offset = 50
    start_x = col * BLOCK_SIZE + offset
    start_y = row * BLOCK_SIZE + offset
    end_x = col * BLOCK_SIZE + BLOCK_SIZE - offset
    end_y = row * BLOCK_SIZE + BLOCK_SIZE - offset
    pygame.draw.line(pantalla, ROJO, (start_x, start_y), (end_x, end_y), LINE_WIDTH)
    pygame.draw.line(pantalla, ROJO, (start_x, end_y), (end_x, start_y), LINE_WIDTH)

def dibujar_o(row, col):
    offset = 50
    center_x = col * BLOCK_SIZE + BLOCK_SIZE // 2
    center_y = row * BLOCK_SIZE + BLOCK_SIZE // 2
    radius = BLOCK_SIZE // 3
    pygame.draw.circle(pantalla, AZUL, (center_x, center_y), radius, LINE_WIDTH)

def verificar_ganador(tablero):
    for row in range(3):
        if tablero[row][0] == tablero[row][1] == tablero[row][2] and tablero[row][0] is not None:
            return tablero[row][0]
    for col in range(3):
        if tablero[0][col] == tablero[1][col] == tablero[2][col] and tablero[0][col] is not None:
            return tablero[0][col]
    if tablero[0][0] == tablero[1][1] == tablero[2][2] and tablero[0][0] is not None:
        return tablero[0][0]
    if tablero[0][2] == tablero[1][1] == tablero[2][0] and tablero[0][2] is not None:
        return tablero[0][2]
    return None

def verificar_empate(tablero):
    for row in range(3):
        for col in range(3):
            if tablero[row][col] is None:
                return False
    return True

def minimax(tablero, es_maximizador):
    ganador = verificar_ganador(tablero)
    if ganador == "O":
        return 1
    elif ganador == "X":
        return -1
    elif verificar_empate(tablero):
        return 0
    if es_maximizador:
        mejor_puntuacion = -math.inf
        for row in range(3):
            for col in range(3):
                if tablero[row][col] is None:
                    tablero[row][col] = "O"
                    puntuacion = minimax(tablero, False)
                    tablero[row][col] = None
                    mejor_puntuacion = max(puntuacion, mejor_puntuacion)
        return mejor_puntuacion
    else:
        peor_puntuacion = math.inf
        for row in range(3):
            for col in range(3):
                if tablero[row][col] is None:
                    tablero[row][col] = "X"
                    puntuacion = minimax(tablero, True)
                    tablero[row][col] = None
                    peor_puntuacion = min(puntuacion, peor_puntuacion)
        return peor_puntuacion

def mejor_movimiento(tablero):
    mejor_puntuacion = -math.inf
    movimiento = None
    for row in range(3):
        for col in range(3):
            if tablero[row][col] is None:
                tablero[row][col] = "O"
                puntuacion = minimax(tablero, False)
                tablero[row][col] = None
                if puntuacion > mejor_puntuacion:
                    mejor_puntuacion = puntuacion
                    movimiento = (row, col)
    return movimiento

def mostrar_mensaje(texto):
    mensaje = fuente.render(texto, True, VERDE)
    pantalla.blit(mensaje, (ANCHO // 4, ALTO // 2 - 50))
    pygame.display.update()
    pygame.time.delay(2000)

def reiniciar_tablero():
    return [[None, None, None], [None, None, None], [None, None, None]]

jugando = True
tablero = reiniciar_tablero()
dibujar_tablero()
jugador = "X"

while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False
        if event.type == pygame.MOUSEBUTTONDOWN and jugador == "X":
            x, y = pygame.mouse.get_pos()
            row = y // BLOCK_SIZE
            col = x // BLOCK_SIZE
            if tablero[row][col] is None:
                tablero[row][col] = "X"
                dibujar_x(row, col)
                ganador = verificar_ganador(tablero)
                if ganador:
                    mostrar_mensaje(f"{ganador} gana!")
                    tablero = reiniciar_tablero()
                    dibujar_tablero()
                    jugador = "X"
                elif verificar_empate(tablero):
                    mostrar_mensaje("Empate!")
                    tablero = reiniciar_tablero()
                    dibujar_tablero()
                    jugador = "X"
                else:
                    jugador = "O"

    if jugador == "O" and jugando:
        pygame.time.delay(500)
        movimiento = mejor_movimiento(tablero)
        tablero[movimiento[0]][movimiento[1]] = "O"
        dibujar_o(movimiento[0], movimiento[1])
        ganador = verificar_ganador(tablero)
        if ganador:
            mostrar_mensaje(f"{ganador} gana!")
            tablero = reiniciar_tablero()
            dibujar_tablero()
            jugador = "X"
        elif verificar_empate(tablero):
            mostrar_mensaje("Empate!")
            tablero = reiniciar_tablero()
            dibujar_tablero()
            jugador = "X"
        else:
            jugador = "X"

    pygame.display.update()

pygame.quit()
sys.exit()
