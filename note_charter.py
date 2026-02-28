import pygame
import sys
import json

from scripts.camera import *
from scripts.button_object import *

class NoteCharter:
    def __init__(self):  
        pygame.init()

        self.screen_width, self.screen_height = 400, 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Note Charter')

        self.dt = 0

        self.song = pygame.mixer.Sound('assets/songs/BGM_DUN_MONSTERHOUSE/audio.wav')
        self.song_name = 'BGM_DUN_MONSTERHOUSE'
        self.song_len = pygame.mixer.Sound.get_length(self.song)

        self.bpm = 135
        self.beat_dur = 60 / self.bpm
        self.beat_text_spacing = 50
        self.lanes = 4

        self.beats_in_song = int(self.song_len / self.beat_dur)

        self.tap_notes = set()
        self.hold_notes = []
        self.hold_start = None

        self.tap_note_mode = True
        self.hold_note_mode = False

        self.mouse_clicked = False
        self.camera = Camera()
        self.camera.offset.y = -self.song_len * 100 - 30

        self.tap_note_button = ButtonObject((325, 30), (120, 30), 'Tap Notes', font_size=28, hover_color=(215, 255, 215))
        self.hold_note_button = ButtonObject((325, 90), (120, 30), 'Hold Notes', font_size=28, hover_color=(215, 255, 215))

        self.text_display = pygame.Surface((60, 13.25 * self.beat_text_spacing + self.song_len * 100))
        self.text_display.fill((30, 210, 140))
        self.text_display_rect = self.text_display.get_rect()

        self.bpm_text = TextObject((325, 150), None, 36, (255, 255, 255))
        self.song_name_text = TextObject((200, 688), None, 20, (255, 255, 255))
        self.save_chart_text = TextObject((325, 210), None, 28, (255, 255, 255))
        self.load_chart_text = TextObject((325, 240), None, 28, (255, 255, 255))

        self.bpm_text.write(f'BPM: {self.bpm}')
        self.song_name_text.write(f'{self.song_name}')
        self.save_chart_text.write('Save chart: O')
        self.load_chart_text.write('Load chart: P')

        for i in range(self.beats_in_song):
            y = self.text_display_rect.bottom - 15 - (i * self.beat_text_spacing)
            self.beat_inc_text = TextObject((30, y), None, 32, (255, 255, 255))
            self.beat_inc_text.write(f'{i + 1}')
            self.beat_inc_text.render(self.text_display)

    def get_cell_from_mouse(self, mouse_pos):
        world_y = mouse_pos[1] + self.camera.offset.y + self.song_len * 100

        lane = (mouse_pos[0] - 60) // self.beat_text_spacing
        beat = world_y // self.beat_text_spacing

        if 0 <= lane < self.lanes and 0 <= beat < self.beats_in_song:
            return int(lane), int(beat)

        return None
    
    def get_hold_at(self, lane, beat):
        for hold in self.hold_notes:
            h_lane, start, end = hold
            if h_lane == lane and start <= beat <= end:
                return hold
        return None
    
    def save_chart(self, filename="chart.json"):
        chart_data = {
            "name": self.song_name,
            "bpm": self.bpm,
            "tap_notes": list(self.tap_notes),
            "hold_notes": self.hold_notes
        }

        with open(filename, "w") as f:
            json.dump(chart_data, f, indent=3)

    def load_chart(self, filepath):
        with open(filepath, "r") as f:
            chart_data = json.load(f)
            self.bpm = chart_data["bpm"]
            self.tap_notes = {(lane, beat) for lane, beat in chart_data["tap_notes"]}
            self.hold_notes = [(lane, start, end) for lane, start, end in chart_data["hold_notes"]]

    def run(self):
        while True:
            self.screen.fill((30, 210, 140))
            self.screen.blit(self.text_display, (0, -self.song_len * 100 - self.camera.offset.y))

            mouse_pos = pygame.mouse.get_pos()

            if self.camera.offset.y >= 0:
                self.camera.offset.y = 0
            if self.camera.offset.y <= -self.song_len * 100 - 30:
                self.camera.offset.y = -self.song_len * 100 - 30

            for lane in range(self.lanes):
                for beat in range(self.beats_in_song):
                    x = lane * self.beat_text_spacing + 60
                    y = beat * self.beat_text_spacing - self.camera.offset.y - self.song_len * 100

                    rect = pygame.Rect(x, y, 36, 36)
                    pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, 10)

            for lane, beat in self.tap_notes:
                x = lane * self.beat_text_spacing + 60 + 18
                y = beat * self.beat_text_spacing - self.camera.offset.y - self.song_len * 100 + 18

                pygame.draw.circle(self.screen, (55, 80, 255), (x, y), 12)

            for lane, start, end in self.hold_notes:
                x = lane * self.beat_text_spacing + 60 + 18

                y_start = start * self.beat_text_spacing - self.camera.offset.y - self.song_len * 100
                y_end = end * self.beat_text_spacing - self.camera.offset.y - self.song_len * 100

                height = y_end - y_start

                rect = pygame.Rect(x - 8, y_start + 18, 16, height)
                pygame.draw.rect(self.screen, (220, 75, 25), rect, border_radius=8)

                pygame.draw.circle(self.screen, (220, 75, 25), (x, y_start + 18), 12)
                pygame.draw.circle(self.screen, (220, 75, 25), (x, y_end + 18), 12)

            self.camera.update(1250, self.dt)

            self.tap_note_button.color = (215, 255, 215) if self.tap_note_mode else (90, 255, 150)
            self.hold_note_button.color = (215, 255, 215) if self.hold_note_mode else (90, 255, 150)

            if self.tap_note_button.is_clicked(mouse_pos, self.mouse_clicked) and not self.tap_note_mode:
                self.tap_note_mode = True
                self.hold_note_mode = False
            
            if self.hold_note_button.is_clicked(mouse_pos, self.mouse_clicked) and not self.hold_note_mode:
                self.tap_note_mode = False
                self.hold_note_mode = True

            self.tap_note_button.update(mouse_pos)
            self.hold_note_button.update(mouse_pos)

            self.tap_note_button.render(self.screen)
            self.hold_note_button.render(self.screen)

            pygame.draw.rect(self.screen, (100, 100, 100), (0, 675, self.screen_width, 50))

            self.bpm_text.render(self.screen)
            self.song_name_text.render(self.screen)
            self.save_chart_text.render(self.screen)
            self.load_chart_text.render(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:
                        self.save_chart(f"assets/songs/BGM_DUN_MONSTERHOUSE/chart.json")
                    if event.key == pygame.K_p:
                        self.load_chart(f"assets/songs/BGM_DUN_MONSTERHOUSE/chart.json")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mouse_clicked = True
                        if self.tap_note_mode:
                            cell = self.get_cell_from_mouse(event.pos)
                            if cell:
                                lane, beat = cell
                                self.tap_notes.add((lane, beat))
                        if self.hold_note_mode:
                            cell = self.get_cell_from_mouse(event.pos)
                            if cell:
                                self.hold_start = cell
                    if event.button == 3:
                        cell = self.get_cell_from_mouse(event.pos)
                        if cell:
                            lane, beat = cell
                            if self.tap_notes:
                                self.tap_notes.discard((lane, beat))

                            if self.hold_notes:
                                hold = self.get_hold_at(lane, beat)
                                if hold:
                                    self.hold_notes.remove(hold) 
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_clicked = False
                        if self.hold_note_mode and self.hold_start:
                            cell = self.get_cell_from_mouse(event.pos)
                            if cell:
                                lane_start, beat_start = self.hold_start
                                lane_end, beat_end = cell

                                if lane_start == lane_end:
                                    start = min(beat_start, beat_end)
                                    end = max(beat_start, beat_end)

                                    if start != end:
                                        self.hold_notes.append((lane_start, start, end))

                            self.hold_start = None

            pygame.display.update()
            self.dt = self.clock.tick(60) / 1000

NoteCharter().run()