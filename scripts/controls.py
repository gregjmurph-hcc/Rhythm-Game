from scripts.game_state import *
from scripts.button_object import *

class Controls(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.title = TextObject((self.game.screen_width / 2, 160), None, 102, (255, 255, 255))
        self.back_button = ButtonObject((90, 660), (100, 50), 'Back', hover_color=(215, 255, 215))
        self.left_lane_key_bind = ButtonObject((self.game.screen_width / 2 - 260, self.game.screen_height / 2), (120, 100), font_size=48, hover_color=(215, 255, 215))
        self.up_lane_key_bind = ButtonObject((self.game.screen_width / 2 - 130, self.game.screen_height / 2), (120, 100), font_size=48, hover_color=(215, 255, 215))
        self.down_lane_key_bind = ButtonObject((self.game.screen_width / 2, self.game.screen_height / 2), (120, 100), font_size=48, hover_color=(215, 255, 215))
        self.right_lane_key_bind = ButtonObject((self.game.screen_width / 2 + 130, self.game.screen_height / 2), (120, 100), font_size=48, hover_color=(215, 255, 215))
        self.pause_key_bind = ButtonObject((self.game.screen_width / 2 + 260, self.game.screen_height / 2), (120, 100), font_size=48, hover_color=(215, 255, 215))

        self.back_button.color = (90, 255, 150)
        self.left_lane_key_bind.color = (90, 255, 150)
        self.up_lane_key_bind.color = (90, 255, 150)
        self.down_lane_key_bind.color = (90, 255, 150)
        self.right_lane_key_bind.color = (90, 255, 150)
        self.pause_key_bind.color = (90, 255, 150)

        self.title.write('Controls')

        self.rebinding_action = None

    def update(self, delta_time):
        self.left_lane_key_bind.text = f'{self.game.key_names["left_lane"].capitalize()}'
        self.up_lane_key_bind.text = f'{self.game.key_names["up_lane"].capitalize()}'
        self.down_lane_key_bind.text = f'{self.game.key_names["down_lane"].capitalize()}'
        self.right_lane_key_bind.text = f'{self.game.key_names["right_lane"].capitalize()}'
        self.pause_key_bind.text = f'{self.game.key_names["pause"].capitalize()}'

        self.back_button.update(self.game.mouse_pos)
        self.left_lane_key_bind.update(self.game.mouse_pos)
        self.up_lane_key_bind.update(self.game.mouse_pos)
        self.down_lane_key_bind.update(self.game.mouse_pos)
        self.right_lane_key_bind.update(self.game.mouse_pos)
        self.pause_key_bind.update(self.game.mouse_pos)

        if self.back_button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.game.current_state = self.game.start_menu

        if self.left_lane_key_bind.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.rebinding_action = "left_lane"
        if self.up_lane_key_bind.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.rebinding_action = "up_lane"
        if self.down_lane_key_bind.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.rebinding_action = "down_lane"
        if self.right_lane_key_bind.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.rebinding_action = "right_lane"
        if self.pause_key_bind.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.rebinding_action = "pause"

    def render(self, screen):
        screen.fill((30, 210, 140))

        self.title.render(screen)
        self.back_button.render(screen)
        self.left_lane_key_bind.render(screen)
        self.up_lane_key_bind.render(screen)
        self.down_lane_key_bind.render(screen)
        self.right_lane_key_bind.render(screen)
        self.pause_key_bind.render(screen)