import pygame

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2(0, 0)

    def update(self, speed, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.offset.y -= speed * delta_time
        if keys[pygame.K_s]:
            self.offset.y += speed * delta_time