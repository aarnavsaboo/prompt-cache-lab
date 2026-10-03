from time import perf_counter
from urllib.request import Request, urlopen
import json


def generate(model: str, prompt: str, endpoint: str = "http://127.0.0.1:11434", keep_alive: str = "10m"):
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        "options": {"num_predict": 64},
    }).encode()
    req = Request(endpoint.rstrip("/") + "/api/generate", data=payload,
                  headers={"Content-Type": "application/json"}, method="POST")
    started = perf_counter()
    with urlopen(req, timeout=600) as response:
        row = json.load(response)
    row["client_seconds"] = perf_counter() - started
    return row
