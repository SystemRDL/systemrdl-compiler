import re

def get_illegal_trailing_text_pos(text: str, idx: int) -> tuple:
    """
    Scan the remainder of a line for illegal text.
    Verilog preprocessor directives require that there be no trailing text,
    except for comments.

    If illegal text is found, return the start/end index of it as a tuple.
    Otherwise return (None, None)
    """

    # First, scan ahead past all block comments
    bc_regex = re.compile(r'(?:[ \t]*/\*.*?\*/)*[ \t]*')
    m = bc_regex.match(text, idx)
    assert m is not None
    idx = m.end()

    # Assert that any remaining text is a comment
    rem_regex = re.compile(r'(:?//.*|/\*.*)?$', re.MULTILINE)
    m = rem_regex.match(text, idx)
    if m:
        return (None, None)
    else:
        # Did not match. Find end of the line
        eol_regex = re.compile(r'.+$', re.MULTILINE)
        m = eol_regex.match(text, idx)
        return (m.start(), m.end())
