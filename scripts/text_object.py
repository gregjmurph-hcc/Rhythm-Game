import pygame

class TextObject:
    def __init__(self, pos, font, size, color, antialias=True):
        self.pos = pygame.Vector2(pos)
        self.font_type = font
        self.font_size = size
        self.font = pygame.font.Font(self.font_type, self.font_size)
        self.color = color
        self.antialias = antialias
        self.rect = ()

    def write(self, text):
        self.text = self.font.render(text, self.antialias, self.color)

    def render(self, screen):
        self.rect = self.text.get_rect(center=(self.pos))
        screen.blit(self.text, self.rect)
