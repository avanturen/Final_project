import numpy as np


def camera_move(x, y, pic):
    camera_view = np.zeros((405, 720, 4))
    for i in range(405):
        for j in range(720):
            camera_view[i][j] = pic[x - 360 + i][y - 202 + j]
    return camera_view
