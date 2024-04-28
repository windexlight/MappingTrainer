from enum import Enum

class scancode(Enum):
    BacktickTilde = 0x29
    OneExclam = 0x02
    TwoAt = 0x03
    ThreePound = 0x04
    FourDollar = 0x05
    FivePercent = 0x06
    SixCaret = 0x07
    SevenAmpersand = 0x08
    EightAsterisk = 0x09
    NineLeftParen = 0x0a
    ZeroRightParen = 0x0b
    MinusUnderscore = 0x0c
    EqualPlus = 0x0d
    Backspace = 0x0e
    Tab = 0x0f
    Q = 0x10
    W = 0x11
    E = 0x12
    R = 0x13
    T = 0x14
    Y = 0x15
    U = 0x16
    I = 0x17
    O = 0x18
    P = 0x19
    LeftSquareBracket = 0x1a
    RightSquareBracket = 0x1b
    BackslashPipe = 0x2b
    CapsLock = 0x3a
    A = 0x1e
    S = 0x1f
    D = 0x20
    F = 0x21
    G = 0x22
    H = 0x23
    J = 0x24
    K = 0x25
    L = 0x26
    SemicolonColon = 0x27
    SingleDoubleQuote = 0x28
    nonUS1 = 0xff
    Enter = 0x1c
    LShift = 0x2a
    Z = 0x2c
    X = 0x2d
    C = 0x2e
    V = 0x2f
    B = 0x30
    N = 0x31
    M = 0x32
    CommaLeftAngle = 0x33
    PeriodRightAngle = 0x34
    SlashQuestion = 0x35
    RShift = 0x36
    LCtrl = 0x1d
    LAlt = 0x38
    Space = 0x39
    RAlt = 0x138
    RCtrl = 0x11d
    Insert = 0x152
    Delete = 0x153
    Home = 0x147
    End = 0x14f
    PgUp = 0x149
    PgDn = 0x151
    Left = 0x14b
    Up = 0x148
    Down = 0x150
    Right = 0x14d
    NumLock = 0x45
    KP7Home = 0x47
    KP4Left = 0x4b
    KP1End = 0x4f
    KPSlash = 0x135
    KP8Up = 0x48
    KP5 = 0x4c
    KP2Down = 0x50
    KP0Ins = 0x52
    KPAsterisk = 0x37
    KP9PgUp = 0x49
    KP6Right = 0x4d
    KP3PgDn = 0x51
    KPPeriodDel = 0x53
    KPMinus = 0x4a
    KPPlus = 0x4e
    KPEnter = 0x11c
    Esc = 0x01
    F1 = 0x3b
    F2 = 0x3c
    F3 = 0x3d
    F4 = 0x3e
    F5 = 0x3f
    F6 = 0x40
    F7 = 0x41
    F8 = 0x42
    F9 = 0x43
    F10 = 0x44
    F11 = 0x57
    F12 = 0x58
    PrtScr = 0x137
    AltSysRq = 0x54
    ScrollLock = 0x46
    CtrlBreak = 0x146
    LWin = 0x15b
    RWin = 0x15c
    Menu = 0x15d
    Sleep = 0x15f
    Power = 0x15e
    Wake = 0x163

scancodeSet = set(item.value for item in scancode)

scancodeTranslations = {
    scancode.RShift: scancode.LShift,
    scancode.RCtrl: scancode.LCtrl,
    scancode.RAlt: scancode.LAlt,
    scancode.RWin: scancode.LWin,
}

scancodeNames = {
    scancode.BacktickTilde: "`",
    scancode.OneExclam: "1",
    scancode.TwoAt: "2",
    scancode.ThreePound: "3",
    scancode.FourDollar: "4",
    scancode.FivePercent: "5",
    scancode.SixCaret: "6",
    scancode.SevenAmpersand: "7",
    scancode.EightAsterisk: "8",
    scancode.NineLeftParen: "9",
    scancode.ZeroRightParen: "0",
    scancode.MinusUnderscore: "-",
    scancode.EqualPlus: "=",

    (scancode.LShift, scancode.BacktickTilde): "~",
    (scancode.LShift, scancode.OneExclam): "!",
    (scancode.LShift, scancode.TwoAt): "@",
    (scancode.LShift, scancode.ThreePound): "#",
    (scancode.LShift, scancode.FourDollar): "$",
    (scancode.LShift, scancode.FivePercent): "%",
    (scancode.LShift, scancode.SixCaret): "^",
    (scancode.LShift, scancode.SevenAmpersand): "&",
    (scancode.LShift, scancode.EightAsterisk): "*",
    (scancode.LShift, scancode.NineLeftParen): "(",
    (scancode.LShift, scancode.ZeroRightParen): ")",
    (scancode.LShift, scancode.MinusUnderscore): "_",
    (scancode.LShift, scancode.EqualPlus): "+",

    scancode.Backspace: "Backspace",
    scancode.Tab: "Tab",

    scancode.Q: "q",
    scancode.W: "w",
    scancode.E: "e",
    scancode.R: "r",
    scancode.T: "t",
    scancode.Y: "y",
    scancode.U: "u",
    scancode.I: "i",
    scancode.O: "o",
    scancode.P: "p",
    scancode.LeftSquareBracket: "[",
    scancode.RightSquareBracket: "]",
    scancode.BackslashPipe: "\\",

    (scancode.LShift, scancode.Q): "Q",
    (scancode.LShift, scancode.W): "W",
    (scancode.LShift, scancode.E): "E",
    (scancode.LShift, scancode.R): "R",
    (scancode.LShift, scancode.T): "T",
    (scancode.LShift, scancode.Y): "Y",
    (scancode.LShift, scancode.U): "U",
    (scancode.LShift, scancode.I): "I",
    (scancode.LShift, scancode.O): "O",
    (scancode.LShift, scancode.P): "P",
    (scancode.LShift, scancode.LeftSquareBracket): "{",
    (scancode.LShift, scancode.RightSquareBracket): "}",
    (scancode.LShift, scancode.BackslashPipe): "|",

    scancode.CapsLock: "CapsLock",

    scancode.A: "a",
    scancode.S: "s",
    scancode.D: "d",
    scancode.F: "f",
    scancode.G: "g",
    scancode.H: "h",
    scancode.J: "j",
    scancode.K: "k",
    scancode.L: "l",
    scancode.SemicolonColon: ";",
    scancode.SingleDoubleQuote: "'",

    (scancode.LShift, scancode.A): "A",
    (scancode.LShift, scancode.S): "S",
    (scancode.LShift, scancode.D): "D",
    (scancode.LShift, scancode.F): "F",
    (scancode.LShift, scancode.G): "G",
    (scancode.LShift, scancode.H): "H",
    (scancode.LShift, scancode.J): "J",
    (scancode.LShift, scancode.K): "K",
    (scancode.LShift, scancode.L): "L",
    (scancode.LShift, scancode.SemicolonColon): ":",
    (scancode.LShift, scancode.SingleDoubleQuote): "\"",

    scancode.nonUS1: "non-US-1",
    scancode.Enter: "Enter",
    scancode.LShift: "Shift",

    scancode.Z: "z",
    scancode.X: "x",
    scancode.C: "c",
    scancode.V: "v",
    scancode.B: "b",
    scancode.N: "n",
    scancode.M: "m",
    scancode.CommaLeftAngle: ",",
    scancode.PeriodRightAngle: ".",
    scancode.SlashQuestion: "/",

    (scancode.LShift, scancode.Z): "Z",
    (scancode.LShift, scancode.X): "X",
    (scancode.LShift, scancode.C): "C",
    (scancode.LShift, scancode.V): "V",
    (scancode.LShift, scancode.B): "B",
    (scancode.LShift, scancode.N): "N",
    (scancode.LShift, scancode.M): "M",
    (scancode.LShift, scancode.CommaLeftAngle): "<",
    (scancode.LShift, scancode.PeriodRightAngle): ">",
    (scancode.LShift, scancode.SlashQuestion): "?",

    scancode.RShift: "RShift",
    scancode.LCtrl: "Ctrl",
    scancode.LAlt: "Alt",
    scancode.Space: "Space",
    scancode.RAlt: "RAlt",
    scancode.RCtrl: "RCtrl",
    scancode.Insert: "Insert",
    scancode.Delete: "Delete",
    scancode.Home: "Home",
    scancode.End: "End",
    scancode.PgUp: "PgUp",
    scancode.PgDn: "PgDn",
    scancode.Left: "Left",
    scancode.Up: "Up",
    scancode.Down: "Down",
    scancode.Right: "Right",
    scancode.NumLock: "NumLock",
    scancode.KP7Home: "KP-7 / Home",
    scancode.KP4Left: "KP-4 / Left",
    scancode.KP1End: "KP-1 / End",
    scancode.KPSlash: "KP-/",
    scancode.KP8Up: "KP-8 / Up",
    scancode.KP5: "KP-5",
    scancode.KP2Down: "KP-2 / Down",
    scancode.KP0Ins: "KP-0 / Ins",
    scancode.KPAsterisk: "KP-*",
    scancode.KP9PgUp: "KP-9 / PgUp",
    scancode.KP6Right: "KP-6 / Right",
    scancode.KP3PgDn: "KP-3 / PgDn",
    scancode.KPPeriodDel: "KP-. / Del",
    scancode.KPMinus: "KP--",
    scancode.KPPlus: "KP-+",
    scancode.KPEnter: "KP-Enter",
    scancode.Esc: "Esc",
    scancode.F1: "F1",
    scancode.F2: "F2",
    scancode.F3: "F3",
    scancode.F4: "F4",
    scancode.F5: "F5",
    scancode.F6: "F6",
    scancode.F7: "F7",
    scancode.F8: "F8",
    scancode.F9: "F9",
    scancode.F10: "F10",
    scancode.F11: "F11",
    scancode.F12: "F12",
    scancode.PrtScr: "PrtScr",
    scancode.AltSysRq: "AltSysRq",
    scancode.ScrollLock: "ScrollLock",
    scancode.CtrlBreak: "CtrlBreak",
    scancode.LWin: "Win",
    scancode.RWin: "RWin",
    scancode.Menu: "Menu",
    scancode.Sleep: "Sleep",
    scancode.Power: "Power",
    scancode.Wake: "Wake",
}

def processScancode(k) -> scancode:
    if k in scancodeSet:
        k = scancode(k)
        if k in scancodeTranslations:
            k = scancodeTranslations[k]
        return k