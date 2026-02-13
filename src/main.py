from chat_display import ChatDisplay
from interface import OllamaInterface

from textual import on, work
from pathlib import Path
from textual.app import App
from textual.widgets import Header, Input, Markdown, Static, LoadingIndicator
from textual.containers import ScrollableContainer

CONTEXT_WINDOW = 80
SYSTEM_PROMPT = """You are a helpful and concise AI Assistant. You are currently running inside a Terminal User Interface (TUI) built with the Textual framework.

In the conversation history provided:
- The human is identified as "User:".
- You are identified as "Assistant:".

Rules for your responses:
1. ALWAYS adhere to the "Assistant:" persona. Never refer to yourself as "System" or "AI".
2. Use Markdown for structure. Use bolding for emphasis and code blocks for any technical snippets.
3. Be concise. Terminal screens have limited space; avoid unnecessary "fluff" or long introductory sentences.
4. If the user asks for code, provide it in a way that is easy to read in a terminal environment.
5. Do not include your own label "Assistant:" in the text of your response; the UI handles the labeling."
            """


class LocalChat(App):
    CSS_PATH = "./frontend.css"
    BINDINGS = []

    def on_mount(self) -> None:
        self.interface = OllamaInterface("gemma3:4b", "http://localhost:11434/api/generate")
        self.system_prompt = SYSTEM_PROMPT
        self.chat_history = []
        self.context = ""

    def compose(self): # visible components of the application
        yield Header(name="LocalChat", show_clock=True) 
        yield ScrollableContainer(id="container")
        yield Input(placeholder="Waiting for prompt...", id="inp")

    @on(Input.Submitted) 
    def write_user_input(self, event: Input.Submitted):
        if (event.value == ""): return # disregard empty chats

        self.update_history(event.value, "User")

        user_input = "\n".join(self.chat_history[-CONTEXT_WINDOW:])
        input = self.query_one("#inp", Input)
        input.clear() # clears the input widget

        chat_container = self.query_one("#container")

        user_chat = Markdown(markdown=event.value, classes="user")
        chat_container.mount(user_chat)
        user_chat.scroll_visible() # scroll so new chat is visible

        self.run_model_query(user_input)

    @work(thread=True) # signals func to run on a new thread 
    def run_model_query(self, user_input: str) -> None:
        response = str(self.interface.query_model(prompt=user_input, stream=False))
        
        self.update_history("Assistant: ", response)
        self.call_from_thread(self.display_response, response)

    def display_response(self, text: str) -> None:
        chat_container = self.query_one("#container")
        model_chat = Markdown(markdown=text, classes="model")
        chat_container.mount(model_chat)
        model_chat.scroll_visible()

    def update_history(self, role : str, chat : str):
        out = f"\n{role}: {chat}"
        self.chat_history.append(out)
        self.context += out
        if len(self.context) > CONTEXT_WINDOW:
            self.context = self.context[:-CONTEXT_WINDOW]

if __name__ == "__main__":
    app = LocalChat()
    app.run()
