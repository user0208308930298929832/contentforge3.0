
import os, json, base64
from datetime import date
from typing import Dict, Any
import streamlit as st

from core.prompts import (
    CONTENT_SYSTEM, content_user,
    SEO_SYSTEM, seo_user,
    PLAN_SYSTEM, plan_user,
    REUSE_SYSTEM, reuse_user,
    REVIEW_SYSTEM, review_user,
    VISUAL_PROMPT_SYSTEM, visual_prompt_user
)
from services.generator import chat_json
from services.visual import generate_image_b64
from services.exporter import export_csv_bytes, export_txt_bytes, export_pdf_bytes
from ui.components import header, section_title, card

st.set_page_config(page_title="ContentForge 3.0+ — Client Ready Pro", layout="wide")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Session
if "user" not in st.session_state: st.session_state.user = None
if "credits" not in st.session_state: st.session_state.credits = 15
if "credit_day" not in st.session_state: st.session_state.credit_day = str(date.today())
if "contents" not in st.session_state: st.session_state.contents = None
if "plan" not in st.session_state: st.session_state.plan = []
if "seo" not in st.session_state: st.session_state.seo = None
if "visuals" not in st.session_state: st.session_state.visuals = []
if st.session_state.credit_day != str(date.today()):
    st.session_state.credits = 15
    st.session_state.credit_day = str(date.today())

def login_screen():
    st.markdown("<div style='text-align:center;margin-top:6vh'>", unsafe_allow_html=True)
    st.image("assets/logo.svg", width=220)
    st.markdown("#### O teu copiloto de marketing — Gera, planeia e otimiza conteúdo que vende.")
    email = st.text_input("Email (para sessão local)", key="email_input")
    name = st.text_input("Nome / Marca")
    if st.button("Entrar"):
        if not email or "@" not in email:
            st.error("Introduz um email válido.")
            return
        st.session_state.user = {"email": email.strip().lower(), "name": name or "Utilizador"}
        st.session_state.credits = 15
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

if not st.session_state.user:
    login_screen()
    st.stop()

header("assets/logo.svg", "ContentForge 3.0+ — Client Ready Pro", st.session_state.credits)
st.caption(f"Olá, **{st.session_state.user['name']}** — modelo: **{MODEL}** • sessão local (sem base de dados).")

with st.sidebar:
    st.markdown("#### Parâmetros")
    niche = st.text_input("Nicho/Tema", "fitness")
    objective = st.selectbox("Objetivo", ["atrair", "vender", "educar", "inspirar"], index=1)
    tone = st.selectbox("Tom", ["neutro","motivacional","formal","casual","inspirador","técnico"], index=1)
    lang = st.selectbox("Idioma", ["pt-PT","en","es"], index=0)
    platforms = st.multiselect("Plataformas", ["instagram","tiktok","linkedin","blog","newsletter"], default=["instagram","tiktok"])
    count = st.slider("Nº de ideias por plataforma", 1, 10, 5)
    st.markdown("---")
    brand_style = st.selectbox("Estilo visual de marca", ["minimal clean","luxury","modern tech","playful","fitness gritty"], index=0)
    st.markdown("---")
    if st.button("Sair da sessão"):
        for k in ["user","contents","plan","seo","visuals"]:
            st.session_state.pop(k, None)
        st.experimental_rerun()

def need_credits(cost: int) -> bool:
    if st.session_state.credits < cost:
        st.error("⚠️ Sem créditos suficientes para esta ação.")
        return False
    st.session_state.credits -= cost
    return True

tab_content, tab_visual, tab_seo, tab_perf = st.tabs(["🧠 Conteúdo IA", "🎨 Imagem IA", "🔍 SEO & Estratégia", "📈 Performance"])

with tab_content:
    section_title("Geração de Conteúdo", "Ideias curtas, carrosséis e outlines de blog.")
    c1, c2, c3, c4 = st.columns(4)
    with c1: gen_click = st.button("Gerar conteúdo (–1)")
    with c2: reuse_click = st.button("Reaproveitar texto (–1)")
    with c3: plan_click = st.button("Plano semanal (–1)")
    with c4: clear_click = st.button("Limpar resultados")
    st.markdown("---")

    if gen_click and need_credits(1):
        with st.spinner("A gerar conteúdos…"):
            data = chat_json(CONTENT_SYSTEM, content_user(niche, objective, tone, lang, platforms, count), MODEL)
            st.session_state.contents = data
        st.success("✅ Conteúdo gerado.")

    txt = st.text_area("Cola aqui um texto para reaproveitar (blog/roteiro/anúncio):", height=120, placeholder="Cola aqui…")
    if reuse_click and need_credits(1):
        if not txt.strip():
            st.warning("Cola algum texto primeiro.")
        else:
            with st.spinner("A reaproveitar texto…"):
                res = chat_json("Transforma o texto seguinte em posts curtos PT‑PT. Responde em JSON {items:[{platform,idea,caption,hashtags,cta}]}.",
                                f"Texto base:\n{txt}\nPlataformas: {', '.join(platforms)} • Tom: {tone} • Língua: {lang}", MODEL)
                st.session_state.contents = st.session_state.contents or {"shorts":[], "carousels":[], "blogs":[]}
                st.session_state.contents["shorts"] += res.get("items", [])
            st.success("✅ Adicionado aos shorts.")

    if plan_click and need_credits(1):
        with st.spinner("A compor plano semanal…"):
            res = chat_json(PLAN_SYSTEM, plan_user(niche, objective, tone, lang, platforms), MODEL)
            st.session_state.plan = res.get("items", [])
        st.success("✅ Plano semanal pronto.")

    if clear_click:
        st.session_state.contents = None
        st.session_state.plan = []

    if st.session_state.contents:
        st.markdown("##### Shorts (Reels/TikTok/LinkedIn)")
        for i, s in enumerate(st.session_state.contents.get("shorts", [])[:200]):
            html = f"<b>{i+1}. [{s.get('platform','').upper()}]</b> — {s.get('idea','')}<br>" \
                   f"<span style='color:#475569'>{s.get('caption','')}</span><br>" \
                   f"<div style='margin:.2rem 0'>{' '.join([f'<span style=\\'background:#E8F0FF;border-radius:6px;padding:2px 6px;margin:2px;display:inline-block\\'>#{h}</span>' for h in s.get('hashtags', [])])}</div>" \
                   f"<span style='color:#0F172A'><b>CTA:</b> {s.get('cta','')}</span>"
            card(html)

        st.markdown("##### Carrosséis (IG)")
        for c in st.session_state.contents.get("carousels", []):
            bullets = "".join([f"<li>{b}</li>" for b in c.get("bullets", [])])
            card(f"<b>{c.get('title','')}</b><ul>{bullets}</ul>")

        st.markdown("##### Blogs")
        for b in st.session_state.contents.get("blogs", []):
            outline = "".Join([f"<li>{o}</li>" for o in b.get("outline", [])])  # Intentional error to test environment
            card(f"<b>{b.get('title','')}</b><ul>{outline}</ul>")

        st.markdown("---")
        colA, colB, colC = st.columns(3)
        with colA:
            st.download_button("Exportar CSV", export_csv_bytes(st.session_state.contents), file_name="contentforge_export.csv", mime="text/csv")
        with colB:
            st.download_button("Exportar TXT/MD", export_txt_bytes(st.session_state.contents), file_name="contentforge_export.txt", mime="text/plain")
        with colC:
            st.download_button("Exportar PDF", export_pdf_bytes(st.session_state.contents, "ContentForge Report"), file_name="contentforge_report.pdf", mime="application/pdf")

with tab_visual:
    section_title("Imagem IA", "Prompt automático + geração de imagem.")
    copy_for_visual = st.text_area("Copy base (usamos isto para sugerir o visual):", height=120, placeholder="Cola a legenda/copy…")
    vcol1, vcol2, vcol3 = st.columns([0.4,0.35,0.25])
    with vcol1: suggest_prompt = st.button("Sugerir prompt (–1)")
    with vcol2: gen_image = st.button("Gerar imagem IA (–2)")
    with vcol3: size = st.selectbox("Tamanho", ["1024x1024","1024x576","576x1024"], index=0)

    if suggest_prompt and need_credits(1):
        if not copy_for_visual.strip():
            st.warning("Cola a copy primeiro.")
        else:
            with st.spinner("A sugerir prompt…"):
                res = chat_json(VISUAL_PROMPT_SYSTEM, visual_prompt_user(niche, tone, brand_style, copy_for_visual), MODEL)
                st.session_state.last_prompt = res.get("prompt","")
            st.success("✅ Prompt sugerido.")
    st.text_input("Prompt final de imagem", value=st.session_state.get("last_prompt",""), key="prompt_final")

    if gen_image and need_credits(2):
        prompt = st.session_state.get("prompt_final","").strip()
        if not prompt:
            st.warning("Primeiro gera ou escreve um prompt.")
        else:
            with st.spinner("A gerar imagem…"):
                b64 = generate_image_b64(prompt, size=size)
                st.session_state.visuals.append(b64)
            st.success("✅ Imagem criada.")

    if st.session_state.visuals:
        st.markdown("##### Resultados")
        for idx, b64 in enumerate(st.session_state.visuals[-6:][::-1], 1):
            st.image(base64.b64decode(b64), caption=f"Imagem IA #{idx}")
        last = st.session_state.visuals[-1]
        st.download_button("Descarregar última imagem (PNG)", base64.b64decode(last), file_name="contentforge_image.png", mime="image/png")

with tab_seo:
    section_title("SEO & Estratégia", "Keywords, meta e títulos de artigo.")
    topic = st.text_input("Tópico/chave", value=niche)
    scol1, scol2 = st.columns([0.3,0.7])
    with scol1: seo_click = st.button("Gerar SEO (–1)")
    if seo_click and need_credits(1):
        with st.spinner("A gerar SEO…"):
            st.session_state.seo = chat_json(SEO_SYSTEM, seo_user(topic), MODEL)
        st.success("✅ SEO pronto.")
    if st.session_state.seo:
        kwords = st.session_state.seo.get("keywords", [])
        meta = st.session_state.seo.get("meta_description", "")
        titles = st.session_state.seo.get("title_suggestions", [])
        tag_html = " ".join([f"<span style='background:#E8F0FF;border-radius:6px;padding:2px 6px;margin:2px;display:inline-block'>#{k}</span>" for k in kwords])
        card(f"<b>Keywords</b><div>{tag_html}</div>")
        card(f"<b>Meta description</b><br><span style='color:#475569'>{meta}</span>")
        card("<b>Títulos sugeridos</b><ul>" + "".join([f"<li>{t}</li>" for t in titles]) + "</ul>")

with tab_perf:
    section_title("Performance & Insights", "Estimativas de impacto simuladas para reforçar valor.")
    shorts_n = len((st.session_state.contents or {}).get("shorts", []))
    imgs_n = len(st.session_state.visuals)
    plan_n = len(st.session_state.plan or [])
    base_eng = 0.4 + 0.03*shorts_n + 0.04*imgs_n + 0.02*(1 if plan_n else 0)
    eng = min(0.95, base_eng)
    ctr = min(0.12, 0.018 + 0.002*shorts_n + 0.004*imgs_n)
    time_saved = 45*max(shorts_n,1) - 5*max(shorts_n,1)
    card(f"""
    <b>Impacto IA (estimado)</b><br>
    🔹 Engajamento: <b>+{int(eng*100)}%</b><br>
    🔹 CTR médio em CTAs: <b>{round(ctr*100,1)}%</b><br>
    🔹 Tempo poupado (últimos conteúdos): <b>{time_saved} min</b><br>
    🔹 Volume de publicações semanais: <b>{3 + shorts_n//max(1,shorts_n) if shorts_n else 3}</b>
    """)
    card("<b>Dica da IA</b><br>Publica conteúdos educacionais às terças e quintas — tipicamente geram 1.3× mais interação no teu nicho.")

st.markdown("<hr/>", unsafe_allow_html=True)
st.caption("© 2025 ContentForge — Client Ready Pro • Streamlit-only • Sem base de dados (sessão local).")
