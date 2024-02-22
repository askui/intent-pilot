import platform
import subprocess

import pyautogui
from PIL import ImageGrab


def capture_screen_with_cursor(file_path):
    user_platform = platform.system()

    if user_platform == "Windows":
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)
    elif user_platform == "Linux":
        import Xlib.display  # global import causes issues on windows
        import Xlib.X

        # Using xlib to prevent scrot dependency for Linux
        screen = Xlib.display.Display().screen()
        size = screen.width_in_pixels, screen.height_in_pixels
        screenshot = ImageGrab.grab(bbox=(0, 0, size[0], size[1]))
        screenshot.save(file_path)
    elif user_platform == "Darwin":  # (Mac OS)
        # Use the screencapture utility to capture the screen with the cursor
        subprocess.run(["screencapture", "-C", file_path])
    else:

        print(
            f"The platform you're using ({user_platform}) is unfortunately not currently supported"
        )
