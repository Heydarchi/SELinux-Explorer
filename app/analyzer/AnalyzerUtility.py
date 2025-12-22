def clean_line(input_str: str):
    """Normalize a policy file line.

    - Removes occurrences of literal "--" (preserves previous behaviour).
    - Strips inline comments starting with `#`, but ignores `#` inside quotes.
    - Returns None for empty or comment-only lines.
    """
    if input_str is None:
        return None

    # Keep legacy behaviour of removing double-dash
    input_str = input_str.replace("--", "")

    # Walk the string and find first '#' that is not inside quotes
    in_single = False
    in_double = False
    s = input_str
    for i, ch in enumerate(s):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            s = s[:i]
            break

    cleaned = s.strip()
    if cleaned == "":
        return None
    return cleaned
