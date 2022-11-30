import numpy as np
from config import *

def camera_move(x, y, pic):
    return pic[x-WIDTH//2: x + WIDTH//2, y - HEIGHT//2: y + HEIGHT//2]