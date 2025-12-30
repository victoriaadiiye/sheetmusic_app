import pytest
from unittest.mock import patch
from music21 import stream, note, chord, meter, key
from tab_creation_app.converter import (
    get_tuning,
    generate_name,
    transpose_score,
    convert_to_lilypond,
    iterate_measure,
    write_lilypond_tab,
    convert,
)
import os


# -------------------------------
# Fixtures
# -------------------------------
@pytest.fixture
def simple_score_file(tmp_path):
    """Create a simple MusicXML file for testing convert."""
    s = stream.Score()
    p = stream.Part()
    m = stream.Measure()
    m.append(note.Note("C4", quarterLength=1))
    p.append(m)
    s.append(p)
    file_path = tmp_path / "simple_score.xml"
    s.write("musicxml", fp=str(file_path))
    return str(file_path)


# -------------------------------
# get_tuning tests
# -------------------------------
def test_get_tuning_default():
    assert get_tuning("standard") == "#'standard \\stringTuning <e, a, d g b e'>"


def test_get_tuning_custom_valid():
    assert get_tuning("abcdef") == "#'abcdef \\stringTuning <a, b, c, d, e, f>’"


def test_get_tuning_invalid():
    assert get_tuning("abc") is None


# -------------------------------
# generate_name tests
# -------------------------------
def test_generate_name_empty():
    assert generate_name("") == "mA"


def test_generate_name_simple_increment():
    assert generate_name("mA") == "mB"
    assert generate_name("mZ") == "mAA"
    assert generate_name("mZZ") == "mAAA"


def test_generate_name_invalid_input():
    with pytest.raises(ValueError):
        generate_name("A")
    with pytest.raises(ValueError):
        generate_name("mAB")


# -------------------------------
# transpose_score tests
# -------------------------------
def test_transpose_score_inplace():
    s = stream.Score()
    p = stream.Part()
    p.append(note.Note("C4"))
    s.append(p)
    t_score = transpose_score(s, transpose=True, interval="P8")
    assert t_score.parts[0].notes[0].pitch.nameWithOctave == "C5"


# -------------------------------
# convert_to_lilypond tests
# -------------------------------
def test_convert_to_lilypond_notes_and_key():
    s = stream.Score()
    p = stream.Part()
    m = stream.Measure()
    m.append(note.Note("C4", quarterLength=1))
    m.append(note.Rest(quarterLength=1))
    m.append(chord.Chord(["E4", "G4"], quarterLength=2))
    m.append(key.Key("G"))
    m.append(meter.TimeSignature("4/4"))
    p.append(m)
    s.append(p)

    notes, time_sig, key_sig = convert_to_lilypond(s)
    assert "c" in notes.lower()
    assert "|" in notes
    assert time_sig == "4/4"
    assert key_sig.startswith("g")


# -------------------------------
# iterate_measure tests
# -------------------------------
def test_iterate_measure_multiple_measures():
    s = stream.Score()
    p = stream.Part()
    for _ in range(5):
        m = stream.Measure()
        m.append(note.Note("C4"))
        p.append(m)
    s.append(p)
    current_scores, time_sig, key_sig = iterate_measure(s)
    assert isinstance(current_scores, str)
    assert "|" in current_scores


# -------------------------------
# write_lilypond_tab tests
# -------------------------------
def test_write_lilypond_tab(tmp_path):
    code = "c' d' e'"
    file = tmp_path / "test.ly"
    filename = write_lilypond_tab(code, str(file))
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        content = f.read()
    assert content == code


# -------------------------------
# Full convert pipeline tests
# -------------------------------
def test_convert_pipeline(simple_score_file, tmp_path):
    """Test the convert function end-to-end without writing files."""
    with patch("music2lilypond.converter.os.makedirs") as mock_makedirs, patch(
        "music2lilypond.converter.write_lilypond_tab", return_value="mock_file.ly"
    ) as mock_write:

        filename = convert(
            file_path=simple_score_file,
            tuning_arg="standard",
            transpose=True,
            output_dir=str(tmp_path),
        )

        mock_makedirs.assert_called_once_with(str(tmp_path), exist_ok=True)
        assert mock_write.called
        assert filename == "mock_file.ly"


def test_convert_invalid_tuning(simple_score_file, tmp_path):
    """Check that convert raises an error for invalid tuning."""
    with pytest.raises(ValueError):
        convert(
            file_path=simple_score_file,
            tuning_arg="invalid_tuning",
            transpose=True,
            output_dir=str(tmp_path),
        )
