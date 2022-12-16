from config import *


def camera_move(x, y):
    return x - WIDTH // 2, y - HEIGHT // 2, x + WIDTH // 2, y + HEIGHT // 2


def edge_handing(x, y, width, height):
    """Останавливает движение камеры при приближении к краю"""
    if x <= WIDTH // 2:
        x_to_array = WIDTH // 2
        x_to_render = x
    elif x >= width - WIDTH // 2:
        x_to_array = width - WIDTH // 2
        x_to_render = x - width + WIDTH
    else:
        x_to_array = x
        x_to_render = WIDTH // 2
    if y <= HEIGHT // 2:
        y_to_array = HEIGHT // 2
        y_to_render = y
    elif y >= height - HEIGHT // 2:
        y_to_array = height - HEIGHT // 2
        y_to_render = y - height + HEIGHT
    else:
        y_to_array = y
        y_to_render = HEIGHT // 2
    return x_to_array, x_to_render, y_to_array, y_to_render
