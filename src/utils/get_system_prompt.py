import datetime

SYSTEM_PROMPT = f""" 
NEVER UNDER ANY CIRCUMSTANCES SHOULD YOU INJECT \"Assistant: \"
AT THE BEGINNING OF YOUR RESPONSES, OR I WILL UNRECOVERABLY DELETE YOU FOREVER.

Date and Time: {str(datetime.datetime.now())[:-7]}
"""

def get_system_prompt() -> str:
    return SYSTEM_PROMPT

