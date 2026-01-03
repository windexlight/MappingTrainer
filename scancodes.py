from enum import Enum, auto

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
    # Mute = 0x700 # Here down are totally made up values, just to fill out ones I want from keycodes
    # VolUp = auto()
    # VolDown = auto()
    # NextTrack = auto()
    # PrevTrack = auto()
    # Stop = auto()
    # PlayPause = auto()
    BrightUp = 0x700 #auto()
    BrightDown = auto()
    Mute = 0x120
    VolUp = 0x130
    VolDown = 0x12E
    NextTrack = 0x119
    PrevTrack = 0x110
    Stop = 0x124
    PlayPause = 0x122

scancodeSet = set(item.value for item in scancode)

scancodeTranslations = {
    scancode.RShift: scancode.LShift,
    scancode.RCtrl: scancode.LCtrl,
    scancode.RAlt: scancode.LAlt,
    scancode.RWin: scancode.LWin,
}

def processScancode(k) -> scancode | None:
    if k in scancodeSet:
        k = scancode(k)
        if k in scancodeTranslations:
            k = scancodeTranslations[k]
        return k
    
SCANCODE_MODS = [scancode.LCtrl, scancode.LShift, scancode.LAlt, scancode.LWin]
