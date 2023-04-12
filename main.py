import argparse
from parse_files import parse_txt_file, parse_m3u8_file
from set_builder import build_dj_set
from export_playlist import export_to_m3u8

def main():
    parser = argparse.ArgumentParser(description="Create a DJ set from Rekordbox playlists.")
    parser.add_argument("--playlist_txt_path", type=str, required=True, help="Path to the .txt Rekordbox playlist")
    parser.add_argument("--playlist_m3u8_path", type=str, required=True, help="Path to the .m3u8 Rekordbox playlist")
    parser.add_argument("--output_file", type=str, default="output.m3u8", help="Output .m3u8 file")
    parser.add_argument("--set_length", type=int, default=10, help="Length of the DJ set")
    parser.add_argument("--min_rating", type=int, default=0, help="Minimum rating for track priority")
    parser.add_argument("--algorithm", type=str, choices=["greedy", "glued", "dynamic", "genetic", "simulated_annealing"], default="greedy", help="Algorithm used to build the DJ set")

    args = parser.parse_args()

    tracks, track_paths = parse_txt_file(args.playlist_txt_path), parse_m3u8_file(args.playlist_m3u8_path)
    dj_set = build_dj_set(tracks, args.set_length, args.min_rating, args.algorithm)
    export_to_m3u8(args.output_file, dj_set, track_paths)

if __name__ == "__main__":
    main()
