from textual import on
from textual.app import App
from textual.widgets import Header, Footer, Static, Button, Input, Markdown

class SecureChatApp(App):

    md = """
    #header
    this is some markdown my friend

    **hello bold**












hello

        """

    CSS_PATH = "./frontend.css"
    BINDINGS = [
        ("d", "toggle_dark", "Toggles dark mode"), # textual looks for methods that have the action_ prefix (action_toggle_dark is a built in function)
    ]

    def compose(self): # where you put all the visible functions of the app
        yield Header(show_clock=True, name="LocalChat")
        yield Markdown(self.md)
        yield Input(placeholder="Insert prompt here")
        yield Footer()

if __name__ == "__main__":
    app = SecureChatApp()
    app.run()
