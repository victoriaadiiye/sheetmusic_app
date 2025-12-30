DEFAULT_TUNINGS: dict[str, str] = {
    "standard": "#'standard \\stringTuning <e, a, d g b e'>",
    "drop-d": "#'drop-d \\stringTuning <d, a, d g b e'>",
    "open-g": "#'open-g \\stringTuning <d, g, d g b d'>",
    "dadgad": "#'dadgad \\stringTuning <d, a, d g a d'>",
    "guitar-cello-tuning": "#'guitar-cello-tuning \\stringTuning <c, g, d g a e'>",
    "bouzouki": "#'bouzouki \\stringTuning <g, d a d'>",
}


def get_tuning(tuning: str) -> str | None:
    """
    Return a LilyPond tuning string for a given tuning name or 6-character custom tuning.

    Args:
        tuning: Name of a standard tuning or a 6-character string representing custom tuning.

    Returns:
        LilyPond string for the tuning, or None if invalid.
    """
    if tuning in DEFAULT_TUNINGS:
        return DEFAULT_TUNINGS[tuning]

    if len(tuning) == 6:
        return f"#'{tuning} \\stringTuning <{', '.join(tuning)}>’"

    return None


def generate_name(s: str) -> str:
    """
    Generate the next staff group name for LilyPond.

    Args:
        s: Current staff group name (must start with 'm').

    Returns:
        Next staff group name, e.g., "mA" -> "mB", "mZ" -> "mAA".

    Raises:
        ValueError: If input is invalid.
    """
    if not s:
        return "mA"
    if not s.startswith("m"):
        raise ValueError("Input must start with 'm'")

    letters = s[1:]
    if len(set(letters)) != 1:
        raise ValueError("All letters after 'm' must be the same")

    c = letters[0]
    length = len(letters)

    if c == "Z":
        next_letters = "A" * (length + 1)
    else:
        next_letters = chr(ord(c) + 1) * length

    return "m" + next_letters
