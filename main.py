from math import cos, sin

import numpy as np
import time

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from grid import Grid


class MetaBall:
    def __init__(self, radius=3.):
        self.position = np.empty(3, dtype=np.float)
        self.position[0] = 0.0
        self.position[1] = 0.0
        self.position[2] = 0.0
        self.radius = radius


def load_shader(path, shader_type, program):
    with open(path) as file:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, file.read())
        glCompileShader(shader)
        glAttachShader(program, shader)


def display():
    update()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0.0, 0.0, -45.0)
    grid.draw()

    glutSwapBuffers()


def reshape(w, h):
    global width, height
    width, height = w, h

    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(100., width / height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def update():
    balls[0].position[0] = 20.0 * cos(time.time() / 1)
    balls[1].position[0] = -20.0 * cos(time.time() / 1)
    balls[2].position[0] = 20.0 * sin(time.time() / 1)
    balls[2].position[1] = 20.0 * sin(time.time() / 1)

    for vertex in grid.vertexes:
        vertex.value = 0.0

    for ball in balls:
        for vertex in grid.vertexes:
            point[0] = vertex.position[0] - ball.position[0]
            point[1] = vertex.position[1] - ball.position[1]
            point[2] = vertex.position[2] - ball.position[2]

            dist = point[0] * point[0] + point[1] * point[1] + point[2] * point[2]
            if dist == 0.:
                dist = 0.000001

            scale = ball.radius / dist
            vertex.value += scale

    glutPostRedisplay()


width = 800
height = 800
grid = Grid()
balls = [MetaBall(4), MetaBall(2), MetaBall(3)]
point = np.empty(3, np.float)

glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutCreateWindow(b"Bakhvalov Pavel - HW3 Metaballs + marching cubes")

reshape(width, height)

program = glCreateProgram()
load_shader("vertex.glsl", GL_VERTEX_SHADER, program)
load_shader("fragment.glsl", GL_FRAGMENT_SHADER, program)
glLinkProgram(program)
glUseProgram(program)

glEnable(GL_DEPTH_TEST)
glEnable(GL_NORMALIZE)

glutDisplayFunc(display)
glutReshapeFunc(reshape)

glutMainLoop()
