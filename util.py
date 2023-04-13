def print_dj_set(dj_set):
    # Find the maximum lengths for each column
    max_artist_length = max(len(track.artist) for track in dj_set)
    max_title_length = max(len(track.title) for track in dj_set)
    max_key_length = max(len(track.key) for track in dj_set)

    # Print the header row
    print(f"{'Artist name':<{max_artist_length}} | {'Track name':<{max_title_length}} | BPM    | {'Key':<{max_key_length}} | Rating")

    # Print the track information
    for track in dj_set:
        stars = '*' * track.rating
        print(f"{track.artist:<{max_artist_length}} | {track.title:<{max_title_length}} | {track.bpm:6.2f} | {track.key:<{max_key_length}} | {stars}")
