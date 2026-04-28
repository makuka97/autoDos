import ctypes
import ctypes.wintypes

xinput = ctypes.windll.xinput1_4

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons", ctypes.wintypes.WORD),
        ("bLeftTrigger", ctypes.c_ubyte),
        ("bRightTrigger", ctypes.c_ubyte),
        ("sThumbLX", ctypes.c_short),
        ("sThumbLY", ctypes.c_short),
        ("sThumbRX", ctypes.c_short),
        ("sThumbRY", ctypes.c_short),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", ctypes.wintypes.DWORD),
        ("Gamepad", XINPUT_GAMEPAD),
    ]

state = XINPUT_STATE()
result = xinput.XInputGetState(0, ctypes.byref(state))
if result == 0:
    print("Controller found!")
    print("Buttons:", state.Gamepad.wButtons)
else:
    print("No controller on port 0, error:", result)