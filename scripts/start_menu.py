from scripts.game_state import *
from scripts.button_object import *

class StartMenu(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.title = TextObject((self.game.screen_width / 2, 200), None, 128, (255, 255, 255))
        self.start_button = ButtonObject((self.game.screen_width / 2, 360), (400, 100), 'Start', None, 64, hover_color=(215, 255, 215))
        self.controls_button = ButtonObject((self.game.screen_width / 2, 520), (400, 100), 'Controls', None, 64, hover_color=(215, 255, 215))

        self.start_button.color = (90, 255, 150)
        self.controls_button.color = (90, 255, 150)

        self.title.write('Rhythm Game')

    def update(self, delta_time):
        self.start_button.update(self.game.mouse_pos)
        self.controls_button.update(self.game.mouse_pos)

        if self.start_button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.game.current_state = self.game.song_picker
        if self.controls_button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.game.current_state = self.game.controls_menu

    def render(self, screen):
        screen.fill((30, 210, 140))

        self.title.render(screen)
        self.start_button.render(screen)
        self.controls_button.render(screen)