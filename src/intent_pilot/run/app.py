import argparse
import time

from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import message_dialog

from langchain_core.messages import HumanMessage

from intent_pilot.utils.config import Config
from intent_pilot.utils.controller.thought2command import operate
from intent_pilot.utils.models.model_handler import call_gpt_4_vision_preview_labeled, call_ollama_vision_labeled
from intent_pilot.utils.models.prompts import get_system_prompt
from intent_pilot.utils.system_utils import show_notification
from intent_pilot.utils.terminal import ANSI_BLUE, ANSI_RED, ANSI_RESET, get_user_input
import traceback

from enum import StrEnum
class Models(StrEnum):
    GPTV4 = "gpt4v"
    LLAVA = "llava"

def get_args():
    parser = argparse.ArgumentParser(description="Intent-Pilot")
    parser.add_argument("--debug", action="store_true", help="Enable verbose mode")
    parser.add_argument('-m', '--model', type=str, default="gpt4v", help='Enter a model: llava or gpt4v (default: gpt4v)')

    args = parser.parse_args()
    return args

def main():
    args = get_args()
    message_dialog(
        title="Intent-Pilot",
        text="An AskUI open source initiative to automate computer operations.",
    ).run()
    config = Config()
    config.verbose = args.debug

    config.initialize_askui()

    if (
        not config.is_user_config_exists()
        and prompt("Do you want to save the config user? y/n: \n") == "y"
    ):
        config.save_config()

    config.model = args.model

    client = None
    if config.model == Models.GPTV4:
        client = config.initialize_openai()
        print(f"{ANSI_BLUE} [Intent Pilot] Using model {Models.GPTV4}")
    elif config.model == Models.LLAVA:
        client = config.initialize_ollama()
        print(f"{ANSI_BLUE} [Intent Pilot] Using model {Models.LLAVA}")
    else:
        raise ValueError(f"We do not support this model: {config.model}")

    objective = get_user_input()
    messages = []
    if config.model == Models.GPTV4:
        system_prompt = get_system_prompt("gpt-4-with-som", objective)
        system_message = {"role": "system", "content": system_prompt}
        messages.append(system_message)
    elif config.model == Models.LLAVA:
        system_prompt = get_system_prompt("ollama", objective)
        system_message = HumanMessage(content=system_prompt)
        messages.append(system_message)

    exception_count = 0
    step = 0
    operations = []
    while True:
        print(f"{ANSI_BLUE} [Intent Pilot] Step  {step} {ANSI_RESET}")
        step += 1
        if step > 20:
            print(
                f"{ANSI_RED}[Intent Pilot]  {step} steps are completed.. Quitting... {ANSI_RESET}"
            )
            break
        try:
            if config.model == Models.GPTV4:
                operations = call_gpt_4_vision_preview_labeled(
                    client, messages, skip_som_draw_labels=["text"]
                )  # skip labels some
            elif config.model == Models.LLAVA:
                operations = call_ollama_vision_labeled(
                    client, messages, skip_som_draw_labels=["text"]
                )
        except Exception as e:
            exception_count += 1
            print(f"{ANSI_RED}[Intent Pilot][Operate] error {e}{ANSI_RESET}")
            if config.verbose:
                traceback.print_exc()
            if exception_count >= 2:
                break;
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
