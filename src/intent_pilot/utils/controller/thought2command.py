import time
from intent_pilot.utils.config import Config
from intent_pilot.utils.controller.controller import Controller
from intent_pilot.utils.terminal import ANSI_BLUE, ANSI_RESET, ANSI_BRIGHT_GREEN, ANSI_RED

config = Config()
operating_system = Controller()

def operate(operations):
    for operation in operations:
        # wait one second
        time.sleep(1)
        operate_type = operation.get("operation").lower() # make a pydantic model for this
        operate_thought = operation.get("thought")
        operate_detail = ""

        if operate_type == "press" or operate_type == "hotkey":
            keys = operation.get("keys")
            operate_detail = keys
            operating_system.press(keys)
        elif operate_type == "write":
            content = operation.get("content")
            operate_detail = content
            operating_system.write(content)
        elif operate_type == "click":
            x = operation.get("x")
            y = operation.get("y")
            click_detail = {"x": x, "y": y}
            operate_detail = click_detail

            operating_system.mouse(click_detail)
        elif operate_type == "done":
            summary = operation.get("summary")
            print(
                f"{ANSI_BRIGHT_GREEN} [controller] Objective Completed \n\n{summary} {ANSI_RESET}"
            )
            return True

        else:
            print(
                f"{ANSI_RED} [Controller-2command][Error] unknown operation response :( \n\n  AI response: {operation} {ANSI_RESET}"
            )
            return True

        print(
            f"{ANSI_BRIGHT_GREEN}[Controller-2command][Operate] Thought  {operate_thought} {ANSI_RESET}"
        )
        print(
            f"{ANSI_BRIGHT_GREEN} [Controller-2command][Operate] {operate_type}  {operate_detail} {ANSI_RESET}"
        )

    return False