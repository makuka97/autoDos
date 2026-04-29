"""Test 8BitDo button registration via XInput."""
import ctypes
import ctypes.wintypes
import time

xinput = ctypes.windll.xinput1_4

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ("wButtons",       ctypes.wintypes.WORD),
        ("bLeftTrigger",   ctypes.c_ubyte),
        ("bRightTrigger",  ctypes.c_ubyte),
        ("sThumbLX",       ctypes.c_short),
        ("sThumbLY",       ctypes.c_short),
        ("sThumbRX",       ctypes.c_short),
        ("sThumbRY",       ctypes.c_short),
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ("dwPacketNumber", ctypes.wintypes.DWORD),
        ("Gamepad",        XINPUT_GAMEPAD),
    ]

BUTTON_NAMES = {
    0x0001: "D-Pad Up",
    0x0002: "D-Pad Down",
    0x0004: "D-Pad Left",
    0x0008: "D-Pad Right",
    0x0010: "Start",
    0x0020: "Back/Select",
    0x0040: "Left Stick Click",
    0x0080: "Right Stick Click",
    0x0100: "Left Bumper (LB)",
    0x0200: "Right Bumper (RB)",
    0x1000: "A",
    0x2000: "B",
    0x4000: "X",
    0x8000: "Y",
}

AXIS_DEADZONE = 8000

print("Controller button tester — press buttons and move sticks")
print("Press Ctrl+C to quit\n")

prev_buttons = 0
prev_lt = 0
prev_rt = 0

state = XINPUT_STATE()

while True:
    result = xinput.XInputGetState(0, ctypes.byref(state))
    if result != 0:
        print("Controller disconnected!")
        break

    gp = state.Gamepad
    buttons = gp.wButtons

    # Check buttons
    for mask, name in BUTTON_NAMES.items():
        was_pressed = prev_buttons & mask
        is_pressed  = buttons & mask
        if is_pressed and not was_pressed:
            print(f"  PRESSED:  {name}  (mask={hex(mask)})")
        elif not is_pressed and was_pressed:
            print(f"  released: {name}")

    # Check triggers
    if gp.bLeftTrigger > 50 and prev_lt <= 50:
        print(f"  PRESSED:  Left Trigger  (value={gp.bLeftTrigger})")
    if gp.bLeftTrigger <= 50 and prev_lt > 50:
        print(f"  released: Left Trigger")
    if gp.bRightTrigger > 50 and prev_rt <= 50:
        print(f"  PRESSED:  Right Trigger  (value={gp.bRightTrigger})")
    if gp.bRightTrigger <= 50 and prev_rt > 50:
        print(f"  released: Right Trigger")

    # Check sticks (only report when crossing deadzone)
    lx = gp.sThumbLX
    ly = gp.sThumbLY
    rx = gp.sThumbRX
    ry = gp.sThumbRY

    if abs(lx) > AXIS_DEADZONE or abs(ly) > AXIS_DEADZONE:
        direction = ""
        if ly > AXIS_DEADZONE:  direction += "UP "
        if ly < -AXIS_DEADZONE: direction += "DOWN "
        if lx < -AXIS_DEADZONE: direction += "LEFT "
        if lx > AXIS_DEADZONE:  direction += "RIGHT "
        if direction:
            print(f"  Left Stick: {direction.strip()}")

    if abs(rx) > AXIS_DEADZONE or abs(ry) > AXIS_DEADZONE:
        direction = ""
        if ry > AXIS_DEADZONE:  direction += "UP "
        if ry < -AXIS_DEADZONE: direction += "DOWN "
        if rx < -AXIS_DEADZONE: direction += "LEFT "
        if rx > AXIS_DEADZONE:  direction += "RIGHT "
        if direction:
            print(f"  Right Stick: {direction.strip()}")

    prev_buttons = buttons
    prev_lt      = gp.bLeftTrigger
    prev_rt      = gp.bRightTrigger

    time.sleep(0.02)