
import os, json
from typing import Dict, Any
from openai import OpenAI

def _client() -> OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Falta OPENAI_API_KEY")
    return OpenAI(api_key=key)

def chat_json(system: str, user: str, model: str) -> Dict[str, Any]:
    cli = _client()
    resp = cli.chat.completions.create(
        model=model,
        temperature=0.7,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}],
        response_format={"type":"json_object"}
    )
    content = resp.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        s, e = content.find("{"), content.rfind("}")
        if s!=-1 and e!=-1 and e>s:
            return json.loads(content[s:e+1])
        raise RuntimeError("Modelo não devolveu JSON válido.")
