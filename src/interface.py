import json
import requests

# URL = "http://localhost:11434/api/generate"
# MODEL = "gemma3:4b"

class OllamaInterface():
    def __init__(self, model, url):
        self.MODEL = model
        self.URL = url
        self.load_model()

    def load_model(self):
        payload = {
                "model": self.MODEL,
                "keep_alive" : -1
        }

        response = requests.post(self.URL, json=payload)

        if not response.ok:
            raise Exception(f"{self.MODEL} could not be loaded")

    def unload_model(self):
        payload = {
                "model": self.MODEL,
                "keep_alive": 0
        }

        response = requests.post(self.URL, json=payload)

        if not response.ok:
            raise Exception(f"{self.MODEL} could not be unloaded")

    def send_prompt(self, prompt : str, stream : bool):
        payload = {
          "model": self.MODEL,
          "prompt": prompt,
          "stream": stream
        }

        if stream:
            return self.__handle_stream(payload)
        else:
            return self.__handle_block(payload)
           
    def __handle_stream(self, payload):
        with requests.post(self.URL, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line.decode('utf-8')) # each line needs to be decodes with utf-8 dict (internet standart encoding)
                    yield chunk.get("response", "") # yeild the response token

    def __handle_block(self, payload) -> str:
        response = requests.post(self.URL, json=payload)

        if response.ok:
            js = json.loads(response.content)
            return js.get("response", "")
        else:
            raise Exception("bad request")

