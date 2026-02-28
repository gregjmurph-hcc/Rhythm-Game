import pygame
import json

from scripts.game_state import *
from scripts.button_object import *
from scripts.note import *

class PlayingSong(GameState):
    def __init__(self, game, chart_data, bpm, audio_path):
        super().__init__(game)

        self.chart_data = chart_data
        self.bpm = bpm
        self.beat_duration = 60 / bpm * 1000

        self.notes = []
        for tap in chart_data.get('tap_notes', []):
            lane, beat = tap
            self.notes.append(Note(lane, beat * self.beat_duration))
        for hold in chart_data.get('hold_notes', []):
            lane, beat, end_beat = hold
            self.notes.append(Note(lane, beat * self.beat_duration, end_beat * self.beat_duration))

        self.lane_x = [180, 300, 420, 540]
        self.lane_keys = ['left_lane', 'up_lane', 'down_lane', 'right_lane']
        self.lane_colors = [(90, 255, 150), (255, 255, 255), (255, 255, 255), (90, 255, 150)]
        self.lane_pressed = [False, False, False, False]

        self.hit_y = 620
        self.note_speed = 400
        self.travel_time = ((self.hit_y + 40) / self.note_speed) * 1000

        self.hit_window = 120
        self.good_window = 220

        self.score = 0
        self.combo = 0
        self.judgement = ''
        self.judgement_timer = 0

        self.held_notes = {}

        self.state = 'countdown'
        self.countdown = 4
        self.countdown_timer = 0
        self.music_started = False
        self.song_length = pygame.mixer.Sound(audio_path).get_length() * 1000

        self.title = TextObject((self.game.screen_width / 2, 50), None, 48, (255, 255, 255))
        self.score_text = TextObject((self.game.screen_width - 20, 20), None, 48, (255, 255, 255))
        self.combo_text = TextObject((self.game.screen_width / 2, 520), None, 48, (255, 255, 255))
        self.judgement_text = TextObject((self.game.screen_width / 2, 470), None, 48, (255, 255, 255))
        self.countdown_text = TextObject((self.game.screen_width / 2, self.game.screen_height / 2), None, 128, (255, 255, 255))
        self.paused_text = TextObject((self.game.screen_width / 2, self.game.screen_height / 2 - 60), None, 102, (255, 255, 255))

        self.quit_button = ButtonObject((self.game.screen_width / 2, self.game.screen_height / 2 + 80), (200, 60), 'Quit', font_size=36, hover_color=(215, 255, 215))
        self.quit_button.color = (90, 255, 150)

        self.title.write(chart_data.get('name', ''))
        self.paused_text.write('Paused')

    def handle_keydown(self, key):
        if key == self.game.key_bindings['pause']:
            if self.state == 'playing':
                self.state = 'paused'
                pygame.mixer.music.pause()
            elif self.state == 'paused':
                self.state = 'countdown'
                self.countdown = 4
                self.countdown_timer = 0
            return

        if self.state != 'playing':
            return

        for i, action in enumerate(self.lane_keys):
            if key == self.game.key_bindings[action]:
                self.lane_pressed[i] = True

                music_pos = pygame.mixer.music.get_pos()
                best_note = None
                best_diff = float('inf')

                for note in self.notes:
                    if note.lane != i or note.hit:
                        continue
                    diff = abs(music_pos - note.start_time)
                    if diff < best_diff and diff <= self.good_window:
                        best_diff = diff
                        best_note = note

                if best_note:
                    best_note.hit = True
                    if best_note.is_hold():
                        self.held_notes[i] = best_note
                    self.combo += 1
                    if best_diff <= self.hit_window:
                        self.score += 300 * self.combo
                        self.judgement = 'Perfect'
                    else:
                        self.score += 100 * self.combo
                        self.judgement = 'Good'
                    self.judgement_timer = 0.6

    def handle_keyup(self, key):
        if self.state != 'playing':
            return

        for i, action in enumerate(self.lane_keys):
            if key == self.game.key_bindings[action]:
                self.lane_pressed[i] = False

                if i in self.held_notes:
                    note = self.held_notes.pop(i)
                    music_pos = pygame.mixer.music.get_pos()
                    if music_pos >= note.end_time - self.good_window:
                        self.combo += 1
                        if abs(music_pos - note.end_time) <= self.hit_window:
                            self.score += 300 * self.combo
                            self.judgement = 'Perfect'
                        else:
                            self.score += 100 * self.combo
                            self.judgement = 'Good'
                    else:
                        self.combo = 0
                        self.judgement = 'Miss'
                    self.judgement_timer = 0.6

    def update(self, delta_time):
        if self.state == 'countdown':
            self.countdown_timer += delta_time * 1000
            if self.countdown_timer >= self.beat_duration:
                self.countdown_timer -= self.beat_duration
                self.countdown -= 1
                if self.countdown <= 0:
                    self.state = 'playing'
                    if not self.music_started:
                        pygame.mixer.music.play()
                        self.music_started = True
                    else:
                        pygame.mixer.music.unpause()

        if self.state == 'playing':
            music_pos = pygame.mixer.music.get_pos()

            for note in self.notes:
                if not note.hit and music_pos > note.start_time + self.good_window:
                    note.hit = True
                    if note.lane not in self.held_notes:
                        self.combo = 0
                        self.judgement = 'Miss'
                        self.judgement_timer = 0.6

            if self.judgement_timer > 0:
                self.judgement_timer -= delta_time

            if self.music_started and pygame.mixer.music.get_pos() >= self.song_length:
                pygame.mixer.music.stop()
                self.game.current_state = self.game.song_picker

        if self.state == 'paused':
            self.quit_button.update(self.game.mouse_pos)
            if self.quit_button.is_clicked(self.game.mouse_pos, self.game.mouse_clicked):
                pygame.mixer.music.stop()
                self.game.current_state = self.game.song_picker

    def render(self, screen):
        screen.fill((30, 210, 140))

        for i, x in enumerate(self.lane_x):
            pygame.draw.rect(screen, (20, 170, 115), pygame.Rect(x - 50, 0, 100, self.game.screen_height))
            if self.lane_pressed[i]:
                pygame.draw.rect(screen, self.lane_colors[i], pygame.Rect(x - 50, self.hit_y - 15, 100, 30), border_radius=6)
            else:
                pygame.draw.rect(screen, self.lane_colors[i], pygame.Rect(x - 50, self.hit_y - 15, 100, 30), border_radius=6, width=3)

        if self.music_started:
            music_pos = pygame.mixer.music.get_pos()
        else:
            music_pos = -self.travel_time

        for note in self.notes:
            if note.hit and not note.is_hold():
                continue
            if note.hit and note.lane not in self.held_notes:
                continue

            time_until = note.start_time - music_pos
            progress = 1 - (time_until / self.travel_time)
            y = -40 + progress * (self.hit_y + 40)

            if y < -40 or y > self.game.screen_height + 40:
                continue

            x = self.lane_x[note.lane]
            col = self.lane_colors[note.lane]

            if note.is_hold():
                end_time_until = note.end_time - music_pos
                end_progress = 1 - (end_time_until / self.travel_time)
                end_y = -40 + end_progress * (self.hit_y + 40)
                draw_y = min(y, self.hit_y)
                hold_surf = pygame.Surface((80, max(1, int(draw_y - end_y))), pygame.SRCALPHA)
                hold_surf.fill((*col, 140))
                screen.blit(hold_surf, (x - 40, end_y))
                pygame.draw.rect(screen, col, pygame.Rect(x - 50, end_y - 15, 100, 30), border_radius=6)

            if y <= self.hit_y:
                pygame.draw.rect(screen, col, pygame.Rect(x - 50, y - 15, 100, 30), border_radius=6)

        self.score_text.write(f'{self.score:,}')
        self.score_text.rect = self.score_text.text.get_rect(topright=(self.game.screen_width - 20, 20))
        screen.blit(self.score_text.text, self.score_text.rect)

        if self.combo > 1:
            self.combo_text.write(f'{self.combo}x')
            self.combo_text.render(screen)

        if self.judgement_timer > 0:
            self.judgement_text.write(self.judgement)
            self.judgement_text.render(screen)

        self.title.render(screen)

        if self.state == 'countdown':
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            self.countdown_text.write(str(max(1, self.countdown)))
            self.countdown_text.render(screen)

        if self.state == 'paused':
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            self.paused_text.render(screen)
            self.quit_button.render(screen)