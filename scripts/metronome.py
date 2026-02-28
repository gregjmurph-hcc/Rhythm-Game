import pygame

class Metronome:
    def __init__(self, bpm, beat_window):
        self.music_pos = 0
        self.current_beat = 1
        self.beat_duration = 60 / bpm * 1000
        self.next_beat_pos = self.beat_duration
        self.beat_window = beat_window

        self.active_beat = True
        self.active_beat_start = self.next_beat_pos - self.beat_window
        self.active_beat_end = self.next_beat_pos + self.beat_window

    def tick(self):
        self.music_pos = pygame.mixer.music.get_pos()
        self.active_beat_start = self.next_beat_pos - self.beat_window
        self.active_beat_end = self.next_beat_pos + self.beat_window

        self.in_beat = self.music_pos >= self.active_beat_start and self.music_pos <= self.active_beat_end

        if self.music_pos >= self.next_beat_pos:
            self.current_beat += 1
            self.next_beat_pos += self.beat_duration 
            if self.current_beat > 4:
                self.current_beat = 1