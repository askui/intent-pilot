import pyautogui
import time
import math
import pyautogui
import time
import math
import platform
import pyperclip

os_name = platform.system()


class Controller:
    def write(self, content):
        try:
            content = content.replace("\\n", "\n")
            pyperclip.copy(content)
            if os_name == "Darwin":
                self.press(["command", "v"])
            else:
                self.press(["ctrl", "v"])
                time.sleep(0.05)
        except Exception as e:
            print("[Controller][write] error:", e)

    def press(self, keys):
        try:
            for key in keys:
                pyautogui.keyDown(key)
            time.sleep(0.1)
            for key in keys:
                pyautogui.keyUp(key)
        except Exception as e:
            print("[Controller][press] error:", e)

    def mouse(self, click_detail):
        try:
            x = click_detail.get("x")
            y = click_detail.get("y")

            if click_detail and isinstance(x, float) and isinstance(y, float):
                self.click(x, y)

        except Exception as e:
            print("[Controller][mouse] error:", e)

    def click(
        self,
        x_pixel,
        y_pixel,
        duration=0.2,
        circle_radius=50,
        circle_duration=0.5,
    ):
        try:
            pyautogui.moveTo(x_pixel, y_pixel, duration=duration)
            start_time = time.time()
            while time.time() - start_time < circle_duration:
                angle = ((time.time() - start_time) / circle_duration) * 2 * math.pi
                x = x_pixel + math.cos(angle) * circle_radius
                y = y_pixel + math.sin(angle) * circle_radius
                pyautogui.moveTo(x, y, duration=0.1)

            pyautogui.click(x_pixel, y_pixel)
        except Exception as e:
            print("[Controller][click_at_percentage] error:", e)

    def click_at_percentage(
        self,
        x_percentage,
        y_percentage,
        duration=0.2,
        circle_radius=50,
        circle_duration=0.5,
    ):
        try:
            screen_width, screen_height = pyautogui.size()
            x_pixel = int(screen_width * float(x_percentage))
            y_pixel = int(screen_height * float(y_percentage))

            pyautogui.moveTo(x_pixel, y_pixel, duration=duration)

            start_time = time.time()
            while time.time() - start_time < circle_duration:
                angle = ((time.time() - start_time) / circle_duration) * 2 * math.pi
                x = x_pixel + math.cos(angle) * circle_radius
                y = y_pixel + math.sin(angle) * circle_radius
                pyautogui.moveTo(x, y, duration=0.1)

            pyautogui.click(x_pixel, y_pixel)
        except Exception as e:
            print("[Controller][click_at_percentage] error:", e)
