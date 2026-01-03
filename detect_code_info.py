from pygments.lexers import guess_lexer_for_filename
from pygments.lexer import Lexer
from pygments.util import ClassNotFound
from detect_indent import detect_indent
from detect_indent.detect_indentation import INDENT_TYPE_SPACE, INDENT_TYPE_TAB
from enum import Enum, auto

class IndentType(Enum):
    space = 0
    tab = auto()

class CodeInfo:
    is_code: bool = False
    lexer: Lexer | None = None
    language: str | None = None
    indent_type: IndentType | None = None
    indent_size: int | None = None

def detect_code_info(filename: str, text: str):
    result = CodeInfo()

    # Try to guess the language using Pygments
    try:
        lexer = guess_lexer_for_filename(filename, text)
        if lexer.name == "Text only":
            return result
        result.is_code = True
        result.language = lexer.name
        result.lexer = lexer
    except ClassNotFound:
        return result  # not code

    # Detect indentation style if it's code
    di = detect_indent(text)
    if di and di.get("type"):
        result.indent_type = IndentType.space if di.get("type") == INDENT_TYPE_SPACE else IndentType.tab
        result.indent_size = di.get("amount") or None

    return result
