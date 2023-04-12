import csv
import re
from typing import List
from track import Track

def parse_txt_file(file_path: str) -> List[Track]:
    tracks = []

    with open(file_path, "r", encoding="utf-16") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        
        # Parse header line to create a mapping of column names to positions
        header = next(csvreader)
        col_map = {name.lower(): pos for pos, name in enumerate(header)}

        for row in csvreader:
            index = int(row[col_map['#']])
            title = row[col_map['titel van muziekstuk']]
            artist = row[col_map['artiest']]
            genre = row[col_map['genre']]
            bpm = float(row[col_map['bpm']].replace(",", "."))
            rating = len(row[col_map['beoordeling']].strip()) if row[col_map['beoordeling']].strip() else 0
            duration_str = row[col_map['duur']]
            duration = int(duration_str[:2]) * 60 + int(duration_str[-2:])  # Convert duration to seconds
            key = row[col_map['toonsoort']]
            added_date = row[col_map['datum toegevoegd']]
            bit_depth = int(row[col_map['bitdiepte']])

            track = Track(index, title, artist, genre, bpm, rating, duration, key, added_date, bit_depth, "")
            tracks.append(track)

    return tracks


def parse_m3u8_file(file_path: str) -> List[str]:
    file_paths = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
        for line in lines:
            if not line.startswith("#"):
                file_path = line.strip()
                file_paths.append(file_path)

    return file_paths