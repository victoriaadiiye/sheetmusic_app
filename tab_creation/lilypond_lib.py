from music21 import *
from textwrap import dedent
import subprocess
import shlex
import os


def generate_pdf_from_lilypond(ly_file: str, output_dir: str = ".") -> str:
    """
    Run LilyPond to generate a PDF from a .ly file.

    Args:
        ly_file: Path to the LilyPond file (.ly)
        output_dir: Directory where the PDF will be created

    Returns:
        Path to the generated PDF file.
    """
    output_path = ly_file
    try:
        # -o specifies the output file prefix (LilyPond adds .pdf automatically)
        cmd = f"lilypond -o {shlex.quote(output_dir)} {shlex.quote(ly_file)}"
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LilyPond failed: {e}")

    pdf_file = os.path.join(
        output_dir, os.path.splitext(os.path.basename(ly_file))[0] + ".pdf"
    )
    if not os.path.exists(pdf_file):
        raise FileNotFoundError(f"PDF was not created: {pdf_file}")
    return pdf_file


OCTAVE_MAP = {
    0: ",,,,",
    1: ",,,",
    2: ",,",
    3: ",",
    4: "",
    5: "'",
    6: "''",
    7: "'''",
    8: "''''",
}

DURATION_MAP = {
    "Quarter": "4",
    "Dotted Quarter": "4.",
    "Eighth": "8",
    "Dotted Eighth": "8.",
    "Half": "2",
    "Dotted Half": "2.",
    "16th": "16",
    "Dotted 16th": "16.",
}


def create_lilypond_note(n, withduration=True):
    """Convert a Note object to a LilyPond note string."""
    name = n.pitch.name[0].lower()
    if "#" in n.pitch.name:
        name += "is"
    elif "-" in n.pitch.name:
        name += "es"

    octave = OCTAVE_MAP.get(n.octave, "")
    dur = DURATION_MAP.get(n.duration.fullName, "")

    if withduration:
        return f"{name}{octave}{dur}".replace(" ", "")
    else:
        return f"{name}{octave}".replace(" ", ""), dur


def create_lilypond_chord(c):
    """Convert a Chord object to a LilyPond chord string."""
    notes_str = []
    dur = None
    for note in c.notes:
        n_str, dur = create_lilypond_note(note, withduration=False)
        notes_str.append(n_str)

    chord_str = f"<{' '.join(notes_str)}> {dur}"
    return chord_str


def create_lilypond_rest(r):
    """Convert a Rest object to a LilyPond rest string."""
    dur = DURATION_MAP.get(r.duration.fullName, "")
    return f"r{dur}".replace(" ", "")


def generate_staff_groups(notes, name, current_scores):
    score_group = dedent(
        f"""
        {current_scores}
        {name} = {{ {notes} }}
        \\score {{ #(systemPair {name}) }}
    """
    )
    return score_group


def generate_guitar_tab(scores, time_signature, key_signature, tuning, tuning_name):

    lilypond_code = dedent(
        f"""
    \\version "2.24.0"
    \\makeDefaultStringTuning {tuning}
    \\paper {{
        indent = 0
        ragged-bottom = ##f
        ragged-last-bottom = ##f
        ragged-last = ##f
        ragged-right = ##f
    }}

    \\layout {{
    \\context {{
        \\Score
    }}
    \\context {{
        \\Staff
    }}
    }}
    #(define (systemPair music)
    #{{

        \\new StaffGroup <<
            \\new Staff {{ \\clef "treble_8" \\time {time_signature} \\key {key_signature} #music }}
            \\new TabStaff \\with {{ stringTunings = #{tuning_name} }}
            {{ \\clef "moderntab" \\time {time_signature} \\key {key_signature} #music }}
        >>
    #}})
    {scores}
    """
    )
    return lilypond_code
