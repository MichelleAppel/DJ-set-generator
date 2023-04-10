import csv
import re
from typing import List
from track import Track

def parse_txt_file(file_path: str) -> List[Track]:
    tracks = []
    
    with open(file_path, "r", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter="\t")
        next(csvreader)  # Skip header line
        
        for row in csvreader:
            index = int(row[0])
            title = row[2]
            artist = row[3]
            genre = row[4]
            bpm = float(row[5].replace(",", "."))
            rating = len(row[6].strip()) if row[6].strip() else 0
            duration = int(row[7][:2]) * 60 + int(row[7][-2:])  # Convert duration to seconds
            key = row[8]
            added_date = row[10]
            bit_depth = int(row[11])

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