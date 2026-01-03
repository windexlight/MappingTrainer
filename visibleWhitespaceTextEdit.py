import sys
import re
from PySide6.QtWidgets import QApplication, QPlainTextEdit
from PySide6.QtGui import QPainter, QColor, QFontMetrics, QTextCursor
from PySide6.QtCore import Qt, Signal

class VisibleWhitespaceTextEdit(QPlainTextEdit):
    enterPressed = Signal()
    backPressed = Signal()
    forwardPressed = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.n = 0
        self.invert = False
        self.indent_with_spaces = False
        self.spaces_per_indent_level = 4
        metrics = self.fontMetrics()
        self.setTabStopDistance(metrics.horizontalAdvance(" ") * 4)
        self.draw_return = True

    def setTypedChars(self, n: int, *, invert=False):
        self.n = n
        self.invert = invert

    def setIndentWithSpaces(self, n):
        self.indent_with_spaces = True
        if isinstance(n, int):
            self.spaces_per_indent_level = n
        else:
            self.spaces_per_indent_level = 4

    def setIndentWithTabs(self):
        self.indent_with_spaces = False

    def setNoDrawReturn(self):
        self.draw_return = False

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self.viewport())
        std_color = QColor("#bbbbbb")
        green_color = QColor("#88ff88")
        red_color = QColor("#ff8888")
        painter.setPen(std_color)
        painter.setFont(self.font())
        metrics = self.fontMetrics()
        symbol_height = metrics.height()

        block = self.firstVisibleBlock()
        top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())

        while block.isValid() and top <= self.viewport().height():
            text = block.text()
            block_rect = self.blockBoundingGeometry(block).translated(self.contentOffset())
            baseline_y = block_rect.top() + (metrics.lineSpacing() - symbol_height)/2 + metrics.ascent()


            if block.blockNumber() == 0 and self.n > 0 and not self.invert:
                painter.setPen(green_color)
            elif block.blockNumber() == 0 and self.n == 0 and self.invert:
                painter.setPen(red_color)
            else:
                painter.setPen(std_color)

            for i, ch in enumerate(text):
                cursor = self.textCursor()
                cursor.setPosition(block.position() + i)
                rect = self.cursorRect(cursor)

                if ch == " ":
                    if i > 0 and text[i-1] == " " or \
                        i < len(text)-1 and text[i+1] == " ":
                        painter.drawText(rect.x(), int(baseline_y), "·")
                if ch == "\t":
                    painter.drawText(rect.x(), int(baseline_y), "→")

                if i == self.n-1:
                    if self.invert:
                        painter.setPen(red_color)
                    else:
                        painter.setPen(std_color)

            if self.draw_return:
                cursor = self.textCursor()
                cursor.setPosition(block.position() + len(text))
                rect = self.cursorRect(cursor)
                painter.drawText(rect.x(),
                                    int(baseline_y), "↲")

            block = block.next()
            top = int(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())

        painter.end()

    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.AltModifier:
            if event.key() == Qt.Key.Key_Left:
                self.backPressed.emit()
                return
            elif event.key() == Qt.Key.Key_Right:
                self.forwardPressed.emit()
                return
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            self.enterPressed.emit()
            event.ignore()  # prevent newlines
        elif event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            if self.indent_with_spaces:
                tab = " " * self.spaces_per_indent_level
            else:
                tab = "\t"
            cursor.insertText(tab)
        elif event.key() == Qt.Key.Key_Backtab:  # Shift+Tab
            cursor = self.textCursor()
            pos = cursor.position()
            text = self.toPlainText()

            if pos > 0 and text[pos - 1] == "\t":
                # Delete tab before cursor
                cursor.deletePreviousChar()
                self.setTextCursor(cursor)
            elif text.startswith("\t"):
                # Delete leading tab
                cursor.setPosition(0)
                cursor.deleteChar()
                # Adjust caret one step back if it was after the deleted tab
                if pos > 0:
                    cursor.setPosition(pos - 1)
                self.setTextCursor(cursor)
            elif text.startswith(" "):
                if (g := re.match(r'^ +', text)):
                    spaces = g.group(0)
                    to_del = min(len(spaces), self.spaces_per_indent_level)
                    cursor.setPosition(0)
                    cursor.setPosition(to_del, cursor.MoveMode.KeepAnchor)
                    cursor.removeSelectedText()
        elif event.key() in (Qt.Key.Key_Up, Qt.Key.Key_Down, Qt.Key.Key_PageUp, Qt.Key.Key_PageDown):
            return
        else:
            super().keyPressEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() != 0:
            event.ignore()
        else:
            super().wheelEvent(event)