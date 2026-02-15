import utils.ollama_client as client

from textual import on, work
from textual.app import App
from textual.widgets import Header, Input, Markdown, Static, LoadingIndicator
from textual.containers import ScrollableContainer

from utils.get_system_prompt import get_system_prompt

CONTEXT_WINDOW = 80
MODEL = "gemma3:4b"
API_URL = "http://localhost:11434/api/generate"

class LocalChat(App):
    CSS_PATH = "./utils/frontend.css"
    BINDINGS = []

    def on_mount(self) -> None:
        self.chat_history = []
        client.load_model(MODEL, API_URL)
        loader = self.query_one("#loader", LoadingIndicator)
        loader.display = False 


    def compose(self): # visible components of the application
        yield Header(name="LocalChat", show_clock=True) 
        yield ScrollableContainer(id="container")
        yield Input(placeholder="Waiting for prompt...", id="inp")
        yield LoadingIndicator(id="loader")

    @on(Input.Submitted) 
    def write_user_input(self, event: Input.Submitted):
        if (event.value == ""): return # disregard empty chats

        self.chat_history.append(f"\nUser: {event.value}")

        user_input = get_system_prompt() + "".join(self.chat_history[-CONTEXT_WINDOW:])

        input = self.query_one("#inp", Input)
        input.clear() # clears the input widget
        #input.display = False

        loader = self.query_one("#loader", LoadingIndicator)
        loader.display = True

        chat_container = self.query_one("#container")

        user_chat = Markdown(markdown=event.value, classes="user")
        chat_container.mount(user_chat)
        user_chat.scroll_visible() # scroll so new chat is visible

        self.run_model_query(user_input)

    @work(thread=True) # signals func to run on a new thread 
    def run_model_query(self, user_input: str) -> None:
        response = str(client.query_model(MODEL, API_URL, user_input, is_stream=False))
        
        self.call_from_thread(self.display_response_and_update_history, response)

    def display_response_and_update_history(self, text: str) -> None:
        loader = self.query_one("#loader")
        loader.display = False

        #input = self.query_one("#inp")
        #input.display = True
        
        chat_container = self.query_one("#container")
        model_chat = Markdown(markdown=text, classes="model")
        chat_container.mount(model_chat)
        model_chat.scroll_visible()

        self.chat_history.append(f"Assistant: {text}")

if __name__ == "__main__":
    app = LocalChat()
    app.run()
