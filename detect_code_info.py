from collections import Counter
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
from detect_indent import detect_indent
import re

def detect_code_info(filename: str, text: str):
    """
    Detects if the input text is code and, if so:
      - what language it likely is
      - whether indentation uses tabs or spaces
      - if spaces, how many per indent level
    Returns a dict with these fields.
    """
    result = {"is_code": False, "lexer": None, "language": None, "indent_type": None, "indent_size": None}

    # Try to guess the language using Pygments
    try:
        lexer = guess_lexer_for_filename(filename, text)
        if lexer.name == "Text only":
            return result
        result["is_code"] = True
        result["language"] = lexer.name
        result["lexer"] = lexer
    except ClassNotFound:
        return result  # not code

    # Detect indentation style if it's code
    di = detect_indent(text)  # returns {'amount': n, 'type': 'space'|'tab'|None, 'indent': '  '}
    if di and di.get("type"):
        result["indent_type"] = di.get("type")
        result["indent_size"] = di.get("amount") or None
    pass

    # lines = [l for l in text.splitlines() if l.strip()]
    # indents = [re.match(r'^[ \t]+', l) for l in lines]
    # indents = [m.group(0) for m in indents if m]

    # if not indents:
    #     return result

    # tabs = sum('\t' in i for i in indents)
    # spaces = sum(' ' in i for i in indents)

    # if tabs > spaces:
    #     result["indent_type"] = "tabs"
    # elif spaces > tabs:
    #     result["indent_type"] = "spaces"
    #     # Estimate number of spaces per level
    #     space_counts = sorted({len(i) for i in indents if ' ' in i})
    #     if len(space_counts) >= 2:
    #         # try to infer common divisor
    #         diffs = [b - a for a, b in zip(space_counts, space_counts[1:])]
    #         most_common = Counter(diffs).most_common(1)
    #         result["indent_size"] = most_common[0][0] if most_common else space_counts[0] if space_counts else None
    #     elif space_counts:
    #         result["indent_size"] = space_counts[0]
    # else:
    #     result["indent_type"] = "mixed"

    return result
