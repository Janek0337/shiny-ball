class Point:
    def __init__(self, x: float, y: float, z: float, step: float):
        self.x = x
        self.y = y
        self.z = z
        self.step = step

    def move(self, norm_vec: list[int]):
        if len(norm_vec) != 3:
            raise ValueError("Wrong amount of arguments to move")
        self.x += self.step * norm_vec[0]
        self.y += self.step * norm_vec[1]
        self.z += self.step * norm_vec[2]

class sphere(Point):
    def __init__(self, x, y, z, r):
        super().__init__(x, y, z, 0)
        self.r = r