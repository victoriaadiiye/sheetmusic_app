from music21 import stream, note, chord, converter, clef, tempo, dynamics, key, meter
from tab_creation.lilypond_lib import create_lilypond_note, create_lilypond_chord, create_lilypond_rest, generate_staff_groups, generate_guitar_tab, generate_pdf_from_lilypond
from tab_creation.utils import get_tuning, generate_name
import os

def write_lilypond_tab(lilypond_code: str, filename: str) -> str:
    """
    Write LilyPond code to a file.

    Args:
        lilypond_code: The LilyPond code to write.
        filename: Path to the output file.

    Returns:
        The filename written.
    """
    with open(filename, "w") as f:
        f.write(lilypond_code)
    return filename


def import_score(file_path: str) -> stream.Score:
    """
    Import a music score using music21.

    Args:
        file_path: Path to the music file.

    Returns:
        A music21 stream.Score object.
    """
    return converter.parse(file_path)


def transpose_score(s: stream.Score, transpose: bool = False, interval: str = 'P8', new_clef: clef.Clef | None = None) -> stream.Score:
    """
    Optionally transpose a score and set a new clef for all parts.

    Args:
        s: music21 Score object.
        transpose: Whether to transpose the score.
        interval: Interval for transposition (default: octave 'P8').
        new_clef: Clef to apply (default: TrebleClef).

    Returns:
        Transposed and clef-updated score.
    """
    new_clef = new_clef or clef.TrebleClef()

    if transpose:
        s.transpose(interval, inPlace=True)

    for part in s.parts:
        for old_clef in part.recurse().getElementsByClass(clef.Clef):
            part.remove(old_clef, recurse=True)
        part.insert(0, new_clef)

    return s


def convert_to_lilypond(s: stream.Score) -> tuple[str, str, str]:
    """
    Convert a music21 Score to LilyPond notation for notes, key, and time signature.

    Args:
        s: music21 Score object.

    Returns:
        Tuple of (notes string, time signature, key signature).
    """
    temp: list[str] = []
    time_signature: str = ""
    key_signature: str = ""

    for part in s.parts:
        for m in part.recurse().getElementsByClass(stream.Measure):
            measure: list[str] = []
            for n in m.recurse():
                if isinstance(n, note.Note):
                    measure.append(create_lilypond_note(n))
                elif isinstance(n, chord.Chord):
                    measure.append(create_lilypond_chord(n))
                elif isinstance(n, note.Rest):
                    measure.append(create_lilypond_rest(n))
                elif isinstance(n, key.Key):
                    ks = n.name
                    key_signature = ks.replace(" ", " \\").lower()
                elif isinstance(n, meter.TimeSignature):
                    new_TS = f"{n.numerator}/{n.denominator}"
                    if new_TS != time_signature:
                        time_signature = new_TS
            measure.extend('|')
            temp.extend(measure)

    notes: str = ' '.join(temp)
    return notes, time_signature, key_signature


def iterate_measure(s: stream.Score) -> tuple[str, str, str]:
    """
    Iterate over measures of a score and convert them to LilyPond staff groups.

    Args:
        s: music21 Score object.

    Returns:
        Tuple of (current_scores string, time signature, key signature).
    """
    x = 1
    current_scores: str = ''
    key_signature: str = ''
    measures: int = len(s.parts[0].getElementsByClass('Measure'))
    name: str = ''

    while s.measure(x):
        notes, time_signature_temp, key_signature_temp = convert_to_lilypond(s.measures(x, x + 3))
        if time_signature_temp:
            time_signature = time_signature_temp
        if key_signature_temp:
            key_signature = key_signature_temp
        name = generate_name(name)
        current_scores = generate_staff_groups(notes, name, current_scores)

        if x >= measures:
            break
        x += 4

    return current_scores, time_signature, key_signature


def convert(
    file_path: str, 
    tuning_arg: str, 
    transpose: bool = True, 
    output_dir: str = ".", 
    generate_pdf: bool = True
) -> str:
    """
    Convert a music file to LilyPond guitar tab and optionally generate a PDF.

    Args:
        file_path: Path to the input music file.
        tuning_arg: Name of the tuning or a 6-character string.
        transpose: Whether to transpose the score.
        output_dir: Directory to write output LilyPond file.
        generate_pdf: Whether to create a PDF via LilyPond.

    Returns:
        Path to the generated PDF if generate_pdf=True, otherwise the .ly file.
    """
    print(f"Creating a fingering for {file_path} using {tuning_arg}")

    tuning = get_tuning(tuning_arg)
    if tuning is None:
        raise ValueError(f"No recognised tuning option provided: {tuning_arg}")

    s = import_score(file_path)
    title = os.path.basename(file_path)
    title = title[:title.rfind('.')] or "untitled"

    if transpose:
        s = transpose_score(s, transpose)

    os.makedirs(output_dir, exist_ok=True)
    ly_file = os.path.join(output_dir, f"{title}_{tuning_arg}.ly")

    current_scores, time_signature, key_signature = iterate_measure(s)
    ly_code = generate_guitar_tab(current_scores, time_signature, key_signature, tuning, tuning_arg)
    write_lilypond_tab(ly_code, ly_file)

    if generate_pdf:
        pdf_file = generate_pdf_from_lilypond(ly_file, output_dir)
        print(f"✅ PDF created: {pdf_file}")
        return pdf_file

    return ly_file

