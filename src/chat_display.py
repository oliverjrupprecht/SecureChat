import os

#../tmp/chat_history.md

class ChatDisplay():
    def __init__(self, tmp_location : str, model_name : str, user_name : str):
        self.tmp_location = tmp_location
        self.model_name = model_name
        self.user_name = user_name

        if os.path.exists(tmp_location): # if file from prev session exists then delete it
            os.remove(self.tmp_location)

        with open(self.tmp_location, "w") as f:
            f.write("Beginning chat...")

    def add_user_chat(self, prompt : str):
        with open(self.tmp_location, "a") as f:
            f.write(f"\n{self.user_name}: {prompt}\n")

    def add_model_chat(self):
        pass

if __name__ == "__main__":
    cd = ChatDisplay("../tmp/chat_history.md", "gemma", "ollie")
    cd.add_user_chat("hello this is a prompt to the chat file")
    cd.add_user_chat("this is another")
