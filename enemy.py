from entity import Entity


class Enemy(Entity):
    def __init__(self,rect,color):
        super().__init__(rect,color)
        self.speed = 1
        self.velx = 0

    def update(self, waypoint_list):
        self.velx = 0

        self.velx += self.speed

        for waypoint in waypoint_list:
            if waypoint.colliderect((self.rect.x + self.velx, self.rect.y, self.rect.width, self.rect.height)):
                self.speed *= -1

        self.rect.x += self.velx