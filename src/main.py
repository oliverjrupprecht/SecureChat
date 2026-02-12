from chat_display import ChatDisplay
from interface import OllamaInterface

from textual import on
from pathlib import Path
from textual.app import App
from textual.widgets import Header, Input, Markdown

class SecureChatApp(App):
    MARKDOWN_PATH =  Path(__file__).parent / "../tmp/chat_history.md" 
    CSS_PATH = "./frontend.css"
    BINDINGS = []

    def on_mount(self) -> None:
            self.chat_logger = ChatDisplay("../tmp/chat_history.md", "model", "ollie")
            self.llm_interface = OllamaInterface("gemma3:4b", "http://localhost:11434/api/generate")

            self.update_content() 
            self.set_interval(1, self.update_content) # updates md viewer periodically

    def compose(self): # where you put all the visible functions of the app
        yield Header(show_clock=True, name="LocalChat")
        yield Markdown(id="md")
        yield Input(placeholder="Insert prompt here", id="inp")

    def update_content(self) -> None:
        content = self.MARKDOWN_PATH.read_text()
        markdown_widget = self.query_one("#md", Markdown) # grab the widget
        markdown_widget.update(content)

    @on(Input.Submitted)
    async def write_input(self, event: Input.Submitted):
        self.chat_logger.add_user_chat(event.value)

        inp = self.query_one("#inp", Input)
        inp.clear()

        self.chat_logger.add_model_header()
        async for chunk in self.llm_interface.send_prompt(event.value, True):
            self.chat_logger.add_model_chat(chunk)


if __name__ == "__main__":
    app = SecureChatApp()
    app.run()
