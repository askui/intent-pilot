import time
from intent_pilot.utils.config import Config
from intent_pilot.utils.controller.controller import Controller

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
                f"[controller] Objective Completed "
            )
            print(
                f"[controller] Summary {summary}"
            )
            return True

        else:
            print(
                f"[Controller-2command][Error] unknown operation response :("
            )
            print(
                f"[Controller-2command][Error] AI response {operation}"
            )
            return True

        print(
            f"[Controller-2command][Operate] Thought  {operate_thought}"
        )
        print(
            f"[Controller-2command][Operate] {operate_type}  {operate_detail}"
        )

    return False