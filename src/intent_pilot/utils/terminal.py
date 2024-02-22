import os
import platform
import sys

from prompt_toolkit import prompt
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import ValidationError, Validator

style = Style.from_dict(
    {
        "prompt": "ansicyan bold",
        "input": "ansiwhite",
    }
)


def get_user_input():
    user_input = prompt(
        "Enter your prompt: ",
        style=style,
        prompt_continuation="# ",  # Used when input spans multiple lines
        wrap_lines=False,  # Prevent automatic line wrapping
    )
    return user_input


# Validator to ensure the input is not empty
class NonEmptyValidator(Validator):
    def validate(self, document):
        text = document.text.strip()
        if not text:
            raise ValidationError(
                message="This input cannot be empty. Please provide a value.",
                cursor_position=len(text),
            )


# Style for the prompts
style = Style(
    [
        ("qmark", "fg:#5F819D bold"),  # Question mark style
        ("question", "bold"),  # Question text style
        ("answer", "fg:#FF9D00 bold"),  # Answer text style
        ("instruction", "fg:#FF9D00"),  # Instruction text style
        ("error", "fg:#FF0000"),  # Error message style
    ]
)


def get_env_values(variable_names):
    env_values = {}
    for var in variable_names:
        prompt_text = [
            ("class:qmark", "(?) "),
            ("class:question", f"Please enter the value for {var}: "),
            ("class:instruction", " (cannot be empty)"),
        ]
        # Apply NonEmptyValidator to ensure input is not empty
        value = prompt(prompt_text, validator=NonEmptyValidator(), style=style)
        env_values[var] = value
    return env_values


# Check if on a windows terminal that supports ANSI escape codes
def supports_ansi():
    """
    Check if the terminal supports ANSI escape codes
    """
    plat = platform.system()
    supported_platform = plat != "Windows" or "ANSICON" in os.environ
    is_a_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    return supported_platform and is_a_tty


# Define ANSI color codes
ANSI_GREEN = "\033[32m" if supports_ansi() else ""  # Standard green text
ANSI_BRIGHT_GREEN = "\033[92m" if supports_ansi() else ""  # Bright/bold green text
ANSI_RESET = "\033[0m" if supports_ansi() else ""  # Reset to default text color
ANSI_CYAN = "\033[36m" if supports_ansi() else ""  # Standard cyan text
ANSI_MAGENTA = "\033[35m" if supports_ansi() else ""  # Standard magenta text
ANSI_BLUE = "\033[94m" if supports_ansi() else ""  # Bright blue
ANSI_YELLOW = "\033[33m" if supports_ansi() else ""  # Standard yellow text
ANSI_RED = "\033[31m" if supports_ansi() else ""
ANSI_BRIGHT_MAGENTA = "\033[95m" if supports_ansi() else ""  # Bright magenta text
ANSI_BRIGHT_CYAN = "\033[96m" if supports_ansi() else ""  # Bright cyan text
ANSI_BRIGHT_WHITE = "\033[97m" if supports_ansi() else ""  # Bright white text
ANSI_BOLD = "\033[1m" if supports_ansi() else ""  # Bold text
ANSI_UNDERLINE = "\033[4m" if supports_ansi() else ""  # Underlined text
