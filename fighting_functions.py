import pygame
import numpy as np
import math
import camera
from config import *
import numpy as np

def enemy_move(x, y, enemy):
    direction=[(x-enemy.x),(y-enemy.y)]
    norm = np.linalg.norm(direction)
    enemy.vx = direction[1]/norm
    enemy.vy = direction[0]/norm