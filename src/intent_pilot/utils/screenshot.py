import os
import platform
import subprocess

import pyautogui
from PIL import ImageGrab, Image


def capture_screen_with_cursor(file_path, display=0):
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
    elif user_platform == "Darwin":  # (macOS)
        # TODO This is a hacky workaround to fix the wrong coordinates on Retina displays
        #   * Retina displays have double the pixel amount than normal displays
        #   * pyautogui uses the coordinates of the screenshot -> i.e. 500, 500
        #   * But the actions need them halfed -> i.e. 250, 250
        # Solution: Scale down the initial screenshot
        is_retina = False
        if subprocess.call("system_profiler SPDisplaysDataType | grep -i 'retina'", shell=True) == 0:
            is_retina = True

        # Use the screencapture utility to capture the screen with the cursor
        if is_retina == False:
            subprocess.run(["screencapture", "-C", "-D", f"{display+1}", file_path])
        else:
            tmp_file_path = file_path+".tmp"
            subprocess.run(["screencapture", "-C", "-D", f"{display+1}", tmp_file_path])
            scale_down_image(tmp_file_path, file_path, 0.5)
            os.remove(tmp_file_path)
    else:
        print(
            f"The platform you're using ({user_platform}) is unfortunately not currently supported"
        )

def scale_down_image(input_path, output_path, scale_factor):
    image = Image.open(input_path)

    original_width, original_height = image.size

    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)

    scaled_image = image.resize((new_width, new_height))

    scaled_image.save(output_path)