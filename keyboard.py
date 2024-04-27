import ctypes
import subprocess
import time
import sdl2

class Keyboard:
    def __init__(self):
        # SDL_SetHint(SDL_HINT_JOYSTICK_ALLOW_BACKGROUND_EVENTS, b"1")
        sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING)
        self.devices = {}

    def update(self):
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
            pass
            # if event.type == sdl2.SDL_KEYDOWN:
            #     device = sdl2.SDL_JoystickOpen(event.jdevice.which)
            #     id = sdl2.SDL_JoystickGetDeviceInstanceID(event.jdevice.which)
            #     self.devices[id] = device
                # print(F"joy added: {id}, {SDL_JoystickName(device)}, {SDL_JoystickGetVendor(device)}")
            # elif event.type == SDL_JOYDEVICEREMOVED:
            #     if (id := event.jdevice.which) in self.devices:
            #         SDL_JoystickClose(self.devices[id])
            #         del self.devices[id]
            #         # print(F"joy removed: {id}")
            # elif event.type == SDL_JOYBUTTONUP:
            #     # print("joy button up!")
            #     subprocess.run([REWASD_COMMAND_LINE_EXE,
            #                     "apply", "--id", CONTROLLER_DEVICE_ID, "--path", REWASD_CONFIG, "--slot", F"slot{REWASD_SLOT}"])
    def get_keyboard_state(self):
        numkeys = ctypes.c_int()
        keystate = sdl2.keyboard.SDL_GetKeyboardState(ctypes.byref(numkeys))
        ptr_t = ctypes.POINTER(ctypes.c_uint8 * numkeys.value)        
        return ctypes.cast(keystate, ptr_t)[0]

if __name__ == "__main__":
    kb = Keyboard()
    while True:
        kb.update()
        keystatus = kb.get_keyboard_state()
        for k in keystatus:
            if k:
                print(F"the {k} key is pressed")
        # if keystatus[sdl2.SDL_SCANCODE_W]:
        #     print("the w key was pressed")
        time.sleep(0.01)