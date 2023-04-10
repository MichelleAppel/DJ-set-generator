# DJ Set Generator

DJ Set Generator is a Python tool for creating DJ sets from Rekordbox playlists. The tool takes into account track key compatibility, BPM compatibility, and track ratings to generate a coherent and smooth DJ set.

## Features

-   Supports various algorithms for generating DJ sets:
    -   Greedy
    -   Dynamic Programming
    -   Genetic Algorithm
    -   Simulated Annealing
-   Prioritizes tracks with a certain minimum rating without excluding any tracks from the selection
-   Exports generated DJ sets to M3U8 playlists that can be imported into Rekordbox

## Requirements

-   Python 3.6 or higher

## Usage

1.  Clone the repository:
    
     ```bash
     git clone https://github.com/MichelleAppel/AI_set.git 
     cd AI_set
     ```
    
-   Prepare the input files:
    
    -   Place the original .m3u8 playlist file in a folder of your choice.
    -   Create a .txt file containing the list of track indices, one per line, that you want to include in the new playlist.
-   Run the script:
    
     ```bash
     python playlist_generator.py --root_folder /path/to/your/folder --indices_file indices.txt
     ```
    
Replace `/path/to/playlist.txt`, `/path/to/playlist.m3u8`, and `/path/to/output.m3u8` with the appropriate file paths, and adjust the `set_length`, `min_rating`, and `algorithm` arguments as desired. Available algorithms are `greedy`, `dynamic`, `genetic`, and `simulated_annealing`.
    
    This will generate a new .m3u8 file in the same folder as the original .m3u8 file, with a name based on the indices file (e.g., `indices_playlist.m3u8`).
    

## Example

Suppose you have the following file structure:

```markdown
my_sets/
    original_playlist.m3u8
    track_indices.txt
```

Run the script with the following command:

```bash
python playlist_generator.py --root_folder my_sets --indices_file track_indices.txt
```

This will generate a new .m3u8 file named `track_indices_playlist.m3u8` in the `my_sets` folder.

## License

MIT License. See `LICENSE` for more information.