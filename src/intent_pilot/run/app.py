import argparse
import time

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog

from intent_pilot.utils.config import Config
from intent_pilot.utils.controller.thought2command import operate
from intent_pilot.utils.models.model_handler import call_gpt_4_vision_preview_labeled
from intent_pilot.utils.models.prompts import get_system_prompt
from intent_pilot.utils.system_utils import show_notification
from intent_pilot.utils.terminal import ANSI_BLUE, ANSI_RED, ANSI_RESET, get_user_input


def get_args():
    parser = argparse.ArgumentParser(description="Intent-Pilot")
    parser.add_argument("--debug", action="store_true", help="Enable verbose mode")
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    message_dialog(
        title="Intent-Pilot",
        text="An AskUI open source initiative to automate computer operations.",
    ).run()
    model = "gpt-4-with-som"
    config = Config()
    config.verbose = args.debug

    client = None
    client = config.initialize_openai()

    config.initialize_askui()

    if (
        not config.is_user_config_exists()
        and prompt("Do you want to save the config user? y/n: \n") == "y"
    ):
        config.save_config()

    objective = get_user_input()
    system_prompt = get_system_prompt(model, objective)
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]

    step = 0
    while True:
        print(f"{ANSI_BLUE} [Intent Pilot] Step  {step} {ANSI_RESET}")
        step += 1
        if step > 20:
            print(
                f"{ANSI_RED}[Intent Pilot]  {step} steps are completed.. Quitting... {ANSI_RESET}"
            )
            break
        try:
            operations = call_gpt_4_vision_preview_labeled(
                client, messages, skip_som_draw_labels=["text"]
            )  # skip labels some
        except Exception as e:
            if config.verbose:
                print(f"{ANSI_RED}[Intent Pilot][Operate] error {e}{ANSI_RESET}")
            continue

        show_notification("intent-pilot", f"Thought: {operations[-1]['thought']}")
        is_task_achieved = operate(operations)
        time.sleep(1)
        print("*" * 50)
        if is_task_achieved:
            show_notification(
                "intent-pilot", f"Thought: Task Completed. {operations[-1]['summary']}"
            )
            print("HURRAY!")
            break
        else:
            print("More to do ....")


if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print("Error")
        show_notification("intent-pilot", f"Error - {str(err)}")
        raise err
