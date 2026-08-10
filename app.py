import os
from urllib.parse import urlparse

import streamlit as st
from firecrawl import Firecrawl


st.set_page_config(
    page_title="Firecrawl Scraper",
    page_icon="🔥",
    layout="wide",
)


def get_api_key() -> str | None:
    """Recupera la chiave prima da Streamlit Secrets e poi dalle variabili d'ambiente."""
    try:
        secret_key = st.secrets.get("FIRECRAWL_API_KEY")
        if secret_key:
            return secret_key
    except Exception:
        pass

    return os.getenv("FIRECRAWL_API_KEY")


def is_valid_url(url: str) -> bool:
    """Controlla che l'input sia un URL HTTP o HTTPS valido."""
    try:
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)
    except Exception:
        return False


def get_result_value(result, key: str, default=None):
    """Supporta sia oggetti SDK sia eventuali dizionari restituiti dall'API."""
    if isinstance(result, dict):
        return result.get(key, default)

    return getattr(result, key, default)


st.title("🔥 Firecrawl Scraper")
st.write(
    "Inserisci l'indirizzo di una pagina web per estrarne il contenuto "
    "in formato Markdown."
)

api_key = get_api_key()

if not api_key:
    st.error(
        "API key non configurata. Inseriscila in "
        "`.streamlit/secrets.toml` oppure nella variabile "
        "`FIRECRAWL_API_KEY`."
    )
    st.stop()

url = st.text_input(
    "URL da analizzare",
    placeholder="https://example.com",
)

col1, col2 = st.columns([1, 1])

with col1:
    scrape_button = st.button(
        "Estrai contenuto",
        type="primary",
        use_container_width=True,
    )

with col2:
    clear_button = st.button(
        "Pulisci risultato",
        use_container_width=True,
    )

if clear_button:
    st.session_state.pop("scrape_result", None)
    st.session_state.pop("scrape_url", None)
    st.rerun()

if scrape_button:
    if not url.strip():
        st.warning("Inserisci un URL.")
        st.stop()

    if not is_valid_url(url.strip()):
        st.error("Inserisci un URL valido che inizi con http:// o https://.")
        st.stop()

    try:
        with st.spinner("Firecrawl sta analizzando la pagina..."):
            firecrawl = Firecrawl(api_key=api_key)

            result = firecrawl.scrape(
                url.strip(),
                formats=["markdown"],
            )

        st.session_state["scrape_result"] = result
        st.session_state["scrape_url"] = url.strip()

    except Exception as error:
        st.error(f"Errore durante lo scraping: {error}")

result = st.session_state.get("scrape_result")
scraped_url = st.session_state.get("scrape_url")

if result:
    markdown_content = get_result_value(result, "markdown", "")

    metadata = get_result_value(result, "metadata", {})
    if metadata is None:
        metadata = {}

    st.divider()
    st.subheader("Risultato")

    if scraped_url:
        st.caption(f"URL analizzato: {scraped_url}")

    if not markdown_content:
        st.warning("Firecrawl non ha restituito contenuto Markdown.")
    else:
        st.download_button(
            label="Scarica Markdown",
            data=markdown_content,
            file_name="pagina_scrapeata.md",
            mime="text/markdown",
        )

        st.markdown(markdown_content)

    with st.expander("Metadati"):
        if isinstance(metadata, dict) and metadata:
            st.json(metadata)
        else:
            st.info("Nessun metadato disponibile.")