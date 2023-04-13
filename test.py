from track import Track

def test_track_class():
    track1 = Track(index=1, artist="Artist 1", title="Track 1", genre="Genre 1", duration=180, added_date="2023-01-01", bit_depth=16, file_path="path1", bpm=175, key="9A", rating=4)
    track2 = Track(index=2, artist="Artist 2", title="Track 2", genre="Genre 2", duration=180, added_date="2023-01-01", bit_depth=16, file_path="path2", bpm=170, key="2A", rating=5)
    # track3 = Track(index=3, artist="Artist 3", title="Track 3", genre="Genre 3", duration=180, added_date="2023-01-01", bit_depth=16, file_path="path3", bpm=124, key="2A", rating=3)
    # track4 = Track(index=4, artist="Artist 4", title="Track 4", genre="Genre 4", duration=180, added_date="2023-01-01", bit_depth=16, file_path="path4", bpm=126, key="2B", rating=2)

    tracks = [track1, track2]

    for i, track_a in enumerate(tracks):
        for j, track_b in enumerate(tracks):
            if i != j:
                key_score = track_a.key_compatibility_score(track_b)
                bpm_score = track_a.bpm_compatibility_score(track_b)

                print(f"Key kompatibility score between {track_a.title} ({track_a.key + ' '}) and {track_b.title} ({track_b.key + ' '}): {key_score}")
                # print(f"Bpm kompatibility score between {track_a.title} ({track_a.bpm}) and {track_b.title} ({track_b.bpm}): {bpm_score}")
            break


if __name__ == "__main__":
    test_track_class()
