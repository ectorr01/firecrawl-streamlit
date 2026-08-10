import os
from urllib.parse import urlparse

import streamlit as st
from firecrawl import Firecrawl
from firecrawl.types import ScrapeOptions


st.set_page_config(
    page_title="Firecrawl Scraper",
    page_icon="🔥",
    layout="wide",
)


def get_api_key() -> str | None:
    try:
        secret_key = st.secrets.get("FIRECRAWL_API_KEY")
        if secret_key:
            return secret_key
    except Exception:
        pass
    return os.getenv("FIRECRAWL_API_KEY")


def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


st.title("🔥 Firecrawl Scraper")

api_key = get_api_key()
if not api_key:
    st.error("API key non configurata.")
    st.stop()

mode = st.radio(
    "Modalità",
    options=["Scrape (una pagina)", "Crawl (più pagine)"],
    horizontal=True,
)

url = st.text_input("URL", placeholder="https://example.com")

if mode == "Scrape (una pagina)":
    if st.button("Estrai contenuto", type="primary"):
        if not is_valid_url(url.strip()):
            st.error("Inserisci un URL valido.")
            st.stop()

        with st.spinner("Firecrawl sta analizzando la pagina..."):
            firecrawl = Firecrawl(api_key=api_key)
            result = firecrawl.scrape(url.strip(), formats=["markdown"])

        st.download_button(
            "Scarica Markdown",
            data=result.markdown or "",
            file_name="pagina.md",
            mime="text/markdown",
        )
        st.markdown(result.markdown or "Nessun contenuto trovato.")

else:
    limit = st.slider(
        "Numero massimo di pagine da crawlare",
        min_value=1,
        max_value=20,
        value=5,
        help="Ogni pagina consuma 1 credito Firecrawl. Parti con un valore basso.",
    )

    if st.button("Avvia crawl", type="primary"):
        if not is_valid_url(url.strip()):
            st.error("Inserisci un URL valido.")
            st.stop()

        with st.spinner(f"Crawling in corso (max {limit} pagine)..."):
            firecrawl = Firecrawl(api_key=api_key)
            crawl_result = firecrawl.crawl(
                url.strip(),
                limit=limit,
                scrape_options=ScrapeOptions(formats=["markdown"]),
                poll_interval=5,
            )

        pages = getattr(crawl_result, "data", []) or []
        st.success(f"Trovate {len(pages)} pagine.")

        for i, page in enumerate(pages, start=1):
            page_url = getattr(page, "url", None) or getattr(
                getattr(page, "metadata", None), "source_url", "URL non disponibile"
            )
            with st.expander(f"Pagina {i}: {page_url}"):
                st.markdown(getattr(page, "markdown", "") or "Nessun contenuto.")

        if pages:
            combined = "\n\n---\n\n".join(
                getattr(p, "markdown", "") or "" for p in pages
            )
            st.download_button(
                "Scarica tutte le pagine (Markdown)",
                data=combined,
                file_name="crawl_risultato.md",
                mime="text/markdown",
            )