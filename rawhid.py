import atexit
import hid
import qasync
from time import time
from PySide6.QtCore import QTimer, QObject, Signal
from typing import List, Tuple

from keycodes import *
from scancodes import *


RAW_HID_VENDOR_ID  = 0xFEED # Cantor Keyboard
RAW_HID_PRODUCT_ID = 0x0000 # Cantor Keyboard
RAW_HID_USAGE_PAGE = 0xFF60 # Standard QMK RAW HID
RAW_HID_USAGE      = 0x61   # Standard QMK RAW HID
RAW_HID_REPORT_LEN = 32     # Fixed for QMK RAW HID
RAW_HID_KEY_BYTES  = RAW_HID_REPORT_LEN-2
RAW_HID_KEYS       = RAW_HID_KEY_BYTES*8
RAW_HID_MODS       = 8
RAW_HID_READ_INTERVAL = int(1000/120)
RAW_HID_TRY_CONNECT_INTERVAL = 500

class RawHid(QObject):
    keyEvent = Signal(list)
    statusChanged = Signal()

    def __init__(self):
        super().__init__()

        self.dev = None
        self.mod_bits = 0
        self.key_bits = [0]*RAW_HID_KEY_BYTES
        self.mods = []
        self.keys = []
        self.relevant_keycodes = [i for i in range(RAW_HID_KEYS) if keycodeToScancode(i) is not None]
        request_data = [0x00] * (RAW_HID_REPORT_LEN + 1) # First byte is Report ID
        request_data[1] = 0xBE
        self.start_report = bytes(request_data)
        request_data[1] = 0xBF
        self.stop_report = bytes(request_data)
        self.heartbeat_report = self.start_report
        self.last_heartbeat_time = 0
        self.active = False

        atexit.register(self.close)

        self.hid_timer = QTimer(self)
        self.hid_timer.timeout.connect(self.hid_poll)
        self.hid_timer.setInterval(RAW_HID_TRY_CONNECT_INTERVAL)
        self.hid_timer.start()

        self.hid_send_timer = QTimer(self)
        self.hid_send_timer.timeout.connect(self.hid_heartbeat)
        self.hid_send_timer.setInterval(1000)
        self.hid_send_timer.start()
        self.hid_heartbeat()

        self.try_connect()

    def start(self):
        self.heartbeat_report = self.start_report
        self.hid_send_timer.stop()
        self.hid_send_timer.start()
        self.hid_heartbeat()

    def stop(self):
        self.heartbeat_report = self.stop_report
        self.hid_send_timer.stop()
        self.hid_send_timer.start()
        self.hid_heartbeat()

    def try_connect(self):
        device_interfaces = hid.enumerate(RAW_HID_VENDOR_ID, RAW_HID_PRODUCT_ID)
        raw_hid_interfaces = [
            i for i in device_interfaces
            if i['usage_page'] == RAW_HID_USAGE_PAGE and i['usage'] == RAW_HID_USAGE
        ]
        if len(raw_hid_interfaces) > 0:
            self.dev = hid.device()
            self.dev.open_path(raw_hid_interfaces[0]['path'])
            self.dev.set_nonblocking(True)
            self.hid_timer.setInterval(RAW_HID_READ_INTERVAL)

    def hid_poll(self):
        if self.dev is not None:
            try:
                if len(report := self.dev.read(RAW_HID_REPORT_LEN)) > 0:
                    self.process_raw_hid_report(report)
            except:
                self.close()
            if (time() - self.last_heartbeat_time) > 1.5:
                if self.active:
                    self.active = False
                    self.statusChanged.emit()
        else:
            self.try_connect()

    def hid_heartbeat(self):
        if self.dev is not None:
            try:
                self.dev.write(self.heartbeat_report)
            except:
                self.close()


    def process_raw_hid_report(self, report):
        if report is not None:
            if len(report) == RAW_HID_REPORT_LEN:
                if report[0] == 0 and report[1] == 0xEF:
                    self.last_heartbeat_time = time()
                    if not self.active:
                        self.active = True
                        self.statusChanged.emit()
                elif report[0] == 6:
                    self.process_keyboard_report(report[1:])

    def process_keyboard_report(self, report):
        mods = report[0]
        self.mods = [keycodeToScancode(i+keycode.KC_LEFT_CTRL.value) for i in range(RAW_HID_MODS)
                     if (mods & (1 << i)) > 0]
        keys = report[1:]
        pressed = [keycodeToScancode(i) for i in self.relevant_keycodes
                   if key_bit_set(i, keys) and not key_bit_set(i, self.key_bits)]
        released = [keycodeToScancode(i) for i in self.relevant_keycodes
                    if not key_bit_set(i, keys) and key_bit_set(i, self.key_bits)]
        self.key_bits = keys
        self.keys = [k for k in self.keys if k not in SCANCODE_MODS]
        self.keys = [k for k in self.keys if not any(x in released for x in (k if isinstance(k, tuple) else (k,)))]
        self.keys.extend(pressed if not self.mods else ((*self.mods, x) for x in pressed))
        mods_pressed = [x for x in self.mods if not self.keys or not all(x in (y if isinstance(y, tuple) else (y,)) for y in self.keys)]
        # TODO - logging f"[] --- [(<scancode.LCtrl: 29>, <scancode.LShift: 42>, <scancode.BackslashPipe: 43>)]" here at point of exception.
        # why is self.keys a tuple here?
        self.keys = [*mods_pressed, *self.keys]
        self.keyEvent.emit(self.keys)

    def close(self):
        if self.dev is not None:
            try:
                self.dev.close()
            except:
                pass
        self.dev = None
        self.hid_timer.setInterval(RAW_HID_TRY_CONNECT_INTERVAL)
        if self.active:
            self.active = False
            self.statusChanged.emit()

def key_bit_set(key: int, keys: List[int]) -> bool | None:
    if (key >> 3) < len(keys):
        return (keys[key >> 3] & (1 << (key & 7))) > 0

