
import os
from openai import OpenAI

def _client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key: raise RuntimeError("Falta OPENAI_API_KEY")
    return OpenAI(api_key=key)

def generate_image_b64(prompt: str, size: str="1024x1024") -> str:
    cli = _client()
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")
    r = cli.images.generate(model=model, prompt=prompt, size=size)
    return r.data[0].b64_json
