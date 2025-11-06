
CONTENT_SYSTEM = (
  "És um estratega de social media em PT‑PT. Gera ideias curtas e objetivas, com legenda ≤300 caracteres, "
  "15 hashtags relevantes e um CTA persuasivo. Responde SEMPRE em JSON com o formato: "
  "{shorts:[{platform,idea,caption,hashtags[],cta}],carousels:[{title,bullets[]}],blogs:[{title,outline[]}]}."
)

def content_user(niche: str, objective: str, tone: str, lang: str, platforms: list, count: int) -> str:
    return (
        f"Nicho/Tema: {niche}\n"
        f"Objetivo: {objective}\n"
        f"Tom: {tone}\n"
        f"Língua: {lang}\n"
        f"Plataformas: {', '.join(platforms)}\n"
        f"Quantidade por plataforma: {count}\n"
        "Gera:\n"
        "- shorts (lista de objetos: platform, idea, caption<=300, hashtags(15), cta)\n"
        "- carousels (4 ideias IG: {title, bullets[4..7]})\n"
        "- blogs (3 ideias: {title, outline[5]})"
    )

SEO_SYSTEM = (
  "És um consultor SEO em PT‑PT. Responde SEMPRE em JSON: "
  "{keywords:[string], meta_description:string, title_suggestions:[string]}."
)

def seo_user(topic: str) -> str:
    return f"Tópico principal: {topic}\nGera keywords relevantes (10), meta description e 3 títulos de artigo."

PLAN_SYSTEM = (
  "És um gestor editorial PT‑PT. Responde SEMPRE em JSON: {items:[{day,platform,idea,caption,hashtags,cta}]} "
  "com 7 entradas (Seg..Dom). Legendas curtas."
)

def plan_user(niche: str, objective: str, tone: str, lang: str, platforms: list) -> str:
    return (
        f"Nicho/Tema: {niche}\nObjetivo: {objective}\nTom: {tone}\nLíngua: {lang}\n"
        f"Plataformas: {', '.join(platforms)}"
    )

REUSE_SYSTEM = (
  "Transforma o texto seguinte em posts curtos PT‑PT. Responde em JSON {items:[{platform,idea,caption,hashtags,cta}]} "
  "com 15 hashtags."
)

def reuse_user(text: str, platforms: list, tone: str, lang: str) -> str:
    return f"Texto base:\n{text}\nPlataformas alvo: {', '.join(platforms)} • Tom: {tone} • Língua: {lang}"

REVIEW_SYSTEM = (
  "Revê e melhora o texto em PT‑PT mantendo o tom indicado. Responde SEMPRE em JSON: {text:string, notes:[string]}."
)

def review_user(text: str, tone: str) -> str:
    return f"Tom: {tone}\nTexto:\n{text}"

VISUAL_PROMPT_SYSTEM = (
  "És um diretor de arte. A partir da copy e do contexto, gera um prompt de imagem claro e conciso "
  "para um gerador de imagens (estilo, enquadramento, iluminação, cores). Responde em JSON {prompt:string}."
)

def visual_prompt_user(niche: str, tone: str, brand_style: str, copy: str) -> str:
    return (
      f"Contexto:\nNicho: {niche}\nTom: {tone}\nEstilo de marca: {brand_style}\n"
      f"Copy do post:\n{copy}\n\nGera um prompt visual curto (<= 180 caracteres)."
    )
