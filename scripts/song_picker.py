import os

from scripts.game_state import *
from scripts.button_object import *
from scripts.playing_song import *

class SongPicker(GameState):
    def __init__(self, game):
        super().__init__(game)

        self.title = TextObject((self.game.screen_width / 2, 100), None, 86, (255, 255, 255))
        self.back_button = ButtonObject((90, 660), (100, 50), 'Back', hover_color=(215, 255, 215))

        self.back_button.color = (90, 255, 150)

        self.title.write('Song Picker')

        self.options = []

        start_y = 200
        spacing = 105

        for i, folder in enumerate(self.game.song_folders):

            song_path = os.path.join("assets", "songs", folder)
            chart_path = os.path.join(song_path, "chart.json")
            audio_path = os.path.join(song_path, "audio.wav")

            with open(chart_path, "r") as f:
                chart_data = json.load(f)

            display_name = chart_data.get("name", folder)
            bpm = chart_data["bpm"]

            y = start_y + i * spacing

            button = ButtonObject((self.game.screen_width / 2, y), (600, 80), text=f"{display_name}  |  {bpm} BPM", font_size=36, color=(90, 255, 150), hover_color=(215, 255, 215))

            button.chart_data = chart_data
            button.audio_path = audio_path

            self.options.append(button)
            
    def load_song(self, audio_path, chart_data):
        pygame.mixer.music.load(audio_path)

        self.game.playing_song = PlayingSong(self.game, chart_data, chart_data["bpm"], audio_path)
        self.game.current_state = self.game.playing_song

    def update(self, delta_time):
        self.back_button.update(self.game.mouse_pos)

        if self.back_button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
            self.game.current_state = self.game.start_menu

        for button in self.options:
            button.update(self.game.mouse_pos)

            if button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
                self.load_song(button.audio_path, button.chart_data)

    def render(self, screen):
        screen.fill((30, 210, 140))

        self.title.render(screen)
        self.back_button.render(screen)

        for i in range(len(self.options)):
            self.options[i].render(screen)