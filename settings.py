from PySide6.QtCore import QSettings, QStandardPaths, QByteArray
from enum import Enum
from pathlib import Path
from typing import Any, Type, Protocol, Union
from dataclasses import dataclass, fields
import re
import hashlib
from pygments.lexers import get_lexer_by_name
import detect_code_info

class Section:
    _settings: QSettings | None = None
    _section_name: str | None = None
    _loaded = False
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if not self._loaded or not self._settings or not self._section_name or name.startswith("_"):
            return
        key = f"{self._section_name}/{name}"
        if isinstance(value, Enum):
            value = value.name
        self._settings.setValue(key, value)


class ModeValue(Enum):
    Key_Practice = "Key_Practice"
    Typing_Practice = "Typing_Practice"
    Words_Top_10 = "Words_Top_10"
    Words_Top_100 = "Words_Top_100"
    Words_Top_1000 = "Words_Top_1000"
    Words_All = "Words_All"

class ModeSettings(Protocol):
    FontSize: int
    AdvanceOnEnter: bool
    AdvanceOnSpace: bool

class WindowGeometrySettings(Protocol):
    WindowGeometry: QByteArray


@dataclass
class typing(Section):
    WindowGeometry: QByteArray = QByteArray()
    FontSize: int = 14
    SerifFont: bool = True
    AdvanceOnEnter: bool = True
    AdvanceOnSpace: bool = True

@dataclass
class code(Section):
    FontSize: int = 12
    AdvanceOnEnter: bool = True
    AdvanceOnSpace: bool = False

@dataclass
class words(Section):
    WindowGeometry: QByteArray = QByteArray()
    FontSize: int = 18
    SerifFont: bool = True
    AdvanceOnEnter: bool = False
    AdvanceOnSpace: bool = False

@dataclass
class key_practice(Section):
    WindowGeometry: QByteArray = QByteArray()
    FontSize: int = 22
    Combos: bool = True
    Function: bool = True
    Lowercase: bool = True
    Modifiers: bool = True
    Numbers: bool = True
    Specials: bool = True
    Symbols: bool = True
    Uppercase: bool = True

@dataclass
class file(Section):
    Mode: ModeValue = ModeValue.Key_Practice
    Filename: str | None = None
    Sha256: str | None = None

@dataclass
class FileSettings(Section):
    Line: int = 0
    IsCode: bool = False
    CodeLanguage: str | None = None
    IndentType: detect_code_info.IndentType | None = None
    IndentSize: int | None = None


class Settings:
    def __init__(self):
        config_dir = Path(QStandardPaths.writableLocation(QStandardPaths.StandardLocation.AppConfigLocation))
        config_dir.mkdir(parents=True, exist_ok=True)
        self._path = config_dir / "settings.ini"
        self._settings = QSettings(str(self._path), QSettings.Format.IniFormat)
        self._settings.setFallbacksEnabled(False)

        # self.font_sizes = self._load(font_sizes)
        self.typing = self._load(typing)
        self.code = self._load(code)
        self.words = self._load(words)
        self.file = self._load(file)
        self.key_practice = self._load(key_practice)
        # self.windows = self._load(windows)

        self._file_settings = {}
        for section in self._settings.childGroups():
            if re.fullmatch(r'.+_[a-f0-9]{64}', section):
                self._file_settings[section] = self._load(FileSettings, section)

    @property
    def file_settings(self) -> FileSettings:
        if not self.file.Filename:
            return FileSettings()
        if self.file.Sha256 is None:
            raise Exception()
        if (key := f"{Path(self.file.Filename).name}_{str.lower(self.file.Sha256)}") not in self._file_settings:
            fs = FileSettings()
            fs._settings = self._settings
            fs._section_name = key
            fs._loaded = True
            self._file_settings[key] = fs
        return self._file_settings[key]
    
    def have_file(self, path: str, sha256: str) -> bool:
        return f"{Path(path).name}_{str.lower(sha256)}" in self._file_settings
    
    @property
    def code_info(self) -> detect_code_info.CodeInfo:
        ret = detect_code_info.CodeInfo()
        fs = self.file_settings
        try:
            if fs.CodeLanguage is None:
                raise Exception()
            lexer = get_lexer_by_name(fs.CodeLanguage)
        except:
            return ret
        ret.is_code = fs.IsCode
        ret.language = fs.CodeLanguage or None
        ret.indent_type = fs.IndentType or None
        ret.indent_size = fs.IndentSize or None
        ret.lexer = lexer
        return ret
    
    def set_code_info(self, code_info: detect_code_info.CodeInfo):
        fs = self.file_settings
        fs.IsCode = code_info.is_code
        fs.CodeLanguage = code_info.language if code_info.language is not None else ""
        fs.IndentType = code_info.indent_type
        fs.IndentSize = code_info.indent_size

    @property
    def mode_settings(self) -> ModeSettings:
        if self.file.Mode in (ModeValue.Typing_Practice, ModeValue.Key_Practice):
            if self.file_settings.IsCode:
                return self.code
            else:
                return self.typing
        else:
            return self.words
        
    @property
    def window_geometry(self) -> WindowGeometrySettings:
        if self.file.Mode == ModeValue.Key_Practice:
            return self.key_practice
        elif self.file.Mode == ModeValue.Typing_Practice:
            return self.typing
        else:
            return self.words
        
    @property
    def serif_font(self) -> Union[bool, None]:
        if self.file.Mode == ModeValue.Typing_Practice:
            if not self.file_settings.IsCode:
                return self.typing.SerifFont
        elif self.file.Mode != ModeValue.Key_Practice:
            return self.words.SerifFont

    @serif_font.setter
    def serif_font(self, value: bool):
        if self.file.Mode == ModeValue.Typing_Practice:
            if not self.file_settings.IsCode:
                self.typing.SerifFont = value
        elif self.file.Mode != ModeValue.Key_Practice:
            self.words.SerifFont = value

    def _load(self, cls, section_name = None):
        if not section_name:
            section_name = str.upper(cls.__name__)
        obj = cls()
        obj._settings = self._settings
        obj._section_name = section_name
        for f in fields(cls):
            key = f"{section_name}/{f.name}"
            if (raw := self._settings.value(key, None)) is not None:
                try:
                    value = self._convert_value(raw, f.type, getattr(obj, f.name))
                    setattr(obj, f.name, value)
                    continue
                except:
                    pass
            if isinstance(value := getattr(obj, f.name), Enum):
                value = value.value
            self._settings.setValue(key, value)
        obj._loaded = True
        return obj

    def _convert_value(self, raw, typ, default):
        try:
            if raw == "":
                return None
            elif issubclass(typ, Enum):
                return typ[raw]
            elif typ is QByteArray:
                if isinstance(raw, QByteArray) and raw.size() < 1024:
                    return raw
                return QByteArray()
            elif typ is bool:
                return str(raw).lower() in ("1", "true", "yes", "on")
            else:
                return typ(raw)
        except Exception:
            return default
