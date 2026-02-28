class Note:
    def __init__(self, lane, start_time, end_time=None):
        self.lane = lane
        self.start_time = start_time
        self.end_time = end_time  
        self.hit = False
        self.active = False

    def is_hold(self):
        return self.end_time is not None