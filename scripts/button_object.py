import pygame

from scripts.text_object import *

class ButtonObject():
    def __init__(self, pos, size, text='', font_type=None, font_size=32, color='blue', hover_color='yellow', text_color='black'):
        self.pos = pygame.math.Vector2(pos)
        self.rect = pygame.Rect(0, 0, *size)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font_type = font_type
        self.font_size = font_size
        self.rect.center = self.pos

    def is_clicked(self, mouse_pos, mouse_clicked):
        return self.rect.collidepoint(mouse_pos) and mouse_clicked
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
            
    def render(self, screen):
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        
        if self.text:
            text_obj = TextObject((self.pos.x, self.pos.y), self.font_type, self.font_size, self.text_color)
            text_obj.write(self.text)
            text_obj.render(screen)