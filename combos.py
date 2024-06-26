from scancodes import *

numbers = [
    [scancode.OneExclam],
    [scancode.TwoAt],
    [scancode.ThreePound],
    [scancode.FourDollar],
    [scancode.FivePercent],
    [scancode.SixCaret],
    [scancode.SevenAmpersand],
    [scancode.EightAsterisk],
    [scancode.NineLeftParen],
    [scancode.ZeroRightParen],
]

symbols = [
    [scancode.BacktickTilde],
    [scancode.MinusUnderscore],
    [scancode.EqualPlus],
    [scancode.LeftSquareBracket],
    [scancode.RightSquareBracket],
    [scancode.BackslashPipe],
    [scancode.SemicolonColon],
    [scancode.SingleDoubleQuote],
    [scancode.CommaLeftAngle],
    [scancode.PeriodRightAngle],
    [scancode.SlashQuestion],
    [scancode.LShift, scancode.CommaLeftAngle],
    [scancode.LShift, scancode.PeriodRightAngle],
    [scancode.LShift, scancode.SlashQuestion],
    [scancode.LShift, scancode.BacktickTilde],
    [scancode.LShift, scancode.OneExclam],
    [scancode.LShift, scancode.TwoAt],
    [scancode.LShift, scancode.ThreePound],
    [scancode.LShift, scancode.FourDollar],
    [scancode.LShift, scancode.FivePercent],
    [scancode.LShift, scancode.SixCaret],
    [scancode.LShift, scancode.SevenAmpersand],
    [scancode.LShift, scancode.EightAsterisk],
    [scancode.LShift, scancode.NineLeftParen],
    [scancode.LShift, scancode.ZeroRightParen],
    [scancode.LShift, scancode.MinusUnderscore],
    [scancode.LShift, scancode.EqualPlus],
    [scancode.LShift, scancode.LeftSquareBracket],
    [scancode.LShift, scancode.RightSquareBracket],
    [scancode.LShift, scancode.BackslashPipe],
    [scancode.LShift, scancode.SemicolonColon],
    [scancode.LShift, scancode.SingleDoubleQuote],
]

specials = [
    [scancode.Backspace],
    [scancode.Tab],
    [scancode.Enter],
    [scancode.Space],
    [scancode.Delete],
    [scancode.Home],
    [scancode.End],
    [scancode.PgUp],
    [scancode.PgDn],
    [scancode.Left],
    [scancode.Up],
    [scancode.Down],
    [scancode.Right],
    [scancode.Esc],
    # [scancode.CapsLock],
    # [scancode.nonUS1],
    # [scancode.Insert],
    # [scancode.NumLock],
    # [scancode.KP7Home],
    # [scancode.KP4Left],
    # [scancode.KP1End],
    # [scancode.KPSlash],
    # [scancode.KP8Up],
    # [scancode.KP5],
    # [scancode.KP2Down],
    # [scancode.KP0Ins],
    # [scancode.KPAsterisk],
    # [scancode.KP9PgUp],
    # [scancode.KP6Right],
    # [scancode.KP3PgDn],
    # [scancode.KPPeriodDel],
    # [scancode.KPMinus],
    # [scancode.KPPlus],
    # [scancode.KPEnter],
    # [scancode.PrtScr],
    # [scancode.AltSysRq],
    # [scancode.ScrollLock],
    # [scancode.CtrlBreak],
    # [scancode.Menu],
    # [scancode.Sleep],
    # [scancode.Power],
    # [scancode.Wake],
]

modifiers = [
    [scancode.LShift],
    [scancode.LCtrl],
    [scancode.LAlt],
    # [scancode.LWin],
    # [scancode.RWin],
    # [scancode.RShift],
    # [scancode.RAlt],
    # [scancode.RCtrl],
]

lowercase = [
    [scancode.Q],
    [scancode.W],
    [scancode.E],
    [scancode.R],
    [scancode.T],
    [scancode.Y],
    [scancode.U],
    [scancode.I],
    [scancode.O],
    [scancode.P],
    [scancode.A],
    [scancode.S],
    [scancode.D],
    [scancode.F],
    [scancode.G],
    [scancode.H],
    [scancode.J],
    [scancode.K],
    [scancode.L],
    [scancode.Z],
    [scancode.X],
    [scancode.C],
    [scancode.V],
    [scancode.B],
    [scancode.N],
    [scancode.M],
]

uppercase = [
    [scancode.LShift, scancode.Q],
    [scancode.LShift, scancode.W],
    [scancode.LShift, scancode.E],
    [scancode.LShift, scancode.R],
    [scancode.LShift, scancode.T],
    [scancode.LShift, scancode.Y],
    [scancode.LShift, scancode.U],
    [scancode.LShift, scancode.I],
    [scancode.LShift, scancode.O],
    [scancode.LShift, scancode.P],
    [scancode.LShift, scancode.A],
    [scancode.LShift, scancode.S],
    [scancode.LShift, scancode.D],
    [scancode.LShift, scancode.F],
    [scancode.LShift, scancode.G],
    [scancode.LShift, scancode.H],
    [scancode.LShift, scancode.J],
    [scancode.LShift, scancode.K],
    [scancode.LShift, scancode.L],
    [scancode.LShift, scancode.Z],
    [scancode.LShift, scancode.X],
    [scancode.LShift, scancode.C],
    [scancode.LShift, scancode.V],
    [scancode.LShift, scancode.B],
    [scancode.LShift, scancode.N],
    [scancode.LShift, scancode.M],
]

function = [
    [scancode.F1],
    [scancode.F2],
    [scancode.F3],
    [scancode.F4],
    [scancode.F5],
    [scancode.F6],
    [scancode.F7],
    [scancode.F8],
    [scancode.F9],
    [scancode.F10],
    [scancode.F11],
    [scancode.F12],
]

combos = [
    [scancode.LCtrl, scancode.C],
    [scancode.LCtrl, scancode.V],
    [scancode.LCtrl, scancode.X],
    [scancode.LCtrl, scancode.Z],
    [scancode.LCtrl, scancode.Y],
    [scancode.LCtrl, scancode.A],
    [scancode.LCtrl, scancode.O],
    [scancode.LCtrl, scancode.S],
    [scancode.LCtrl, scancode.F],
]