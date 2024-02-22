import platform
import subprocess

from plyer import notification

from intent_pilot.utils.terminal import ANSI_BLUE, ANSI_RESET


def show_notification(title, message):
    try:
        if platform.system() == "Darwin":
            subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'display notification "{message}" with title "{title}"',
                ]
            )
        else:
            notification.notify(
                title=title,
                message=message,
                app_name="Intent Pilot",
                timeout=10,  # Duration in seconds the notification stays
            )
    except Exception as _:
        print(
            f"{ANSI_BLUE} [Intent Pilot][show_notification] Message: {message} {ANSI_RESET}"
        )
