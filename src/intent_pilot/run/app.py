from intent_pilot.utils.config import Config
from intent_pilot.utils.models.prompts import get_system_prompt
from intent_pilot.utils.models.model_handler import call_gpt_4_vision_preview_labeled
from intent_pilot.utils.controller.thought2command import operate
from intent_pilot.utils.system_utils import show_notification
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

style = Style.from_dict({
    'prompt': 'ansicyan bold',
    'input': 'ansiwhite',
})

def get_user_input():
    user_input = prompt('Enter your prompt: ',
                        style=style,
                        prompt_continuation='# ',  # Used when input spans multiple lines
                        wrap_lines=False,          # Prevent automatic line wrapping
                        )
    return user_input


config = Config()

def main():
    message_dialog(
    title="Intent-Pilot",
    text="An AskUI initiative to automate computer operations.",
    ).run()
    model = "gpt-4-with-som"
    objective = get_user_input()
    system_prompt = get_system_prompt(model, objective)
    system_message = {"role": "system", "content": system_prompt}
    messages = [system_message]
    
    client = config.initialize_openai()
    while True:
        print("*" * 50)
        operations = call_gpt_4_vision_preview_labeled(client, messages, objective)
        show_notification("intent-pilot",f"Thought: {operations[-1]['thought']}")
        is_task_achieved = operate(operations)
        print("*" * 50)
        if is_task_achieved:
            show_notification("intent-pilot",f"Thought: Task Completed. {operations[-1]['summary']}")
            print("HURRAY!")
            return
        else:
            print("More to do ....")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Error")
        show_notification("intent-pilot",f"Error - {str(e)}")