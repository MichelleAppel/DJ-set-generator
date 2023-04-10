# M3u8 Playlist Generator

The `generate_set.py` script is a tool for generating a new .m3u8 playlist file from an original .m3u8 file, using a list of selected track indices.

## Requirements

-   Python 3.6+

## Usage

1.  Clone the repository:
    
     ```git clone https://github.com/MichelleAppel/AI_set.git cd AI_set```
    
-   Prepare the input files:
    
    -   Place the original .m3u8 playlist file in a folder of your choice.
    -   Create a .txt file containing the list of track indices, one per line, that you want to include in the new playlist.
-   Run the script:
    
     ```python playlist_generator.py --root_folder /path/to/your/folder --indices_file indices.txt```
    
    Replace `/path/to/your/folder` with the path to the folder containing your original .m3u8 file and `indices.txt` with the name of your indices file.
    
    This will generate a new .m3u8 file in the same folder as the original .m3u8 file, with a name based on the indices file (e.g., `indices_playlist.m3u8`).
    

## Example

Suppose you have the following file structure:

```
my_sets/
    original_playlist.m3u8
    track_indices.txt
```

Run the script with the following command:

```python playlist_generator.py --root_folder my_sets --indices_file track_indices.txt```

This will generate a new .m3u8 file named `track_indices_playlist.m3u8` in the `my_sets` folder.

## License

MIT License. See `LICENSE` for more information.
