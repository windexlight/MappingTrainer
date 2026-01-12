from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from pygments.token import Token
from pygments.lexer import RegexLexer
from pygments import lex
import re
from ngrams import ngrams


def make_ngram_lexer(ngrams, token=Token.Name.Tag, ignore_case=False):
    flags = re.IGNORECASE if ignore_case else re.RegexFlag(0)
    clean = []
    for s in ngrams:
        if not isinstance(s, str):
            continue
        s = s.strip()
        if s:
            clean.append(s)

    clean = sorted(clean, key=len, reverse=True)

    if not clean:
        class _EmptyLexer(RegexLexer):
            name = "EmptyNgramLexer"
            tokens = {
                'root': [
                    (r'.+', Token.Text),
                ]
            }
        return _EmptyLexer()

    escaped = [re.escape(s) for s in clean]
    pattern = r'(' + '|'.join(escaped) + r')'

    class _NgramLexer(RegexLexer):
        name = "NgramLexer"
        tokens = {
            'root': [
                (pattern, token),
                (r'.', Token.Text),
            ]
        }
    _NgramLexer.flags = flags

    return _NgramLexer()


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document, *, invert=False, lexer=None):
        super().__init__(document)
        self.n = 0
        self.lexer = lexer
        self.invert = invert
        self.text_char_format = QTextCharFormat()
        if invert:
            self.text_char_format.setForeground(QColor(170, 0, 0))
        else:
            self.text_char_format.setForeground(QColor(0, 170, 0))

        blue = "#0000FF"
        dark_blue = "#001080"
        brown = "#795E26"
        red = "#A31515"
        green = "#008000"
        teal = "#267F99"
        purple = "#646695"
        dark_red = "#800000"
        num_green = "#098658"
        gray = "#999999"
        black = "#000000"

        self.formats = {
            Token.Comment: self.make_format(green),
            Token.Comment.Single: self.make_format(green),
            Token.Comment.Multiline: self.make_format(green),
            Token.Comment.Preproc: self.make_format(gray),
            Token.Comment.Special: self.make_format(gray),

            Token.Keyword: self.make_format(blue),
            Token.Keyword.Constant: self.make_format(blue),
            Token.Keyword.Declaration: self.make_format(blue),
            Token.Keyword.Namespace: self.make_format(blue),
            Token.Keyword.Pseudo: self.make_format(blue),
            Token.Keyword.Reserved: self.make_format(blue),
            Token.Keyword.Type: self.make_format(blue),

            Token.Operator: self.make_format(black),
            Token.Operator.Word: self.make_format(blue),
            Token.Punctuation: self.make_format(black),

            Token.Name: self.make_format(black),
            Token.Name.Builtin: self.make_format(brown),
            Token.Name.Function: self.make_format(brown),
            Token.Name.Class: self.make_format(teal),
            Token.Name.Decorator: self.make_format(purple),
            Token.Name.Constant: self.make_format(blue),
            Token.Name.Attribute: self.make_format(dark_blue),
            Token.Name.Tag: self.make_format(dark_red),
            Token.Name.Variable: self.make_format(dark_blue),
            Token.Name.Exception: self.make_format(purple),

            Token.String: self.make_format(red),
            Token.String.Double: self.make_format(red),
            Token.String.Single: self.make_format(red),
            Token.String.Doc: self.make_format(green),
            Token.String.Interpol: self.make_format(red),
            Token.String.Regex: self.make_format(purple),
            Token.String.Symbol: self.make_format(red),
            Token.String.Other: self.make_format(red),

            Token.Number: self.make_format(num_green),
            Token.Number.Integer: self.make_format(num_green),
            Token.Number.Float: self.make_format(num_green),
            Token.Number.Hex: self.make_format(num_green),
            Token.Number.Oct: self.make_format(num_green),

            Token.Literal: self.make_format(num_green),
            Token.Literal.Date: self.make_format(num_green),

            Token.Generic.Heading: self.make_format(blue),
            Token.Generic.Subheading: self.make_format(purple),
            Token.Generic.Deleted: self.make_format(red),
            Token.Generic.Inserted: self.make_format(green),
            Token.Generic.Error: self.make_format(red),
            Token.Generic.Emph: self.make_format(black),
            Token.Generic.Strong: self.make_format(black),
            Token.Generic.Prompt: self.make_format(gray),
            Token.Generic.Output: self.make_format(gray),
            Token.Generic.Traceback: self.make_format(red),

            Token.Error: self.make_format(red),
        }

    def setHighlightLen(self, n: int):
        self.n = n

    def make_format(self, color, bold=False, italic=False, underline=False):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        if italic:
            fmt.setFontItalic(True)
        if underline:
            fmt.setFontUnderline(True)
        return fmt

    def set_lexer(self, lexer):
        if lexer is None:
            lexer = make_ngram_lexer(ngrams)
        self.lexer = lexer

    def highlightBlock(self, text):
        if not text.strip():
            return

        # Syntax highlighting
        if self.lexer:
            index = 0
            for token, content in lex(text, self.lexer):
                length = len(content)
                fmt = self.formats.get(token)
                if fmt:
                    self.setFormat(index, length, fmt)
                index += length

        # Green highlight of typed chars
        if self.currentBlock().blockNumber() == 0:  # first line
            if self.invert:
                if self.n < len(text) and len(text) > 0:
                    self.setFormat(self.n, len(text)-self.n, self.text_char_format)
            else:
                if self.n > 0 and len(text) > 0:
                    length = min(self.n, len(text))
                    self.setFormat(0, length, self.text_char_format)

