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
