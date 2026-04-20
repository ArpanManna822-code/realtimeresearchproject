import random

SHAPES = [

[[1,1,1,1]],

[[1,1],
 [1,1]],

[[0,1,0],
 [1,1,1]],

[[1,0,0],
 [1,1,1]],

[[0,0,1],
 [1,1,1]],

[[1,1,0],
 [0,1,1]],

[[0,1,1],
 [1,1,0]]

]

class Tetromino:

    def __init__(self,color):

        self.shape = random.choice(SHAPES)

        self.x = 4
        self.y = 0.0

        self.color = color


def rotate(shape):

    return [list(row) for row in zip(*shape[::-1])]