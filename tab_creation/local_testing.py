import os
from converter import convert 

def test_conversion():
    """
    Test the MusicXML -> .ly conversion locally.
    Adjust file_path and tuning as needed.
    """
    # Path to a sample MusicXML file
    file_path = "/Users/victoriaadiiye/Projects/sheetmusic/bartokduets_pizzicato_pt1.musicxml"

    # Choose a tuning
    tuning = "guitar-cello-tuning"

    # Directory where output .ly file will be written
    output_dir = "test_outputs"

    # Run conversion
    print(f"Running conversion for {file_path} with tuning '{tuning}'...")
    output_file = convert(file_path, tuning, transpose=False, output_dir=output_dir)

    # Check if file exists
    if os.path.exists(output_file):
        print(f"✅ Conversion successful! Output file: {output_file}")
    else:
        print(f"❌ Conversion failed. No output file created.")

if __name__ == "__main__":
    test_conversion()