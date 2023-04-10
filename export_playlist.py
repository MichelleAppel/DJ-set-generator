def export_to_m3u8(output_file, dj_set, track_paths):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('#EXTM3U\n')
        for track in dj_set:
            track_info = f"{track.artist} - {track.title}"
            track_duration = int(track.duration.total_seconds())
            track_path = track_paths[track]
            f.write(f'#EXTINF:{track_duration},{track_info}\n')
            f.write(f'{track_path}\n')
