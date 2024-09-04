from . import write as hid_write

# With this declaration a data packet must be sent as:
# byte 1   -> "Contact count"        (always == 1)
# byte 2   -> "Contact identifier"   (any value)
# byte 3   -> "Tip Switch" state     (bit 0 = Tip Switch up/down, bit 1 = In Range)
# byte 4,5 -> Absolute X coordinate  (0...10000)
# byte 6,7 -> Absolute Y coordinate  (0...10000)
# Example:
# Touch x:75%, y:50%
# echo -ne "\x01\x00\x01\x4c\x1d\x88\x13" > /dev/hidg3;
# sleep .1;
# echo -ne "\x01\x00\x00\x4c\x1d\x88\x13" > /dev/hidg3
def send_touch_event(touch_path, x = 0, y = 0, tip_switch = 0):
    buf = [
        1,                # Contact count (always == 1)
        0,                # Contact identifier (any value)
        tip_switch,       # Tip Switch state (bit 0 = Tip Switch up/down, bit 1 = In Range)
        x & 0xFF,         # Low-byte of X coordinate (0..10000)
        (x >> 8) & 0xFF,  # High-byte of X coordinate
        y & 0xFF,         # Low-byte of Y coordinate (0..10000)
        (y >> 8) & 0xFF   # High-byte of Y coordinate
    ]
    hid_write.write_to_hid_interface(touch_path, buf)
