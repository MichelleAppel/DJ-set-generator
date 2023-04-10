import sys
import os
import argparse

class Playlist:
    def __init__(self, original_m3u8_file, new_m3u8_file):
        self.original_m3u8_file = original_m3u8_file
        self.new_m3u8_file = new_m3u8_file

    def generate_new_m3u8(self, selected_indices):
        with open(self.original_m3u8_file, 'r') as file:
            lines = file.readlines()

        with open(self.new_m3u8_file, 'w') as new_file:
            new_file.write("#EXTM3U\n")
            for index in selected_indices:
                extinf_line = lines[index * 2 - 1]
                track_path_line = lines[index * 2]
                new_file.write(extinf_line)
                new_file.write(track_path_line)

    def import_indices_from_file(self, indices_file):
        with open(indices_file, 'r') as file:
            indices_list = [int(index.strip()) for index in file.readlines()]
        return indices_list

def main(args):
    set_folder = args.root_folder
    indices_file = os.path.join(args.root_folder, args.indices_file)

    original_m3u8_file = os.path.join(set_folder, 'original_playlist.m3u8')
    new_m3u8_filename = os.path.splitext(os.path.basename(indices_file))[0] + '_playlist.m3u8'
    new_m3u8_file = os.path.join(set_folder, new_m3u8_filename)

    playlist = Playlist(original_m3u8_file, new_m3u8_file)
    selected_indices = playlist.import_indices_from_file(indices_file)
    playlist.generate_new_m3u8(selected_indices)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate new .m3u8 file from the original playlist and indices file')
    parser.add_argument('--root_folder', help='The root folder containing the original .m3u8 file')
    parser.add_argument('--indices_file', help='The file containing the list of selected indices')
    args = parser.parse_args()
    main(args)
