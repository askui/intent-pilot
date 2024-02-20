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

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.styles import Style

# Validator to ensure the input is not empty
class NonEmptyValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(message="This input cannot be empty. Please provide a value.",
                                  cursor_position=len(text))

# Style for the prompts
style = Style([
    ('qmark', 'fg:#5F819D bold'),    # Question mark style
    ('question', 'bold'),            # Question text style
    ('answer', 'fg:#FF9D00 bold'),   # Answer text style
    ('instruction', 'fg:#FF9D00'),   # Instruction text style
    ('error', 'fg:#FF0000'),         # Error message style
])

def get_env_values(variable_names):
    env_values = {}
    for var in variable_names:
        prompt_text = [
            ('class:qmark', '(?) '),
            ('class:question', f'Please enter the value for {var}: '),
            ('class:instruction', ' (cannot be empty)'),
        ]
        # Apply NonEmptyValidator to ensure input is not empty
        value = prompt(prompt_text, validator=NonEmptyValidator(), style=style)
        env_values[var] = value
    return env_values
