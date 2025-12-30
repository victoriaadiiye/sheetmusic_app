# tab_creation/__init__.py

# Import main conversion functions
from .converter import (
    convert,
    import_score,
    transpose_score,
    iterate_measure,
    convert_to_lilypond,
    write_lilypond_tab,
)

# Import helper functions
from .utils import get_tuning, generate_name

# Import LilyPond-specific functions
from .lilypond_lib import (
    create_lilypond_note,
    create_lilypond_chord,
    create_lilypond_rest,
    generate_staff_groups,
    generate_guitar_tab,
    generate_pdf_from_lilypond,
)

# Define what will be exported when someone does:
# from tab_creation import *
__all__ = [
    "convert",
    "import_score",
    "transpose_score",
    "iterate_measure",
    "convert_to_lilypond",
    "write_lilypond_tab",
    "get_tuning",
    "generate_name",
    "create_lilypond_note",
    "create_lilypond_chord",
    "create_lilypond_rest",
    "generate_staff_groups",
    "generate_guitar_tab",
    "generate_pdf_from_lilypond",
]
