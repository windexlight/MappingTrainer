import os
from enum import Enum
from typing import Any, Optional, Type, TypeVar
from pathlib import Path
from PyQt5.QtCore import QSettings, QStandardPaths, QByteArray

T = TypeVar("T")


class Section(Enum):
    LINES = "LINES"
    FONT_SIZES = "FONT_SIZES"
    FLAGS = "FLAGS"
    MODE = "MODE"
    WINDOWS = "WINDOWS"

class FontSizesKey(Enum):
    KeyPracticeSize = "KeyPracticeSize"
    TypingSize = "TypingSize"
    CodeSize = "CodeSize"

class FlagsKey(Enum):
    SerifFont = "SerifFont"
    RandomLocation = "RandomLocation"
    SkipQuote = "SkipQuote"
    KeyPractice_Combos = "KeyPractice_Combos"
    KeyPractice_Function = "KeyPractice_Function"
    KeyPractice_Lowercase = "KeyPractice_Lowercase"
    KeyPractice_Modifiers = "KeyPractice_Modifiers"
    KeyPractice_Numbers = "KeyPractice_Numbers"
    KeyPractice_Specials = "KeyPractice_Specials"
    KeyPractice_Symbols = "KeyPractice_Symbols"
    KeyPractice_Uppercase = "KeyPractice_Uppercase"

class ModeKey(Enum):
    Mode = "Mode"
    Filename = "Filename"

class ModeValue(Enum):
    Key_Practice = "Key_Practice"
    Typing_Practice = "Typing_Practice"
    Words_Top_10 = "Words_Top_10"
    Words_Top_100 = "Words_Top_100"
    Words_Top_1000 = "Words_Top_1000"
    Words_All = "Words_All"

DEFAULTS = {
    Section.FONT_SIZES: {
        FontSizesKey.KeyPracticeSize: 22,
        FontSizesKey.TypingSize: 12,
        FontSizesKey.CodeSize: 12,
    },
    Section.FLAGS: {
        FlagsKey.SerifFont: True,
        FlagsKey.RandomLocation: False,
        FlagsKey.SkipQuote: False,
        FlagsKey.KeyPractice_Combos: True,
        FlagsKey.KeyPractice_Function: True,
        FlagsKey.KeyPractice_Lowercase: True,
        FlagsKey.KeyPractice_Modifiers: True,
        FlagsKey.KeyPractice_Numbers: True,
        FlagsKey.KeyPractice_Specials: True,
        FlagsKey.KeyPractice_Symbols: True,
        FlagsKey.KeyPractice_Uppercase: True,
    },
    Section.MODE: {
        ModeKey.Mode: ModeValue.Key_Practice.value,
        ModeKey.Filename: "",
    },
}


class Settings:
    def __init__(self):
        config_dir = Path(QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation))
        config_dir = config_dir
        config_dir.mkdir(parents=True, exist_ok=True)
        self._path = config_dir / "settings.ini"

        self._settings = QSettings(str(self._path), QSettings.IniFormat)
        self._settings.setFallbacksEnabled(False)

        self._ensure_defaults()

        self.font_sizes = _FontSizesSection(self)
        self.flags = _FlagsSection(self)
        self.mode = _ModeSection(self)
        self.lines = _LinesSection(self)
        self.windows = _WindowsSection(self)

    def _ensure_defaults(self) -> None:
        for section, keys in DEFAULTS.items():
            for key, value in keys.items():
                path = f"{section.value}/{key.value}"
                if self._settings.value(path, None) is None:
                    self._settings.setValue(path, value)

    def get(
        self,
        section: Section,
        key: Any,
        *,
        value_type: Type[T],
        default: Optional[Any] = None,
    ) -> T:
        if default is None:
            default = DEFAULTS.get(section, {}).get(key)
        if isinstance(key, Enum):
            key = key.value
        if not isinstance(key, str):
            key = str(key)
        raw = self._settings.value(f"{section.value}/{key}", default)

        try:
            if raw is None:
                return default

            if value_type is bool:
                return str(raw).lower() in ("1", "true", "yes", "on")
            elif value_type in (int, float, str):
                return value_type(raw)
            elif value_type is QByteArray:
                if isinstance(raw, QByteArray):
                    return raw
                return QByteArray()
            else:
                return raw
        except:
            return default

    def set(self, section: Section, key: Any, value: Any) -> None:
        if isinstance(key, Enum):
            key = key.value
        if not isinstance(key, str):
            key = str(key)
        self._settings.setValue(f"{section.value}/{key}", value)

    def reset_to_defaults(self) -> None:
        self._settings.clear()
        self._ensure_defaults()

    def path(self) -> str:
        return str(self._path)


class _FontSizesSection:
    def __init__(self, parent: Settings):
        self._p = parent

    @property
    def KeyPracticeSize(self) -> int:
        return self._p.get(Section.FONT_SIZES, FontSizesKey.KeyPracticeSize, value_type=int)

    @KeyPracticeSize.setter
    def KeyPracticeSize(self, v: int):
        self._p.set(Section.FONT_SIZES, FontSizesKey.KeyPracticeSize, v)

    @property
    def TypingSize(self) -> int:
        return self._p.get(Section.FONT_SIZES, FontSizesKey.TypingSize, value_type=int)

    @TypingSize.setter
    def TypingSize(self, v: int):
        self._p.set(Section.FONT_SIZES, FontSizesKey.TypingSize, v)

    @property
    def CodeSize(self) -> int:
        return self._p.get(Section.FONT_SIZES, FontSizesKey.CodeSize, value_type=int)

    @CodeSize.setter
    def CodeSize(self, v: int):
        self._p.set(Section.FONT_SIZES, FontSizesKey.CodeSize, v)


class _FlagsSection:
    def __init__(self, parent: Settings):
        self._p = parent
        self._section = Section.FLAGS

    @property
    def SerifFont(self) -> bool:
        return self._p.get(self._section, FlagsKey.SerifFont, value_type=bool)

    @SerifFont.setter
    def SerifFont(self, value: bool):
        self._p.set(self._section, FlagsKey.SerifFont, value)

    @property
    def RandomLocation(self) -> bool:
        return self._p.get(self._section, FlagsKey.RandomLocation, value_type=bool)

    @RandomLocation.setter
    def RandomLocation(self, value: bool):
        self._p.set(self._section, FlagsKey.RandomLocation, value)

    @property
    def SkipQuote(self) -> bool:
        return self._p.get(self._section, FlagsKey.SkipQuote, value_type=bool)

    @SkipQuote.setter
    def SkipQuote(self, value: bool):
        self._p.set(self._section, FlagsKey.SkipQuote, value)

    @property
    def KeyPractice_Combos(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Combos, value_type=bool)

    @KeyPractice_Combos.setter
    def KeyPractice_Combos(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Combos, value)

    @property
    def KeyPractice_Function(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Function, value_type=bool)

    @KeyPractice_Function.setter
    def KeyPractice_Function(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Function, value)

    @property
    def KeyPractice_Lowercase(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Lowercase, value_type=bool)

    @KeyPractice_Lowercase.setter
    def KeyPractice_Lowercase(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Lowercase, value)

    @property
    def KeyPractice_Modifiers(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Modifiers, value_type=bool)

    @KeyPractice_Modifiers.setter
    def KeyPractice_Modifiers(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Modifiers, value)

    @property
    def KeyPractice_Numbers(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Numbers, value_type=bool)

    @KeyPractice_Numbers.setter
    def KeyPractice_Numbers(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Numbers, value)

    @property
    def KeyPractice_Specials(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Specials, value_type=bool)

    @KeyPractice_Specials.setter
    def KeyPractice_Specials(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Specials, value)

    @property
    def KeyPractice_Symbols(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Symbols, value_type=bool)

    @KeyPractice_Symbols.setter
    def KeyPractice_Symbols(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Symbols, value)

    @property
    def KeyPractice_Uppercase(self) -> bool:
        return self._p.get(self._section, FlagsKey.KeyPractice_Uppercase, value_type=bool)

    @KeyPractice_Uppercase.setter
    def KeyPractice_Uppercase(self, value: bool):
        self._p.set(self._section, FlagsKey.KeyPractice_Uppercase, value)


class _ModeSection:
    def __init__(self, parent: Settings):
        self._p = parent
        self._section = Section.MODE

    @property
    def Mode(self) -> ModeValue:
        default = DEFAULTS[Section.MODE][ModeKey.Mode]
        value_str = self._p.get(self._section, ModeKey.Mode, default=default, value_type=str)
        try:
            return ModeValue(value_str)
        except:
            return ModeValue(default)

    @Mode.setter
    def Mode(self, value: ModeValue):
        self._p.set(self._section, ModeKey.Mode, value.value)

    @property
    def Filename(self) -> str:
        return self._p.get(Section.MODE, ModeKey.Filename, value_type=str)

    @Filename.setter
    def Filename(self, v: str):
        self._p.set(Section.MODE, ModeKey.Filename, v)


class _LinesSection:
    def __init__(self, parent: Settings):
        self._p = parent
        self._section = Section.LINES

    def __getitem__(self, key: str) -> int:
        return self._p.get(self._section, key, default=0, value_type=int)

    def __setitem__(self, key: str, value: int) -> None:
        self._p.set(self._section, key, value)


class _WindowsSection:
    def __init__(self, parent: Settings):
        self._p = parent
        self._section = Section.WINDOWS

    @property
    def Main(self) -> QByteArray:
        value = self._p.get(self._section, "Main", default=QByteArray(), value_type=QByteArray)
        return value

    @Main.setter
    def Main(self, geometry: QByteArray):
        self._p.set(self._section, "Main", geometry)
