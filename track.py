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
        def parse_key(key):
            key_number, key_letter = int(key[:-1]), key[-1]
            return key_number, key_letter

        key_number, key_letter = parse_key(self.key)
        other_key_number, other_key_letter = parse_key(other.key)

        number_difference = abs(key_number - other_key_number) % 12
        # if number_difference == 0:
        #     number_difference = 12

        letter_difference = 0 if key_letter == other_key_letter else 1

        if (key_letter == 'A' and other_key_letter == 'B') or (key_letter == 'B' and other_key_letter == 'A'):
            if number_difference in {1, 2}:
                return 1 - letter_difference
            elif number_difference in {11, 10}:
                return 1 - letter_difference - 0.5
            else:
                return 1 - letter_difference - 1

        return 2 - letter_difference - min(number_difference, 12 - number_difference) / 12


    def bpm_compatibility_score(self, other):
        bpm_difference = abs(self.bpm - other.bpm)
        max_bpm_diff = 15  # You can adjust this value based on your preference

        if bpm_difference > max_bpm_diff:
            return 0

        score = 1 - (bpm_difference / max_bpm_diff)
        return score