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

1.  Clone the repository.
    
```bash
git clone https://github.com/yourusername/dj-set-generator.git cd dj-set-generator
```
    
2. Prepare a Rekordbox playlist exported as a .txt file and a corresponding .m3u8 file.
    
3. Run the `main.py` script with the appropriate command line arguments:
    
```bash
python main.py --playlist_txt_path /path/to/playlist.txt --playlist_m3u8_path /path/to/playlist.m3u8 --output_file /path/to/output.m3u8 --set_length 10 --min_rating 3 --algorithm greedy
```

Replace `/path/to/playlist.txt`, `/path/to/playlist.m3u8`, and `/path/to/output.m3u8` with the appropriate file paths, and adjust the `set_length`, `min_rating`, and `algorithm` arguments as desired. Available algorithms are `greedy`, `dynamic`, `genetic`, and `simulated_annealing`.
    
4. Import the generated M3U8 playlist into Rekordbox.

## License

MIT License. See `LICENSE` for more details.
