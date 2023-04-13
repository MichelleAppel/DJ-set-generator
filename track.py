class Track:
    def __init__(self, index: int, title: str, artist: str, genre: str, bpm: float, rating: int, duration: int, key: str, added_date: str, bit_depth: int, file_path: str):
        self.index = index
        self.title = title
        self.artist = artist
        self.genre = genre
        self.bpm = bpm
        self.rating = rating
        self.duration = duration
        self.key = key
        self.added_date = added_date
        self.bit_depth = bit_depth
        self.file_path = file_path

    def __str__(self):
        return f"{self.artist} - {self.title}"
    
    
    def key_compatibility_score(self, other):
        def camelot_to_number(key):
            number = key[:-1]
            return int(number)

        key_a = camelot_to_number(self.key)
        key_b = camelot_to_number(other.key)
        key_diff = abs(key_a - key_b) % 12

        if key_diff in (0, 12):  # Same key
            score = 7
        elif key_diff in (1, 11):  # One step apart
            score = 6
        elif key_diff in (2, 10):  # Two steps apart
            score = 5
        elif key_diff in (3, 9):  # Three steps apart
            score = 4
        elif key_diff in (4, 8):  # Four steps apart
            score = 3
        elif key_diff in (5, 7):  # Five steps apart
            score = 2
        else:  # Six steps apart
            score = 1

        return score / 7  # Normalize the score to be between 0 and 1


    def bpm_compatibility_score(self, other):
        bpm_difference = abs(self.bpm - other.bpm)
        max_bpm_diff = 20  # You can adjust this value based on your preference

        score = 1 - (bpm_difference / max_bpm_diff)
        score = max(0, min(1, score))  # Ensure the score is in the range [0, 1]

        return score
