import json
import requests

def load_model(model : str, url : str):
    payload = {
            "model": model,
            "keep_alive" : "5m"
    }

    response = requests.post(url, json=payload)

    if not response.ok:
        raise Exception(f"{model} could not be loaded")

def unload_model(model : str, url : str):
    payload = {
            "model": model,
            "keep_alive": 0
    }

    response = requests.post(url, json=payload)

    if not response.ok:
        raise Exception(f"{model} could not be unloaded")

def query_model(model : str, url: str, prompt : str, is_stream : bool = False):
    payload = {
      "model": model,
      "prompt": prompt,
      "stream": is_stream
    }

    if is_stream:
        return handle_stream(url, payload)
    else:
        return handle_block(url, payload)
       
def handle_stream(url : str, payload : dict):
    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line.decode('utf-8')) # each line needs to be decodes with utf-8 dict (internet standart encoding)
                yield chunk.get("response", "") # yield the response token

def handle_block(url : str, payload : dict) -> str:
    response = requests.post(url, json=payload)

    if response.ok:
        js = json.loads(response.content)
        return js.get("response", "")
    else:
        raise Exception("bad request")
