import pygame
import sys
import os
import json

from scripts.text_object import *
from scripts.button_object import *
from scripts.camera import *
from scripts.metronome import *
from scripts.note import *

from scripts.game_state import *
from scripts.start_menu import *
from scripts.song_picker import *
from scripts.playing_song import *
from scripts.controls import *

class Game:
    def __init__(self):
        pygame.init()

        self.screen_width, self.screen_height = 720, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Rhythm Game')

        self.delta_time = 0

        self.song_folders = os.listdir("assets/songs")

        with open("data/controls.json", "r") as f:
            self.controls = json.load(f)

        self.key_bindings = {action: pygame.key.key_code(key_code) for action, key_code in self.controls.items()}
        self.key_names = {action: pygame.key.name(key_name) for action, key_name in self.key_bindings.items()}

        self.start_menu = StartMenu(self)
        self.song_picker = SongPicker(self)
        self.controls_menu = Controls(self)

        self.current_state = self.start_menu

        self.mouse_clicked = False

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            self.mouse_pos = pygame.mouse.get_pos()

            self.current_state.update(self.delta_time)

            self.current_state.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_clicked = False
                if event.type == pygame.KEYDOWN:
                    # Key rebinding in Controls screen
                    if isinstance(self.current_state, Controls):
                        if self.current_state.rebinding_action:
                            action = self.current_state.rebinding_action

                            self.key_bindings[action] = event.key
                            self.controls[action] = pygame.key.name(event.key)
                            self.key_names[action] = pygame.key.name(event.key)

                            with open("data/controls.json", "w") as f:
                                json.dump(self.controls, f, indent=2)

                            self.current_state.rebinding_action = None

                    # Forward all key events to PlayingSong
                    if isinstance(self.current_state, PlayingSong):
                        self.current_state.handle_keydown(event.key)

                if event.type == pygame.KEYUP:
                    if isinstance(self.current_state, PlayingSong):
                        self.current_state.handle_keyup(event.key)

            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000

Game().run()